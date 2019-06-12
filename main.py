from simulator import Simulator
from simulator_no_forwarding import Simulator_no_forwarding
from simulator_forwarding import Simulator_forwarding

def main():
    simulator = Simulator()
    simulator_no_forwarding = Simulator_no_forwarding()
    simulator_forwarding = Simulator_forwarding()

    memory_trace = 'final_proj_trace.txt'
    simulator.memory_trace = memory_trace
    simulator_no_forwarding.memory_trace = memory_trace
    simulator_forwarding.memory_trace = memory_trace
    # Read Memory trace by lines
    print("""MIPS simulation Enter option (1-3):\n
     1) Functional simulator only\n
     2) Functional simulator + Timing simulator assuming no pipeline forwarding\n
     3) Functional simulator + Timing simulator with pipeline forwarding\n""")  # Pass a list of instructions to test

    option = input('Enter Number:')

    if int(option) == 1:
        simulator.show_instruction=False
        simulator.simulation()
    elif int(option) == 2:
        simulator_no_forwarding.simulation()
    elif int(option) == 3:
        simulator_forwarding.simulation()
    else:
        simulator.simulation()
        simulator_no_forwarding.simulation()
        simulator_forwarding.simulation()




if __name__ == '__main__':
    main()
