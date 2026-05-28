import zmq
import msgpack


def send_command(socket, command, args=None):
    socket.send_string(command, zmq.SNDMORE if args else 0)
    if args:
        for i, arg in enumerate(args):
            socket.send(msgpack.packb(arg), zmq.SNDMORE if i < len(args) - 1 else 0)

def poll_zmq2(socket):
    while True:
        msg = socket.recv_string()
        if msg == "connect":
            send_command(socket, "ok")
        elif msg == "paused":
            send_command(socket, "get", ["[Clock].Today.Day"])
            reply = msgpack.unpackb(socket.recv())
            assert isinstance(reply, int)
            print("Day:", reply)

            send_command(socket, "get", ["[Soil].Water.PAW"])
            reply = msgpack.unpackb(socket.recv())
            assert isinstance(reply, list) and len(reply) == 7
            print("PAW:", reply)
            
            send_command(socket, "resume")
        elif msg == "finished":
            send_command(socket, "ok")
            break