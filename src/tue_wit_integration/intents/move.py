#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('tue_wit_integration')
import rospy

import robot_smach_states as states

from psi import Compound, Conjunction, Sequence, Constant

class Move(object):
    def __init__(self, robot):
        """@param robot must be an instance of robot_skills.Amigo (TODO: generalize to Sergio)"""
        self.robot = robot

    def interpret(self, outcome):
        import ipdb; ipdb.set_trace()

        
        self.robot.reasoner.query(Compound("load_database", "tue_knowledge", 'prolog/locations.pl'))
        self.robot.reasoner.query(Compound("load_database", "tue_knowledge", 'prolog/objects.pl'))

        name = "nowhere"
        nav_state = True
        try:
            destination = [entity.value for entity in outcome.entities if "destination" in entity.name][0]

            wp = Conjunction(Compound("environment", "Env"), Compound("waypoint", "Env", "Chal", "Name", "Pose"))
            waypoints = self.robot.reasoner.query(wp)
            simple_waypoint_names = [str(ans["Name"]).replace("_", " ") for ans in waypoints if isinstance(ans["Name"], Constant)]

            kwargs = {}
            if destination in simple_waypoint_names:
                name = "the " + destination
                query = Conjunction(
                        Compound("environment", "E"), 
                        Compound("waypoint", "E", "Challenge", destination, Compound("pose_2d", "X", "Y", "Phi")))
                kwargs = {"goal_query":query}
            else:
                poi = Conjunction(Compound("environment", "Env"), Compound("point_of_interest", "Env", "Chal", "Name", "Point"))
                pois = self.robot.reasoner.query(poi)
                simple_poi_names = [str(ans["Name"]).replace("_", " ") for ans in pois if isinstance(ans["Name"], Constant)]
                if destination in simple_poi_names:
                    name = "the " + destination
                    query = Conjunction(
                            Compound("environment", "E"), 
                            Compound("point_of_interest", destination, Compound("point_3d", "X", "Y", "Z")))
                    kwargs = {"lookat_query":query}

                self.robot.speach.speak("There is nothing named {0}, I don't know where to go".format(destination))

            try:
                nav_state = states.NavigateGeneric(self.robot, **kwargs)
            except Exception, e:
                rospy.logerr(e)

        except:
            pass

        try:
            destination = [entity.value for entity in outcome.entities if "contact" in entity.name][0]
            name = destination
            q = Conjunction(  Compound("property_expected", "ObjectID", "class_label", "person"),
                              Compound("property_expected", "ObjectID", "position", Sequence("X","Y","Z")),
                              Compound("property_expected", "ObjectID", "name", destination))
            try:
                nav_state = states.NavigateGeneric(self.robot, lookat_query=q)
            except Exception, e:
                rospy.logerr(e)
        except:
            pass

        if not nav_state or not name:
            self.robot.speech.speak("I should move, but I don't know where")
            return

        self.robot.speech.speak("I'll go to {0}".format(name))
        #nav_state.execute() #TODO: Outcommented nav_state because I can't run Amigo on my PC.


