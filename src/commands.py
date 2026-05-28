import zmq
import msgpack
from summary import SummaryCollector


def send_command(socket, command, args=None):
    socket.send_string(command, zmq.SNDMORE if args else 0)
    if args:
        for i, arg in enumerate(args):
            socket.send(msgpack.packb(arg), zmq.SNDMORE if i < len(args) - 1 else 0)


def poll_zmq2(socket, collector: SummaryCollector | None = None):
    """
    Faz o polling do socket ZMQ.

    Se um `SummaryCollector` for fornecido, registra os dados de cada
    iteração (pausa) no arquivo de saída ao final de cada ciclo.
    """
    while True:
        msg = socket.recv_string()

        if msg == "connect":
            send_command(socket, "ok")

        elif msg == "paused":
            send_command(socket, "get", ["[Clock].Today.Day"])
            day: int = msgpack.unpackb(socket.recv())
            assert isinstance(day, int)
            print("Day:", day)

            send_command(socket, "get", ["[Soil].Water.PAW"])
            paw: list = msgpack.unpackb(socket.recv())
            assert isinstance(paw, list) and len(paw) == 7
            print("PAW:", paw)

            # ── persiste ao final de cada pausa ──────────────────────────
            if collector is not None:
                collector.record(
                    day=day,
                    paw_0=paw[0], paw_1=paw[1], paw_2=paw[2],
                    paw_3=paw[3], paw_4=paw[4], paw_5=paw[5], paw_6=paw[6],
                )
            # ─────────────────────────────────────────────────────────────

            send_command(socket, "resume")

        elif msg == "finished":
            send_command(socket, "ok")
            break