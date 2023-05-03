#  import pyNN.spiNNaker as sim

import pyNN.nest as sim
from stateMachineClass import FSAHelperFunctions
from nealCoverClass import NealCoverFunctions

simName = "nest"
runtime = 1000

def createNeurons(fsa):
    ca = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label = "CA")
    fsa.makeCA(ca, 0)
    ca2 = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label = "CA 2")
    fsa.makeCA(ca2, 0)
    ca3 = sim.Population(fsa.CA_SIZE, sim.IF_cond_exp, fsa.CELL_PARAMS, label = "CA 3")
    fsa.makeCA(ca3, 0)
    n1 = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="Neuron 1")
    n2 = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="Neuron 2")
    n3 = sim.Population(1, sim.IF_cond_exp, fsa.CELL_PARAMS, label="Neuron 3")
    n1.record("spikes")
    n2.record("spikes")
    n3.record("spikes")
    ca.record("spikes")
    ca2.record("spikes")
    ca3.record("spikes")

    return ca, ca2, ca3, n1, n2, n3

def stateToState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)

    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateTurnsOnState(ca,0,ca2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca2.get_data().segments[0].spiketrains[0]) > 0
    
    if(not success):
        data = ca.get_data()
        print("ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2 ")
        print( data.segments[0].spiketrains[0])

        print( "State To State - {}".format(success))

def stateToNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n1.get_data().segments[0].spiketrains[0]) > 0

    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "State To Neuron - {}".format(success))

def twoStateToState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateHalfTurnsOnState(ca,0,ca3,0)
    fsa.stateHalfTurnsOnState(ca2,0,ca3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca3.get_data().segments[0].spiketrains[0]) > 0

    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = ca3.get_data()
        print( "ca3")
        print( data.segments[0].spiketrains[0])

        print( "2 State To State - {}".format(success))

def twoStateToState_Half():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateHalfTurnsOnState(ca,0,ca3,0)
    fsa.stateHalfTurnsOnState(ca2,0,ca3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca3.get_data().segments[0].spiketrains[0]) == 0

    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = ca3.get_data()
        print( "ca3")
        print( data.segments[0].spiketrains[0])

        print( "2 State To State Half - {}".format(success))

def twoStateToNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateHalfTurnsOnOneNueron(ca,0,n1,0)
    fsa.stateHalfTurnsOnOneNueron(ca2,0,n1,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n1.get_data().segments[0].spiketrains[0]) > 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "2 State To Neruon - {}".format(success))

def twoStateToNeuron_Half():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateHalfTurnsOnOneNueron(ca,0,n1,0)
    fsa.stateHalfTurnsOnOneNueron(ca2,0,n1,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n1.get_data().segments[0].spiketrains[0]) == 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "2 State To Neruon Half - {}".format(success))

def neuronToState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronTurnsOnState(n1,0,ca2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca2.get_data().segments[0].spiketrains[0]) > 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "Neruon To State - {}".format(success))

def neuronToNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronTurnsOnOneNeuron(n1,0,n2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n2.get_data().segments[0].spiketrains[0]) > 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])

        print( "Neruon To Neuron - {}".format(success))

def twoNeuronToState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)
    fsa.stateTurnsOnOneNeuron(ca,0,n2,0)

    fsa.oneNeuronHalfTurnsOnState(n1,0,ca2,0)
    fsa.oneNeuronHalfTurnsOnState(n2,0,ca2,0)


    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca2.get_data().segments[0].spiketrains[0]) > 0

    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])

        print( "2 Neruon To State - {}".format(success))

def twoNeuronToState_Half():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)
    
    fsa.oneNeuronHalfTurnsOnState(n1,0,ca2,0)
    fsa.oneNeuronHalfTurnsOnState(n2,0,ca2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca2.get_data().segments[0].spiketrains[0]) == 0
    if (not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])

        print( "2 Neruon To State Half - {}".format(success))

def twoNeuronToNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)
    fsa.stateTurnsOnOneNeuron(ca,0,n2,0)

    fsa.oneNeuronHalfTurnsOnOneNeuron(n1,0,n3,0)
    fsa.oneNeuronHalfTurnsOnOneNeuron(n2,0,n3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n3.get_data().segments[0].spiketrains[0]) > 0
    if (not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])
        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])
        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])
        data = n3.get_data()
        print( "n3")
        print( data.segments[0].spiketrains[0])
        print( "2 Neruon To Neuron - {}".format(success))

def twoNeuronToNeuron_Half():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)
    
    fsa.oneNeuronHalfTurnsOnState(n1,0,n3,0)
    fsa.oneNeuronHalfTurnsOnState(n2,0,n3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n3.get_data().segments[0].spiketrains[0]) == 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])

        data = n3.get_data()
        print( "n3")
        print( data.segments[0].spiketrains[0])

        print( "2 Neruon To Neuron Half - {}".format(success))

def neruonAndStateToState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronHalfTurnsOnState(n1,0,ca3,0)
    fsa.stateHalfTurnsOnState(ca2,0,ca3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca3.get_data().segments[0].spiketrains[0]) > 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = ca3.get_data()
        print( "ca3")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "Neuron And State To State - {}".format(success))

