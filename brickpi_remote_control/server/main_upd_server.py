import socket
from brickpi_remote_control import utils

HOST = "localhost"
BUFFERSIZE = 1024


def listen_for_data(server, move_cmd):
    # Listen for incoming datagram

    data = []
    while True:
        data.extend(server.recv(BUFFERSIZE))
        # print("recv{}".format(data))

        frame = find_frame(data)
        if frame:
            move_cmd.write(frame[0], frame[1])


def find_frame(data):
    frame = None
    sub_data = []
    idx_last_flag = None
    for idx, item in enumerate(reversed(data)):
        if item == utils.END_FLAG:
            if not idx_last_flag:
                idx_last_flag = len(data) - 1 - idx
            if len(sub_data) == utils.FRAME_LENGTH:
                frame = sub_data[::-1]
                break
            sub_data = []
        else:
            sub_data.append(item)

    if idx_last_flag:
        del data[:idx_last_flag]

    return frame


def start_server_and_listen():
    # Create a datagram socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as MyUDPServerSocket:

        # Bind to address and ip
        MyUDPServerSocket.bind((HOST, utils.PORT))

        print("UDP server up and listening")

        move_cmd = utils.MoveCmd()
        listen_for_data(MyUDPServerSocket, move_cmd)


if __name__ == "__main__":
    start_server_and_listen()

