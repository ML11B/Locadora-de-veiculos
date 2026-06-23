import sys
import os

# Garante que imports funcionem ao rodar main.py diretamente
sys.path.insert(0, os.path.dirname(__file__))

from database.conexao import ConexaoBD
from database.repo_categoria import RepositorioCategoria
from database.repo_veiculo import RepositorioVeiculo
from database.repo_contrato import RepositorioContrato
from models.categoria import CategoriaEconomica, CategoriaExecutiva
from models.veiculo import Veiculo
from models.locadora import Locadora


def imprimir_detalhes(contrato):
    """Método polimórfico: exibe categoria, veículo e valor total."""
    print(f"[LOG] Categoria : {contrato.veiculo.categoria}")
    print(f"[LOG] Veículo   : {contrato.veiculo}")
    print(f"[LOG] Valor     : R$ {contrato.valor_total:.2f}")


def menu():
    ConexaoBD().conectar()  # inicializa banco e tabelas
    locadora = Locadora("Locadora Central")
    repo_cat = RepositorioCategoria()
    repo_contrato = RepositorioContrato()

    while True:
        print("\n========== LOCADORA DE VEÍCULOS ==========")
        print("1. Cadastrar categoria")
        print("2. Listar categorias")
        print("3. Cadastrar veículo")
        print("4. Listar veículos")
        print("5. Realizar locação")
        print("6. Listar contratos")
        print("7. Excluir veículo")
        print("8. Excluir categoria")
        print("0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Nome da categoria: ")
            diaria = float(input("Valor da diária (R$): "))
            tipo = input("Tipo (1=Econômica / 2=Executiva): ")
            if tipo == "1":
                franquia = int(input("Franquia de KM por dia: "))
                cat = CategoriaEconomica(nome=nome, diaria=diaria, franquia_km_diaria=franquia)
            else:
                seguro = input("Seguro incluso? (s/n): ").lower() == "s"
                cat = CategoriaExecutiva(nome=nome, diaria=diaria, seguro_incluso=seguro)
            repo_cat.inserir(cat)
            print(f"Categoria cadastrada com ID {cat.id}.")

        elif opcao == "2":
            cats = repo_cat.listar()
            if not cats:
                print("Nenhuma categoria cadastrada.")
            for c in cats:
                print(f"  [{c.id}] {c}")

        elif opcao == "3":
            modelo = input("Modelo do veículo: ")
            placa = input("Placa: ")
            cats = repo_cat.listar()
            if not cats:
                print("Cadastre uma categoria primeiro.")
                continue
            print("Categorias disponíveis:")
            for c in cats:
                print(f"  [{c.id}] {c}")
            cat_id = int(input("ID da categoria: "))
            cat = repo_cat.buscar(cat_id)
            if not cat:
                print("Categoria não encontrada.")
                continue
            v = Veiculo(modelo=modelo, placa=placa, categoria=cat)
            locadora.adicionar_veiculo(v)
            print(f"Veículo cadastrado com ID {v.id}.")

        elif opcao == "4":
            veiculos = locadora.listar_veiculos()
            if not veiculos:
                print("Nenhum veículo cadastrado.")
            for v in veiculos:
                print(f"  [{v.id}] {v} — {v.categoria}")

        elif opcao == "5":
            veiculos = locadora.listar_veiculos()
            if not veiculos:
                print("Nenhum veículo cadastrado.")
                continue
            for v in veiculos:
                print(f"  [{v.id}] {v}")
            vid = int(input("ID do veículo: "))
            repo_v = RepositorioVeiculo()
            veiculo = repo_v.buscar(vid)
            if not veiculo:
                print("Veículo não encontrado.")
                continue
            try:
                dias = int(input("Dias de locação: "))
                km = int(input("KM rodados: "))
                contrato = veiculo.realizar_locacao(dias, km)
                repo_contrato.inserir(contrato)
                print("\n" + contrato.exibir_resumo())
                imprimir_detalhes(contrato)
            except (ValueError, Exception) as e:
                print(f"Erro: {e}")

        elif opcao == "6":
            contratos = repo_contrato.listar()
            if not contratos:
                print("Nenhum contrato registrado.")
            for c in contratos:
                print(c.exibir_resumo())

        elif opcao == "7":
            repo_v = RepositorioVeiculo()
            veiculos = locadora.listar_veiculos()
            for v in veiculos:
                print(f"  [{v.id}] {v}")
            vid = int(input("ID do veículo a excluir: "))
            try:
                repo_v.excluir(vid)
                print("Veículo removido.")
            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "8":
            cats = repo_cat.listar()
            for c in cats:
                print(f"  [{c.id}] {c}")
            cid = int(input("ID da categoria a excluir: "))
            try:
                repo_cat.excluir(cid)
                print("Categoria removida.")
            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
