#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')

import robot_smach_states as states

from psi import Compound, Conjunction, Sequence

class Move(object):
    def __init__(self, robot):
        """@param robot must be an instance of robot_skills.Amigo (TODO: generalize to Sergio)"""
        self.robot = robot

    def interpret(self, outcome):
        #import ipdb; ipdb.set_trace()

        name = "nowhere"
        nav_state = True
        try:
            destination = [entity.value for entity in outcome.entities if "destination" in entity.name][0]
            name = "the " + destination
            q = Compound("point_of_interest", destination, Compound("point_3d", "X", "Y", "Z"))
            #nav_state = states.NavigateGeneric(self.robot, lookat_query=q)
        except:
            pass

        try:
            destination = [entity.value for entity in outcome.entities if "contact" in entity.name][0]
            name = destination
            q = Conjunction(  Compound("property_expected", "ObjectID", "class_label", "person"),
                              Compound("property_expected", "ObjectID", "position", Sequence("X","Y","Z")),
                              Compound("property_expected", "ObjectID", "name", destination))
            #nav_state = states.NavigateGeneric(self.robot, lookat_query=q)
        except:
            pass

        if not nav_state or not name:
            self.robot.speech.speak("I should move, but I don't know where")
            return

        self.robot.speech.speak("I'll go to {0}".format(name))
        #nav_state.execute() #TODO: Outcommented nav_state because I can't run Amigo on my PC.


