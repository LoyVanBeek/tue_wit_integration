#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')

import rospy

from std_msgs.msg import String

from wit_ros.srv import Interpret, ListenAndInterpret

import sys

from intents.hello import Hello
from intents.give import Give
from intents.move import Move
from intents.control_device import ControlDevice
from intents.change_color import ChangeColor

import robot_skills.amigo

class Integration(object):
    """Listen until called by name, then start wit_ros's listen_and_interpret service"""
    def __init__(self, intent_args=[], intent_kwargs={}): 
        #using list and dict as default args may be hazardous, but we init only once in this script
        self.listen_and_interpret = rospy.ServiceProxy("/wit/listen_interpret", ListenAndInterpret)
        self.interpret = rospy.ServiceProxy("/wit/interpret", Interpret)

        self.busy = False

        self.mapping = dict()
        self.mapping["hello"] = Hello(*intent_args, **intent_kwargs)
        self.mapping["give"] = Give(*intent_args, **intent_kwargs)
        self.mapping["move"] = Move(*intent_args, **intent_kwargs)
        self.mapping["control_device"] = ControlDevice(*intent_args, **intent_kwargs)
        self.mapping["change_color"] = ChangeColor(*intent_args, **intent_kwargs)

    def check_for_calling(self, message):
        rospy.logdebug("Received text {0}".format(message.data))
        if message.data.lower() in ["amigo", "sergio"]:
            #I have been called!
            if self.busy: 
                rospy.loginfo("Call heard, but busy processing earlier call")
            if not self.busy:
                self.busy = True
                try:
                    rospy.loginfo("Start listening...")
                    response = None
                    if len(sys.argv) >= 2 and sys.argv[1] == "manual":
                        manual = raw_input("Sentence: ")
                        response = self.interpret(manual)
                    else:
                        response = self.listen_and_interpret()
                    outcome = response.outcome

                    rospy.loginfo("Starting execution of {0}".format(outcome))
                    try:
                        interpreter = self.mapping[outcome.intent]
                        interpreter.interpret(outcome)
                    except KeyError:
                        rospy.logerr("No interpretation for intent '{0}'".format(outcome.intent))
                        #self.robot.speech.speak("I heard what you said, but i don't know how to process a {0} command".format(outcome.intent.replace("_", " ")))
                except rospy.ServiceException:
                    rospy.logerr("Could not interpret command")
                    #self.robot.speech.speak("I couldn't hear you properly, maybe my ears are clogged")
                self.busy = False

if __name__ == "__main__":
    rospy.init_node("tue_wit_integration", log_level=rospy.INFO)

    robot = robot_skills.amigo.Amigo(dontInclude=['base','arms','perception','head', 'worldmodel'])

    i = Integration(intent_args=[robot])
    subscriber = rospy.Subscriber("/speech/output", String, i.check_for_calling, queue_size=1)

    rospy.spin()