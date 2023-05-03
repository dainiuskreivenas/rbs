class ConnectionTypes:
    ### State to State
    ON: int = 0
    HALF_ON: int = 1
    OFF: int = 2
    HALF_OFF: int = 3

    ### State to Neuron
    ON_ONE: int = 4
    HALF_ON_ONE: int = 5

    ### Neuron to State
    ONE_ON: int = 6
    ONE_HALF_ON: int = 7
    ONE_OFF: int = 8
    ONE_HALF_OFF: int = 9

    ### Neuron to Neuron
    ONE_ON_ONE: int = 10
    ONE_HALF_ON_ONE: int = 11