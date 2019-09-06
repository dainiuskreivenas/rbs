class Population:
    def __init__(self, sim, fsa, neurons, fromIndex):
        self.pop = sim.Population(neurons, sim.IF_cond_exp, fsa.CELL_PARAMS)
        self.pop.record("spikes")
        self.fromIndex = fromIndex
        self.toIndex = fromIndex + neurons
