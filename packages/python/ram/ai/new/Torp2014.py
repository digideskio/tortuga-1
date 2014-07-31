import ram.ai.new.utilClasses as utilClasses
import ram.ai.new.utilStates as utilStates
import ram.ai.new.motionStates as motion
import ram.ai.new.searchPatterns as search
import ram.ai.new.searchPatterns as searches
import ram.ai.new.stateMachine as stateMachine
import ram.ai.new.state as state
import ram.ai.new.approach as approach


class TorpedoTask(utilStates.Task):
    def __init__(self, configNode, success, failure, duration = 300):
        super(TorpedoTask,self).__init__(TorpedoMachine(configNode),success, failure, duration) 

    def update(self):
        super(TorpedoTask,self).update()
        if self.getInnerStateMachine().getCurrentState().getName() == 'taskFailed':
            self.doTransition('failure')
        elif self.getInnerStateMachine().getCurrentState().getName() == 'taskSuccess':
            self.doTransition('success')
            

class FireLeft(state.State):
    def __init__(self, next):
        super(FireLeft, self).__init__()
        self.setTransition('next', next)

    def update(self):
        self.getStateMachine().getLegacyState().vehicle.fireTorpedoIndex(0)
        print 'HETERER'
        self.doTransition('next')



class FireRight(state.State):
    def __init__(self, next):
        super(FireRight, self).__init__()
        self.setTransition('next', next)

    def update(self):
        self.getStateMachine().getLegacyState().vehicle.fireTorpedoIndex(1)
        self.doTransition('next')


class TorpedoMachine(stateMachine.StateMachine):
    def __init__(self, configNode):
        super(TorpedoMachine,self).__init__()
    #other hole option is to shoot through the large hole, torps.large
        initialDepth = configNode.get('initialDepth',5)
        yawSearchBound = configNode.get('yawSearchAngle',0)
        forwardsSearchIncrement = configNode.get('forwardsSearchIncrement',5)
        maxSearchAttempts = configNode.get('maxSearchAttempts', 20)
        holeSearchDist = configNode.get('holeSearchDist',1)
        squareCenteringRange = configNode.get('squareCenteringRange',30) 
        squareCenteringRangeBound = configNode.get('squareCenteringRangeBound', 50)
        squareCenteringXYBound = configNode.get('squareCenteringXYBound', .1)
        holeCenteringRange = configNode.get('holeCenteringRange', 50)
        holeCenteringRangeBound = configNode.get('holeCenteringRangeBound', 8)
        holeCenteringXYBound = configNode.get('holeCenteringXYBound', .1) 
        reverseRefindDistance = configNode.get('reverseRefindDistance', 1)
        
    #later on, put code in here that picks what torpedos we're after
    #for now, we're going buoy thunting
        #not a hack anymore, this ones real!
        torps = utilClasses.TorpedoGroupObject(self.getLegacyState())
        #hole1 = utilClasses.OldSimulatorHackVisionObject(self.getLegacyState())
        #hole2 = utilClasses.OldSimulatorHackVisionObject(self.getLegacyState())
        #torps = hole1
        #torps.box = hole1
        #END HACK TO TEST IN SIMULATOR
        hole1 = torps.left
        hole2 = torps.right
        box = torps.left

        start = self.addState('start',utilStates.Start())
        start.setTransition('next','initialMove')
        endS = self.addState('taskSuccess',utilStates.End())
        endF = self.addState('taskFailure',utilStates.End())
    #box finding search
        initialMove = self.addState('initialMove', motion.Turn(-yawSearchBound/2))
        initialMove.setTransition('next', 'initialSearch')
        initialSearch = self.addState('initialSearch', searches.YawSearchPattern(yawSearchBound, box.isSeen, 'boxCentering', 'prepareForwards'))
        prepareForwards =  self.addState('prepareForwards', motion.Turn(-yawSearchBound/2))
        prepareForwards.setTransition('next', 'forwardsSearch')
        forwardsSearch = self.addState('forwardsSearch', search.ForwardsSearchPattern(forwardsSearchIncrement, box.isSeen, 'boxCentering', 'counter'))
        counter = self.addState('counter', utilStates.PassCounter('passSwitch'))
        passSwitch = self.addState('passSwitch', utilStates.Switch('initialMove', 'taskFailure', counter.getPassChecker(maxSearchAttempts)))
    #aligning with box, if that fails, try to search again
        boxCentering = self.addState('boxCentering', approach.ForwardsCenter(box, 'holePassCount', 'initialMove', squareCenteringRange, squareCenteringXYBound,squareCenteringXYBound,squareCenteringRangeBound))
        holePassCount = self.addState('holePassCount', utilStates.PassCounter('holeSwitch'))
        holeSwitch = self.addState('holeSwitch', utilStates.Switch('hole1Search','hole2Search',holePassCount.getPassChecker(2)))
        hole1Search = self.addState('hole1Search', search.ForwardsSearchPattern(holeSearchDist, hole1.isSeen,'hole1Center', 'backUp'))
        hole1Center = self.addState('hole1Center', approach.ForwardsCenter(hole1, 'fireLeft', 'backUp', holeCenteringRange, holeCenteringXYBound, holeCenteringXYBound, holeCenteringRangeBound))
        fireLeft = self.addState('fireLeft', FireLeft('backUp'))
        backUp = self.addState('backUp', motion.Forward(-reverseRefindDistance))
        backUp.setTransition('next', 'holePassCount')
        hole2Search = self.addState('hole2Search', search.ForwardsSearchPattern(holeSearchDist, hole1.isSeen,'hole2Center', 'backUp'))
        hole2Center = self.addState('hole2Center', approach.ForwardsCenter(hole1, 'fireRight', 'backUp', holeCenteringRange, holeCenteringXYBound, holeCenteringXYBound, holeCenteringRangeBound))
        fireRight = self.addState('fireRight', FireRight('taskSuccess'))
    #Now that manipulator is dropped, this probably just needs to move to the side to prepare for the sonar task
    

    
