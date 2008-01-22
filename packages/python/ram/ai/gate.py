# Copyright (C) 2008 Maryland Robotics Club
# Copyright (C) 2008 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:  packages/python/ram/ai/gate.py

"""
A state machine to go through the gate:
 - Waits for Switch
 - Dives to depth
 - Goes forward for a time
 - Surfaces
 
Reguires the following subsystems:
 - timerManager - ram.timer.TimerManager
 - motionManager - ram.motion.MotionManager
 - controller - ext.control.IController
"""

# TODO: Add some way for required subsystems to be checked more throughly

# Project Imports
import ext.core as core

import ram.ai.state as state
import ram.motion as motion

class Wait(state.State):
    @staticmethod
    def transitions():
        # TODO: Replace with a start event from the vehicle or sensor board
        return {"Start" : Dive}
    
class Dive(state.State):
    @staticmethod
    def transitions():
        return {motion.Motion.FINISHED : Forward}
    
    def enter(self):
        # Go to 5 feet in 5 increments
        diveMotion = motion.ChangeDepth(5, 5)
        self.motionManager.setMotion(diveMotion)
    
class Forward(state.State):
    FORWARD_DONE = core.declareEventType('FORWARD_DONE')

    @staticmethod
    def transitions():
        return {Forward.FORWARD_DONE : Surface}

    def enter(self):
        # Full speed ahead!!
        self.controller.setSpeed(3)
        
        # Timer goes off in 10 seconds then sends off FORWARD_DONE
        timer = self.timerManager.newTimer(Forward.FORWARD_DONE, 10)
        timer.start()
    
    def exit(self):
        self.controller.setSpeed(0)
        
class Surface(state.State):
    @staticmethod
    def transitions():
        return {motion.Motion.FINISHED : End}     
    
    def enter(self):  
        # Go to 0 feet in 5 increments
        surfaceMotion = motion.ChangeDepth(0, 5)
        self.motionManager.setMotion(surfaceMotion)
        
class End(state.State):
    def enter(self):
        print 'Mission Complete'