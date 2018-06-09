# Introduction 
This is a N-ARC (Neural Architecture of Cognition). 

# Getting Started
1.	Installation process:
    1. Clone the Repository
2.	Software dependencies:
    1. Nest
    2. pyNN


# How to Use It

Main code is in the rbs.py file

To use the system add the following imports to a new file:
1. import nealParams as nealParameters
2. import pyNN.nest as sim
3. from rbs import RBS

Start the sim:
sim.setup(...)

Construct new RBS
rbs = RBS()

To add facts call:
rbs.addFact()

To add rules:
rbs.addRules()

Run the sim:
sim.run(...)


#Test

Run the runRBSTests.sh in bash. This will generete a results folder each of it will contain a .sp file with spikes from each test

#Facts

Facts are constructed in the following syntax:

'("{name}",{properties})'

- {name} - is the name of the fact group
- {properties} - is a tuple (e.g. ("banana",0) )

#Rules

Rules are consturcted in the following sytanx:

'("{name}",({conditions},{operations}))'

- {name} - is the name of the rule
- {conditions} - is the conditions for the rule:
    - condition syntax: ({positive}, "{name}", {properties}, {binding)
        - {positive} - bool determines if the conditons has to be true or false
        - {name} - name of the fact group
        - {properties} - is a tuple of fact properties
            - can be any value
            - "?" - symbol matches any value
            - "?var" - matches any value, keeps it for operations under the same name
        - {binding} - used for retractions to specify which fact to retract (see below)
- {operations} - there 2 different operations:
    - assert - turns on state, syntax: ("assert",("{name}",{properties})):
        - {name} - name of the fact group
        - {properties} - is a tuple of fact properties
            - can be any value
            - "?var" - will use a value found in preconditions
    - retract - turns off state, syntax ("retract","{binding}")
        - {binding} - name of the condition that matches the fact (see above)
