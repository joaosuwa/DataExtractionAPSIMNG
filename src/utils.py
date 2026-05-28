import re


class FieldReader:
    """
    Lê expressões de variáveis APSIM de um arquivo de texto e fornece
    chaves normalizadas para uso no CSV.

    Exemplo de fields.txt:
        [Clock].Today.Day
        [Soil].Water.PAW
    """

    def __init__(self, path: str) -> None:
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

    @staticmethod
    def to_key(var: str) -> str:
        """
        Converte uma expressão APSIM em uma chave compatível com CSV.

        Exemplos:
            [Clock].Today.Day  ->  clock_today_day
            [Soil].Water.PAW   ->  soil_water_paw
        """
        s = re.sub(r"[\[\]]", "", var) 
        s = re.sub(r"[^a-zA-Z0-9]+", "_", s) 
        return s.strip("_").lower()

    def __repr__(self) -> str:
        return f"FieldReader({self.path!r}, {len(self.variables)} variáveis)"