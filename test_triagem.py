import unittest

from modelos import Paciente, PacientePreferencia, Riscos
from triagem import Triagem


def classificador_falso(sintomas, idade=None):
    # simula a IA sem usar a internet
    if "peito" in sintomas:
        return Riscos.Vermelho, "teste"
    if "febre" in sintomas:
        return Riscos.Amarelo, "teste"
    return Riscos.Verde, "teste"


class TestTriagem(unittest.TestCase):
    def setUp(self):
        self.triagem = Triagem(classificador=classificador_falso)

    def test_gravidade_vence_ordem_de_chegada(self):
        self.triagem.receber(Paciente("Ana", 30, "coriza"))
        self.triagem.receber(Paciente("Bia", 40, "febre alta"))
        self.triagem.receber(Paciente("Caio", 50, "dor no peito"))
        nomes = [self.triagem.chamar_proximo().nome for _ in range(3)]
        self.assertEqual(nomes, ["Caio", "Bia", "Ana"])

    def test_preferencial_vence_no_mesmo_risco(self):
        self.triagem.receber(Paciente("Ana", 30, "coriza"))
        self.triagem.receber(PacientePreferencia("Rui", 70, "coriza", "idoso"))
        self.assertEqual(self.triagem.chamar_proximo().nome, "Rui")

    def test_preferencial_nao_fura_risco_maior(self):
        self.triagem.receber(PacientePreferencia("Rui", 70, "coriza", "idoso"))
        self.triagem.receber(Paciente("Caio", 50, "dor no peito"))
        self.assertEqual(self.triagem.chamar_proximo().nome, "Caio")

    def test_empate_total_segue_ordem_de_chegada(self):
        self.triagem.receber(Paciente("Ana", 30, "coriza"))
        self.triagem.receber(Paciente("Bia", 31, "coriza"))
        self.assertEqual(self.triagem.chamar_proximo().nome, "Ana")

    def test_fila_vazia(self):
        self.assertIsNone(self.triagem.chamar_proximo())


if __name__ == "__main__":
    unittest.main()
