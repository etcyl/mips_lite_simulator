from simulator import Simulator
from simulator_no_forwarding import Simulator_no_forwarding

def main():
    #simulator = Simulator()
    #simulator.show_instruction = False
    #simulator.simulation()


    simulator_no_forwarding = Simulator_no_forwarding()

    simulator_no_forwarding.simulation()



if __name__ == '__main__':
    main()
