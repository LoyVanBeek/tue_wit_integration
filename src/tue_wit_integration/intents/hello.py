#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')

class Hello(object):
    def __init__(self, robot):
        """@param robot must be an instance of robot_skills.Amigo (TODO: generalize to Sergio)"""
        self.robot = robot

    def interpret(self, outcome):
        self.robot.speech.speak("Hi there yourself!")