from estruturas import FilaPrioridade
from ia import classificar


class Triagem:
    """Recebe pacientes, classifica o risco com a IA e controla a fila de atendimento.

    Ordem de atendimento: Vermelho > Amarelo > Verde. Dentro do mesmo risco,
    pacientes preferenciais vêm antes; persistindo o empate, vale a ordem de chegada.
    """

    def __init__(self, banco=None, classificador=classificar):
        self._fila = FilaPrioridade()
        self._banco = banco                  # opcional: o programa roda sem banco
        self._classificador = classificador  # injetado para poder testar sem a API
        self._proximo_id = 1                 # usado só quando não há banco

    def receber(self, paciente):
        risco, motivo = self._classificador(paciente.sintomas, paciente.idade)
        paciente.riscos = risco
        paciente.motivos = motivo

        if self._banco is not None:
            paciente.id = self._banco.salvar_paciente(paciente)
        else:
            paciente.id = self._proximo_id
            self._proximo_id += 1

        # int(risco) = 1, 2 ou 3 (IntEnum); desempate = 0 preferencial, 1 comum
        self._fila.inserir(paciente, int(paciente.riscos), paciente.desempate)
        return paciente

    def chamar_proximo(self, medico=None):
        paciente = self._fila.remover()
        if paciente is not None and self._banco is not None:
            self._banco.registrar_atendimento(paciente, medico)
        return paciente

    def mostrar_fila(self):
        if self._fila.vazia():
            print("Fila vazia")
            return
        for posicao, p in enumerate(self._fila.em_ordem(), start=1):
            print(f"{posicao}. [{p.riscos.name}] {p.nome} ({p.idade} anos) - {p.tipo}")
            print(f"   Motivo: {p.motivos}")

    def __len__(self):
        return len(self._fila)
