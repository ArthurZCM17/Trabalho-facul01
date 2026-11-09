from modelos import Paciente, PacientePreferencia
from triagem import Triagem

def main():
    triagem = Triagem()
    while True:
        print("\n==== TRIAGEM ====")
        print("1 - Cadastrar paciente")
        print("2 - Chamar próximo")
        print("3 - Ver fila")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Nome: ")
            idade = input("Idade: ").strip()
            if not idade.isdigit():
                print("Idade inválida")
                continue
            sintomas = input("Sintomas: ")
            pref = input("Tem preferência? (s/n): ").strip().lower()

            try:
                if pref == "s":
                    print("Motivos: IDOSO, PCD, CRIANÇA DE COLO")
                    motivo = input("Motivo: ")
                    paciente = PacientePreferencia(nome, int(idade), sintomas, motivo)
                else:
                    paciente = Paciente(nome, int(idade), sintomas)
            except ValueError as erro:
                print("Erro:", erro)
                continue

            triagem.receber(paciente)
            print(f"{paciente.nome} cadastrado - risco {paciente.riscos.name} (id {paciente.id})")

        elif opcao == "2":
            paciente = triagem.chamar_proximo()
            if paciente is None:
                print("Ninguém na fila")
            else:
                print(f"Chamando: {paciente.nome} ({paciente.riscos.name})")

        elif opcao == "3":
            triagem.mostrar_fila()

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