def neruonAndStateToState_NotNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronHalfTurnsOnState(n1,0,ca3,0)
    fsa.stateHalfTurnsOnState(ca2,0,ca3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca3.get_data().segments[0].spiketrains[0]) == 0

    if not success:
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = ca3.get_data()
        print( "ca3")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "Neuron And State To State NotNeuron - {}".format(success))

def neruonAndStateToState_NotState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronHalfTurnsOnState(n1,0,ca3,0)
    fsa.stateHalfTurnsOnState(ca2,0,ca3,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca3.get_data().segments[0].spiketrains[0]) == 0
    if not success:
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = ca3.get_data()
        print( "ca3")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        print( "Neuron And State To State NotState - {}".format(success))

def neuronAndStateToNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronHalfTurnsOnOneNeuron(n1,0,n2,0)
    fsa.stateHalfTurnsOnOneNueron(ca2,0,n2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n2.get_data().segments[0].spiketrains[0]) > 0
    if not success:

        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])

        print( "Neuron And State To Neuron - {}".format(success))

def neuronAndStateToNeuron_NotNeuron():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronHalfTurnsOnOneNeuron(n1,0,n2,0)
    fsa.stateHalfTurnsOnOneNueron(ca2,0,n2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)

    neal.nealApplyProjections()
    
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)

    sim.run(runtime)

    success = len(n2.get_data().segments[0].spiketrains[0]) == 0
    if not success:

        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])

        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])

        print( "Neuron And State To Neuron NotNeuron - {}".format(success))


def neuronAndStateToNeuron_NotState():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronHalfTurnsOnOneNeuron(n1,0,n2,0)
    fsa.stateHalfTurnsOnOneNueron(ca2,0,n2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n2.get_data().segments[0].spiketrains[0]) == 0
    if success:
        return

    data = ca.get_data()
    print( "ca")
    print( data.segments[0].spiketrains[0])

    data = ca2.get_data()
    print( "ca2")
    print( data.segments[0].spiketrains[0])

    data = n1.get_data()
    print( "n1")
    print( data.segments[0].spiketrains[0]  )

    data = n2.get_data()
    print( "n2")
    print( data.segments[0].spiketrains[0]    )

    print( "Neuron And State To Neuron NotState - {}".format(success))

def threeStateRule():
    """

    STATE1 ===>
             + ===> N1 ===>
    STATE2 ===>            + ===> A1 ===> STATE4
                STATE3 ===>

    """

    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)

    fsa.stateHalfTurnsOnOneNueron(ca,0,n1,0)
    fsa.stateHalfTurnsOnOneNueron(ca2,0,n1,0)

    fsa.oneNeuronHalfTurnsOnOneNeuron(n1,0,n2,0)
    fsa.stateHalfTurnsOnOneNueron(ca3,0,n2,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)
    spikeTimes = {'spike_times': [[sim.get_current_time()+10]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca2,0)
    spikeTimes = {'spike_times': [[sim.get_current_time()+15]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca3,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(n2.get_data().segments[0].spiketrains[0]) > 0
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])
    
        data = ca2.get_data()
        print( "ca2")
        print( data.segments[0].spiketrains[0])
    
        data = ca3.get_data()
        print( "ca3")
        print( data.segments[0].spiketrains[0])
    
        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])
    
        data = n2.get_data()
        print( "n2")
        print( data.segments[0].spiketrains[0])
    
        print( "Three State Rule - {}".format(success))


def oneNeuronStopsCA():
    neal = NealCoverFunctions(simName, sim)
    fsa = FSAHelperFunctions(simName, sim, neal)
    ca,ca2,ca3,n1,n2,n3 = createNeurons(fsa)
    fsa.stateTurnsOnOneNeuron(ca,0,n1,0)

    fsa.oneNeuronTurnsOffState(n1,0,ca,0)

    spikeTimes = {'spike_times': [[sim.get_current_time()+5]]}
    spikeGen = sim.Population(1, sim.SpikeSourceArray, spikeTimes)
    fsa.turnOnStateFromSpikeSource(spikeGen,ca,0)

    neal.nealApplyProjections()

    sim.run(runtime)

    success = len(ca.get_data().segments[0].spiketrains[0]) == len(n1.get_data().segments[0].spiketrains[0])
    if(not success):
        data = ca.get_data()
        print( "ca")
        print( data.segments[0].spiketrains[0])

        data = n1.get_data()
        print( "n1")
        print( data.segments[0].spiketrains[0])
        print( "One Neuron stops CA - {}".format(success))



sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
stateToState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
stateToNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoStateToState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoStateToState_Half()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoStateToNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoStateToNeuron_Half()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neuronToState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neuronToNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoNeuronToState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoNeuronToState_Half()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoNeuronToNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
twoNeuronToNeuron_Half()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neruonAndStateToState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neruonAndStateToState_NotNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neruonAndStateToState_NotState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neuronAndStateToNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neuronAndStateToNeuron_NotNeuron()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
neuronAndStateToNeuron_NotState()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
threeStateRule()
sim.end()

sim.setup(timestep=1.0,min_delay=1.0,max_delay=1.0, debug=0)
oneNeuronStopsCA()
sim.end()
