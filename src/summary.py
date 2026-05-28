import csv
import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SummaryCollector:
    """
    Acumula dados de cada iteração da simulação e persiste
    incrementalmente em um arquivo CSV ao final de cada pausa.
    """
    output_path: str
    fields: list[str]
    _iteration: int = field(default=0, init=False, repr=False)
    _file: Any = field(default=None, init=False, repr=False)
    _writer: Any = field(default=None, init=False, repr=False)

    def __post_init__(self):
        os.makedirs(os.path.dirname(self.output_path) or ".", exist_ok=True)
        self._file = open(self.output_path, "w", newline="", buffering=1)  # line-buffered
        self._writer = csv.DictWriter(self._file, fieldnames=["iteration"] + self.fields)
        self._writer.writeheader()
        self._file.flush()

    def record(self, **kwargs) -> None:
        """Registra uma linha com os dados da iteração atual e faz flush imediato."""
        self._iteration += 1
        row = {"iteration": self._iteration, **kwargs}
        missing = set(self.fields) - set(kwargs)
        if missing:
            raise ValueError(f"Campos obrigatórios ausentes: {missing}")
        self._writer.writerow(row)
        self._file.flush()  # garante escrita mesmo em crash

    def close(self) -> None:
        if self._file and not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()