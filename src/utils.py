from functools import singledispatchmethod
import re
import pandas as pd
import csv
from typing import List, Dict, Any


class FieldReader:
    """
    Lê expressões de variáveis APSIM de um arquivo de texto e fornece
    chaves normalizadas para uso no CSV.

    Exemplo de fields.txt:
        [Clock].Today.Day
        [Soil].Water.PAW
    """

    def __init__(self, path: str):
        self.path = path
        self.variables: list[str] = self._load(path)

    @staticmethod
    def _load(path: str) -> list[str]:
        variables: list[str] = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    variables.append(line)
        return variables

    def __repr__(self) -> str:
        return f"FieldReader({self.path!r}, {len(self.variables)} variáveis)"

class CSVReader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.df = pd.read_csv(path)

    def get_headers(self) -> List[str]:
        return self.df.columns.tolist()
    
    def get_rows(self) -> List[List[Any]]:
        return self.df.values.tolist()

    @singledispatchmethod
    def get_columns_data(self, columns):
        raise TypeError("O parâmetro 'columns' deve ser uma string ou uma lista.")

    @get_columns_data.register
    def _(self, columns: str) -> List[Any]:
        return self.df[columns].tolist()

    @get_columns_data.register
    def _(self, columns: list) -> Dict[str, List[Any]]:
        return self.df[columns].to_dict(orient='list')