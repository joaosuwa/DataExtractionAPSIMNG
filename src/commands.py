import zmq
import msgpack
from summary import SummaryCollector
from utils import FieldReader


def send_command(socket, command, args=None):
    socket.send_string(command, zmq.SNDMORE if args else 0)
    if args:
        for i, arg in enumerate(args):
            socket.send(msgpack.packb(arg), zmq.SNDMORE if i < len(args) - 1 else 0)


def _fetch_row(socket, field_reader: FieldReader) -> dict:
    """
    Busca todas as variáveis definidas em `field_reader` via ZMQ e
    retorna um dicionário plano.
    """
    row: dict = {}
    for var in field_reader.variables:
        send_command(socket, "get", [var])
        value = msgpack.unpackb(socket.recv())
        key = field_reader.to_key(var)

        if isinstance(value, list):
            for i, v in enumerate(value):
                row[f"{key}_{i}"] = v
        else:
            row[key] = value

    return row


def poll_zmq2(socket, field_reader: FieldReader, output_path: str) -> None:
    """
    Faz o polling do socket ZMQ.

    Na primeira pausa, determina automaticamente as colunas do CSV a
    partir dos tipos retornados pelo APSIM e inicializa o
    `SummaryCollector`. Nas pausas seguintes, apenas registra os dados.

    Args:
        socket:       Socket ZMQ já conectado.
        field_reader: Instância de `FieldReader` com as variáveis a coletar.
        output_path:  Caminho do arquivo CSV de saída.
    """
    collector: SummaryCollector | None = None

    try:
        while True:
            msg = socket.recv_string()

            if msg == "connect":
                send_command(socket, "ok")

            elif msg == "paused":
                row = _fetch_row(socket, field_reader)

                # Inicialização lazy: colunas só são conhecidas após o
                # primeiro fetch (listas têm tamanho variável).
                if collector is None:
                    collector = SummaryCollector(
                        output_path=output_path,
                        fields=list(row.keys()),
                    )

                collector.record(**row)
                send_command(socket, "resume")

            elif msg == "finished":
                send_command(socket, "ok")
                break

    finally:
        if collector is not None:
            collector.close()