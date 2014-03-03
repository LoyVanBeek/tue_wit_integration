#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')

class Give(object):
    def __init__(self, robot):
        """@param robot must be an instance of robot_skills.Amigo (TODO: generalize to Sergio)"""
        self.robot = robot

    def interpret(self, outcome):
        item = "something"
        try:
            item = [entity.value for entity in outcome.entities if entity.name == "item"][0]
        except:
            pass
        
        contact = "someone"
        try:
            contact = [entity.value for entity in outcome.entities if entity.name == "contact"][0]
            if contact == "me":
                contact = "you"
        except:
            pass
        self.robot.speech.speak("I'll give {1} {0}".format(item, contact))