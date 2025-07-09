from dataclasses import dataclass

@dataclass
class Edge:
    prod1: int
    prod2: int
    peso: int

    def __str__(self):
        return f"I prodotti {self.prod1} e {self.prod2} sono collegati con peso {self.peso}"