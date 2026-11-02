
from datetime import datetime
from enum import IntEnum

class Riscos(IntEnum):
    Vermelho = 1 #emergência
    Amarelo = 2 #normal
    Verde = 3 #sem riscos

    @classmethod
    def from_texto(cls,texto: str) -> "Riscos":
        return cls[texto.strip().upper()]

class Paciente:

    def __init__(self,nome,idade,sintomas,id=None,chegada=None):
        self.nome = nome
        self.idade = idade
        self.sintomas = sintomas
        self.__id = id
        self.__chegada = chegada or datetime.now()
        self.__riscos = None
        self.__motivos = ""

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self,valor):
        if not valor or not valor.strip():
            raise ValueError("Nome precisa ser preenchido")
        self.__nome = valor.strip()

    @property
    def idade(self):
        return self.__idade
    @idade.setter
    def idade(self,valor):
        if not isinstance(valor,int) or not 0<= valor <= 120:
            raise ValueError("Idade inválida")
        self.__idade = valor

    @property
    def sintomas(self):
        return self.__sintomas
    @sintomas.setter
    def sintomas(self,valor):
        if not valor or not valor.strip():
            raise ValueError("Informe os sintomas do paciente")
        self.__sintomas = valor.strip()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def chegada(self):
        return self.__chegada

    @property
    def riscos(self):
        return self.__riscos
    @riscos.setter
    def riscos(self,valor:Riscos):
        if not isinstance(valor,Riscos):
            raise TypeError("riscos devem ser do tipo riscos")
        self.__riscos = valor

    @property
    def motivos(self):
        return self.__motivos
    @motivos.setter
    def motivos(self,valor):
        self.__motivos = valor or ""

    @property
    def tipo(self):
        return "COMUM"

    @property
    def motivo_preferencial(self):
        return None

    @property
    def desempate(self):
        return 1

    def __str__(self):
        r = self.risco.name if self.risco else "N/A"
        return f"[{r}] {self.nome} ({self.idade} anos) - {self.tipo}"

class PacientePreferencia(Paciente):

    MOTIVOS = ("IDOSO","Gestante","PCD","CRIANÇA DE COLO")
    def __init__(self, nome, idade, sintomas, motivo, id=None, chegada=None):
        super().__init__(nome, idade, sintomas, id, chegada)
        motivo = motivo.strip().upper()
        if motivo not in self.MOTIVOS:
            raise ValueError("Motivo não reconhecido")
        self.__motivo = motivo

    @property
    def tipo(self):
        return "Preferência"

    @property
    def motivo_preferencial(self):
        return self.__motivo

    @property
    def desempate(self):
        return 0

class Medico:
    def __init__(self, nome, numero,especialidade="Clínico Geral"):
       self.__nome = nome
       self.__numero = numero
       self.__especialidade = especialidade

    @property
    def nome(self):
        return self.__nome

    @property
    def numero(self):
        return self.__número

    @property
    def especialidade(self):
        return self.__especialidade

    def __str__(self):
        return f"Dr(a). {self.nome} (numero {self.numero} {self.especialidade})"
