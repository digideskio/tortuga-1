# Copyright (C) 2008 Maryland Robotics Club
# Copyright (C) 2008 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:  packages/python/ram/ai/light.pyc    
"""
A state machine for finding and hitting the red light
 - Search for light
 - Seeks light when found (goes back to search if lost)
 - Forward ram when close
 - Halts vehicle
 
 
Requires the following subsystems:
 - timerManager - ram.timer.TimerManager
 - motionManager - ram.motion.MotionManager
 - controller - ext.control.IController
"""

# Project Imports
import ext.core as core
import ext.vision as vision

import ram.ai.state as state
import ram.motion as motion
import ram.motion.search
import ram.motion.seek

class Searching(state.State):
    @staticmethod
    def transitions():
        return { vision.EventType.LIGHT_FOUND : Seek }

    def enter(self):
        # Turn on the vision system
        self.visionSystem.redLightDetectorOn()

        # Create zig zag search to 
        zigZag = motion.search.ForwardZigZag(
            legTime = 15,
            sweepAngle = 60,
            speed = 2.5)
        self.motionManager.setMotion(zigZag)

    def exit(self):
        self.motionManager.stopCurrentMotion()

class Seek(state.State):
    @staticmethod
    def transitions():
        return { vision.EventType.LIGHT_LOST : Searching,
                 vision.EventType.LIGHT_FOUND : Seek,
                 vision.EventType.LIGHT_ALMOST_HIT : Hit }

    def LIGHT_FOUND(self, event):
        """Update the state of the light, this moves the vehicle"""
        self._light.setState(event.azimuth, event.elevation, event.range,
                             event.x, event.y)

    def enter(self):
        self._light = ram.motion.seek.PointTarget(0, 0, 0, 0, 0)
        motion = ram.motion.seek.SeekPoint(target = self._light,
                                           maxSpeed = 3,
                                           depthGain = 1.5)
        self.motionManager.setMotion(motion)

    def exit(self):
        self.motionManager.stopCurrentMotion()

class Hit(state.State):
    FORWARD_DONE = core.declareEventType('FORWARD_DONE')
    
    @staticmethod
    def transitions():
        return {Hit.FORWARD_DONE : End}

    def enter(self):
        self.visionSystem.redLightDetectorOff()

        # Timer goes off in 3 seconds then sends off FORWARD_DONE
        self.timer = self.timerManager.newTimer(Hit.FORWARD_DONE, 3)
        self.timer.start()
        self.controller.setSpeed(3)
    
    def exit(self):
        self.timer.stop()
        self.controller.setSpeed(0)
        
class End(state.State):
    pass
