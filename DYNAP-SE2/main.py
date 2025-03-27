
import samna

from lib.dynapse2_init import connect, dynapse2board
from robot_control import comparator, wta_shifted_4joints, robot_control_separate_inputs
import os

class Device:
    device = None


def main():

    # Profile info:
    #   * csv custom name
    boardName = "XXXXXX"
    #   * Profile path + filename
    profileName = "XXXXXX.json"
    # Device info:
    #   * Bitfile of the board used
    bitfiles = ['XXXXXX.bit']
    #   * Type of device "stack" or "devboard"
    deviceName = "stack"
    device = Device()
    device.device = deviceName
    #   * Number of chips used (default = 1)
    number_of_chips = 1
    #   * Experiment (0 = comparator, 1 = wta, 2 = full system)
    experiment = 2

    # Connection info:
    receiver_endpoint = "tcp://0.0.0.0:33335"
    sender_endpoint = "tcp://0.0.0.0:33336"
    node_id = 1
    interpreter_id = 2

    # Create the samna connection
    samna_node = samna.SamnaNode(sender_endpoint, receiver_endpoint, node_id)
    # Connect to the device
    remote = connect(device.device, number_of_chips, samna_node, sender_endpoint, receiver_endpoint, node_id, interpreter_id)
    # Get board object
    board = dynapse2board(opts=device, args=bitfiles, remote=remote)

    # Custom examples
    if experiment == 0:
        comparator.main(board=board, profile_path=os.getcwd() + "/profiles/" + profileName, number_of_chips=number_of_chips)
    elif experiment == 1:
        wta_shifted_4joints.main(board=board, profile_path=os.getcwd() + "/profiles/" + profileName, number_of_chips=number_of_chips)
    elif experiment == 2:
        robot_control_separate_inputs.main(board=board, profile_path=os.getcwd() + "/profiles/" + profileName, number_of_chips=number_of_chips)



if __name__ == '__main__':
    main()
