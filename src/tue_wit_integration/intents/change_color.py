#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')

colormapping = {}
colormapping["red"]     = (255, 0,      0)
colormapping["blue"]    = (0,   0,      255)
colormapping["green"]   = (0,   255,    0)
colormapping["purple"]  = (255, 0,      255)
colormapping["orange"]  = (255, 140,    0)
colormapping["yellow"]  = (255, 255,    0)
colormapping["pink"]    = (255, 192,    203)
colormapping["brown"]   = (94,  38,     18)
colormapping["gray"]    = (169, 169,    169)

class ChangeColor(object):
    def __init__(self, robot):
        """@param robot must be an instance of robot_skills.Amigo (TODO: generalize to Sergio)"""
        self.robot = robot

    def interpret(self, outcome):
        #import ipdb; ipdb.set_trace()

        color = [entity.value for entity in outcome.entities if "color" in entity.name][0]
        
        if color in colormapping:
            rgb = colormapping[color]
            self.robot.lights.set_color(*rgb)
        else:
            self.robot.speech.speak("I don't know the color {0}".format(color))





