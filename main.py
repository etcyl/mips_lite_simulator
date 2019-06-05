from simulator import Simulator
from simulator_no_forwarding import Simulator_no_forwarding
from simulator_forwarding import Simulator_forwarding

def main():
    simulator = Simulator()
    simulator_no_forwarding = Simulator_no_forwarding()
    simulator_forwarding = Simulator_forwarding()
    # Read Memory trace by lines
    print("""MIPS simulation Enter option (1-4):\n
     1) Functional simulator only\n
     2) Functional simulator + Timing simulator assuming no pipeline forwarding\n
     3) Functional simulator + Timing simulator with pipeline forwarding\n""")  # Pass a list of instructions to test

    option = input('Enter Number:')

    if int(option) == 1:
        simulator.simulation()
    elif int(option) == 2:
        simulator_no_forwarding.simulation()
    elif int(option) == 3:
        simulator_forwarding.simulation()
    else:
        print('invalid input')



if __name__ == '__main__':
    main()
