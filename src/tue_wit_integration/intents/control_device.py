#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')
import rospy

import robot_smach_states as states

from psi import Compound, Conjunction, Sequence

class ControlDevice(object):
    def __init__(self, robot):
        """@param robot must be an instance of robot_skills.Amigo (TODO: generalize to Sergio)"""
        self.robot = robot

    def interpret(self, outcome):
        #import ipdb; ipdb.set_trace()

        device = None
        switch_on = True
        room = True
        try:
            device = [entity.value for entity in outcome.entities if "device" in entity.name][0]
        except:
            rospy.logwarn("No device specified")

        try:
            room = [entity.value for entity in outcome.entities if "location" in entity.name][0]
        except:
            rospy.logwarn("No room specified")

        try:
            switch_on = [entity.value for entity in outcome.entities if "on_off" in entity.name][0]
        except:
            rospy.logwarn("No new switch state (on/off) specified")

        sentence = "I don't know what to turn on or off."
        if device and switch_on and room:
            sentence = "I'll turn {0} the {1} in the {2}".format(switch_on, device, room)
        if device and switch_on:
            if switch_on != "toggle":
                sentence = "I'll turn {0} the {1}".format(switch_on, device)
            sentence = "I'll toggle the {0}".format(device)

        self.robot.speech.speak(sentence)





