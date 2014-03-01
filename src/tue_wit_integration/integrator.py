#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')

import rospy

from std_msgs.msg import String

from wit_ros.srv import Interpret, ListenAndInterpret
from wit_ros.msg import Outcome, Entity

from intents.hello import Hello
from intents.give import Give

import robot_skills.amigo

mapping = dict()
mapping["hello"] = Hello
mapping["give"] = Give

class Integration(object):
    """Listen until called by name, then start wit_ros's listen_and_interpret service"""
    def __init__(self, robot):
        self.robot = robot
        self.listen_and_interpret = rospy.ServiceProxy("/wit/listen_interpret", ListenAndInterpret)

    def check_for_calling(self, message):
        rospy.logdebug("Received text {0}".format(message.data))
        if message.data.lower() in ["amigo", "sergio"]: #Susan because the others are not in the dorpus ATM
            #I have been called!
            try:
                rospy.loginfo("Start listening...")
                response = self.listen_and_interpret()
                outcome = response.outcome

                rospy.loginfo("Starting execution of {0}".format(outcome))
                interpreting_class = mapping[outcome.intent] #Which class to use for this interpretation
                interpreter = interpreting_class(self.robot) #Instantiate an instance of this class
                interpreter.interpret(outcome) #Finally pass the outcome to this class
            except rospy.ServiceException:
                rospy.logerr("Could not interpret command")

if __name__ == "__main__":
    rospy.init_node("tue_wit_integration", log_level=rospy.DEBUG)

    robot = robot_skills.amigo.Amigo(dontInclude=['base','arms','perception','head', 'worldmodel', 'reasoner'])

    i = Integration(robot)
    subscriber = rospy.Subscriber("/speech/output", String, i.check_for_calling)

    rospy.spin()