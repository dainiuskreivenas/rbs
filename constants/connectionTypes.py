class ConnectionTypes:
    ### State to State
    ON = 0
    HALF_ON = 1
    OFF = 2
    HALF_OFF = 3

    ### State to Neuron
    ON_ONE = 4
    HALF_ON_ONE = 5

    ### Neuron to State
    ONE_ON = 6
    ONE_HALF_ON = 7
    ONE_OFF = 8
    ONE_HALF_OFF = 9

    ### Neuron to Neuron
    ONE_ON_ONE = 10
    ONE_HALF_ON_ONE = 11