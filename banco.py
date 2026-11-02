import sqlite3
from datetime import datetime

from modelos import Paciente, PacientePreferencia, Riscos


TABELA_PACIENTES = """
                   CREATE TABLE IF NOT EXISTS pacientes \
                   ( \
                       id \
                       INTEGER \
                       PRIMARY \
                       KEY \
                       AUTOINCREMENT, -- número do paciente (automático) \
                       nome \
                       TEXT \
                       NOT \
                       NULL, \
                       idade \
                       INTEGER \
                       NOT \
                       NULL, \
                       tipo \
                       TEXT \
                       NOT \
                       NULL,          -- COMUM ou PREFERENCIAL \
                       motivo_pref \
                       TEXT,          -- idoso, gestante... (pode ficar vazio) \
                       sintomas \
                       TEXT \
                       NOT \
                       NULL, \
                       risco \
                       TEXT \
                       NOT \
                       NULL,          -- VERMELHO, AMARELO ou VERDE \
                       justificativa \
                       TEXT,          -- por que a IA escolheu esse risco \
                       chegada \
                       TEXT \
                       NOT \
                       NULL, \
                       status \
                       TEXT \
                       NOT \
                       NULL \
                       DEFAULT \
                       'AGUARDANDO'
                   ) \
                   """

TABELA_ATENDIMENTOS = """
                      CREATE TABLE IF NOT EXISTS atendimentos \
                      ( \
                          id \
                          INTEGER \
                          PRIMARY \
                          KEY \
                          AUTOINCREMENT, \
                          paciente_id \
                          INTEGER \
                          NOT \
                          NULL \
                          REFERENCES \
                          pacientes \
                      ( \
                          id \
                      ), -- quem foi atendido
                          medico_nome TEXT NOT NULL,
                          medico_crm TEXT NOT NULL,
                          inicio TEXT NOT NULL,
                          espera_min REAL, -- minutos que o paciente esperou
                          observacoes TEXT
                          ) \
                      """


class Banco:
    def __init__(self, caminho="triagem.db"):
        self.conexao = sqlite3.connect(caminho)
        self.conexao.row_factory = sqlite3.Row


        self.conexao.execute(TABELA_PACIENTES)
        self.conexao.execute(TABELA_ATENDIMENTOS)
        self.conexao.commit()


    def salvar_paciente(self, paciente):

        resultado = self.conexao.execute(
            """
            INSERT INTO pacientes
            (nome, idade, tipo, motivo_pref, sintomas, risco, justificativa, chegada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                paciente.nome,
                paciente.idade,
                paciente.tipo,
                paciente.motivo_preferencial,
                paciente.sintomas,
                paciente.risco.name,
                paciente.justificativa,
                paciente.chegada.isoformat(),
            ),
        )
        self.conexao.commit()


        paciente.id = resultado.lastrowid
        return paciente.id

    def registrar_atendimento(self, paciente, medico, observacoes=""):

        agora = datetime.now()
        minutos_de_espera = (agora - paciente.chegada).total_seconds() / 60

        self.conexao.execute(
            """
            INSERT INTO atendimentos
                (paciente_id, medico_nome, medico_crm, inicio, espera_min, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                paciente.id,
                medico.nome,
                medico.crm,
                agora.isoformat(),
                round(minutos_de_espera, 2),
                observacoes,
            ),
        )
        self.conexao.execute(
            "UPDATE pacientes SET status = 'ATENDIDO' WHERE id = ?",
            (paciente.id,),
        )
        self.conexao.commit()


    def carregar_aguardando(self):

        linhas = self.conexao.execute(
            "SELECT * FROM pacientes WHERE status = 'AGUARDANDO'"
        ).fetchall()

        return [self._linha_para_paciente(linha) for linha in linhas]

    def historico_pacientes(self):

        return self.conexao.execute(
            "SELECT * FROM pacientes ORDER BY id DESC"
        ).fetchall()

    def historico_atendimentos(self):

        return self.conexao.execute(
            """
            SELECT a.id, p.nome, p.risco, a.medico_nome, a.inicio, a.espera_min
            FROM atendimentos AS a
                     JOIN pacientes AS p ON p.id = a.paciente_id
            ORDER BY a.id DESC
            """
        ).fetchall()

    def _linha_para_paciente(self, linha):

        dados_extras = {
            "id": linha["id"],
            "chegada": datetime.fromisoformat(linha["chegada"]),
        }

        if linha["tipo"] == "PREFERENCIAL":
            paciente = PacientePreferencia(
                linha["nome"], linha["idade"], linha["sintomas"],
                linha["motivo_pref"], **dados_extras,
            )
        else:
            paciente = Paciente(
                linha["nome"], linha["idade"], linha["sintomas"], **dados_extras,
            )

        paciente.risco = Riscos.from_texto(linha["risco"])
        paciente.justificativa = linha["justificativa"]
        return paciente
