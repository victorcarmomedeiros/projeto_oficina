from datetime import date, timedelta

from clientes import ControleClientes
from atendimento import Atendimento
from arvore import construir_arvore, exibir_arvore, marcar_defeito, listar_pecas_com_defeito
from estoque import Estoque
from ordem_servico import ControleOS
from pagamento import Caixa

SENHA_ADMIN = "admin123"

clientes = ControleClientes()
atendimento = Atendimento(2)  
estoque = Estoque()
controle_os = ControleOS()
caixa = Caixa()


def ler(msg):
    return input(msg).strip()


def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número.")


def ler_float(msg):
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("Digite um valor válido.")


def ler_validade():
    while True:
        texto = ler("Validade (AAAA-MM-DD ou Enter se não tem): ")
        if texto == "":
            return None
        try:
            return date.fromisoformat(texto)
        except ValueError:
            print("Formato inválido.")


def menu(texto):
    print(texto)
    return ler_int("Opção: ")


def mostrar_cliente(cliente):
    print(cliente.nome, "| CPF", cliente.cpf, "| Tel", cliente.telefone)
    for v in cliente.veiculos:
        print("    -", v.placa, v.marca, v.modelo, v.ano)


def mostrar_os(ordem):
    print("\nOS", ordem.numero, "|", ordem.placa, "|", ordem.cliente, "| mecânico:", ordem.mecanico)
    for p in ordem.pecas:
        print("   ", p.quantidade, "x", p.nome, "[" + p.codigo + "] R$", p.preco_unitario)
    for s in ordem.servicos:
        print("    Serviço:", s.descricao, "R$", s.valor)
    print("Peças R$", ordem.valor_pecas(), "| Mão de obra R$", ordem.valor_mao_obra(),
          "| TOTAL R$", ordem.total())
    print("Remontagem concluída:", "sim" if ordem.remontagem_concluida else "não")


def escolher_os():
    if controle_os.abertas.tamanho == 0:
        print("Nenhuma OS aberta.")
        return None
    for o in controle_os.abertas:
        print("OS", o.numero, "|", o.placa, "|", o.cliente)
    ordem = controle_os.buscar(ler_int("Número da OS: "))
    if ordem is None:
        print("OS não encontrada.")
    return ordem


def iniciar_atendimento(chegada):
    """Veículo entrou no box: abre a OS e cria a árvore de diagnóstico dele."""
    print("\nPróximo veículo:", chegada.placa, "-", chegada.cliente, "| Queixa:", chegada.queixa)
    ordem = controle_os.abrir(chegada.placa, chegada.cliente, ler("Mecânico responsável: "))
    ordem.arvore = construir_arvore()
    print("OS", ordem.numero, "aberta.")


def area_cliente():
    cpf = ler("Seu CPF: ")
    cliente = clientes.buscar_por_cpf(cpf)
    if cliente is None:
        print("CPF não cadastrado. Vamos fazer o seu cadastro.")
        cliente = clientes.cadastrar_cliente(ler("Nome: "), cpf, ler("Telefone: "))
    print("Olá,", cliente.nome)

    while True:
        op = menu("""
--- ÁREA DO CLIENTE ---
1 - Cadastrar um veículo
2 - Ver meus veículos
3 - Levar um veículo à oficina
4 - Acompanhar meu veículo
0 - Voltar""")
        if op == 0:
            return
        if op == 1:
            placa = ler("Placa: ").upper()
            veiculo = clientes.cadastrar_veiculo(cpf, placa, ler("Modelo: "), ler("Marca: "), ler_int("Ano: "))
            print("Placa já cadastrada." if veiculo is None else "Veículo cadastrado.")
        elif op == 2:
            mostrar_cliente(cliente)
        elif op in (3, 4):
            placa = ler("Placa: ").upper()
            dono, veiculo = clientes.buscar_por_placa(placa)
            if dono is None or dono.cpf != cpf:
                print("Esse veículo não está cadastrado no seu nome.")
            elif op == 3:
                queixa = ler("Qual o problema? ")
                guincho = ler("Veio de guincho? (s/n): ").lower() == "s"
                atendimento.registrar_chegada(placa, cliente.nome, queixa, guincho)
                print("Veículo na fila de espera. Posição:", atendimento.posicao(placa))
            else:
                ordem = controle_os.abertas.buscar(lambda o: o.placa == placa)
                posicao = atendimento.posicao(placa)
                if ordem is not None:
                    mostrar_os(ordem)
                elif posicao is not None:
                    print("Seu veículo está na fila. Posição:", posicao)
                else:
                    print("Seu veículo não está na oficina no momento.")


def admin_clientes():
    while True:
        op = menu("""
--- CLIENTES E VEÍCULOS ---
1 - Listar todos
2 - Buscar por CPF
3 - Buscar por placa
4 - Remover cliente
5 - Remover veículo
0 - Voltar""")
        if op == 0:
            return
        if op == 1:
            for c in clientes.clientes:
                mostrar_cliente(c)
        elif op == 2:
            c = clientes.buscar_por_cpf(ler("CPF: "))
            if c is None:
                print("Não encontrado.")
            else:
                mostrar_cliente(c)
        elif op == 3:
            c, v = clientes.buscar_por_placa(ler("Placa: ").upper())
            if c is None:
                print("Não encontrado.")
            else:
                print("Veículo", v.placa, v.marca, v.modelo, v.ano, "| Dono:", c.nome, "| CPF", c.cpf)
        elif op == 4:
            achou = clientes.remover_cliente(ler("CPF: "))
            print("Não encontrado." if achou is None else "Cliente removido.")
        elif op == 5:
            achou = clientes.remover_veiculo(ler("Placa: ").upper())
            print("Não encontrado." if achou is None else "Veículo removido.")


def admin_atendimento():
    while True:
        op = menu("""
--- ATENDIMENTO ---
1 - Ver filas e boxes
2 - Chamar próximo veículo
0 - Voltar""")
        if op == 0:
            return
        if op == 1:
            print("Boxes livres:", atendimento.boxes_livres)
            print("Fila do guincho:")
            for c in atendimento.fila_guincho:
                print("   ", c.placa, c.cliente, c.data_hora.strftime("%d/%m %H:%M"), "|", c.queixa)
            print("Fila normal:")
            for c in atendimento.fila_normal:
                print("   ", c.placa, c.cliente, c.data_hora.strftime("%d/%m %H:%M"), "|", c.queixa)
        elif op == 2:
            if atendimento.boxes_livres == 0:
                print("Nenhum box livre.")
                continue
            chegada = atendimento.chamar_proximo()
            if chegada is None:
                print("Nenhum veículo esperando.")
            else:
                iniciar_atendimento(chegada)


def admin_diagnostico():
    ordem = escolher_os()
    if ordem is None:
        return
    while True:
        op = menu("""
--- DIAGNÓSTICO ---
1 - Exibir árvore de componentes
2 - Marcar componente com defeito
3 - Listar peças com defeito
0 - Voltar""")
        if op == 0:
            return
        if op == 1:
            exibir_arvore(ordem.arvore)
        elif op == 2:
            ok = marcar_defeito(ordem.arvore, ler("Nome do componente: "))
            print("Marcado." if ok else "Componente não encontrado.")
        elif op == 3:
            for comp in listar_pecas_com_defeito(ordem.arvore):
                print(" -", comp.nome, "[" + comp.codigo + "]")


def admin_estoque():
    while True:
        op = menu("""
--- ESTOQUE ---
1 - Cadastrar produto
2 - Registrar compra (novo lote)
3 - Ver estoque e lotes
4 - Descartar lotes vencidos
5 - Ajustar quantidade de um lote
6 - Ver alertas de estoque mínimo
0 - Voltar""")
        if op == 0:
            return
        if op == 1:
            estoque.cadastrar_produto(ler("Nome: "), ler("Código: "), ler_float("Preço de venda: "),
                                      ler_int("Quantidade mínima: "))
            print("Produto cadastrado.")
        elif op == 2:
            codigo = ler("Código do produto: ")
            lote = estoque.comprar(codigo, ler("Fornecedor: "), ler_float("Preço de compra: "),
                                   date.today(), ler_validade(), ler_int("Quantidade: "))
            print("Produto não encontrado." if lote is None else "Lote registrado.")
        elif op == 3:
            for p in estoque.produtos:
                print(p.codigo, "|", p.nome, "| total:", p.total(), "| mínimo:", p.minimo)
                for lote in p.lotes:  # do mais antigo para o mais novo
                    print("    lote", lote.numero, "| compra R$", lote.preco_compra, "em", lote.data_compra,
                          "| validade:", lote.validade, "| qtd:", lote.quantidade)
        elif op == 4:
            estoque.descartar_vencidos(date.today())
            for perda in estoque.perdas:
                print("PERDA:", perda.produto.nome, "| lote", perda.lote.numero, "| qtd", perda.lote.quantidade)
        elif op == 5:
            ok = estoque.ajustar_lote(ler("Código do produto: "), ler_int("Número do lote: "),
                                      ler_int("Nova quantidade: "))
            print("Ajustado." if ok else "Produto ou lote não encontrado.")
        elif op == 6:
            for p in estoque.alertas_minimo():
                print("ALERTA:", p.nome, "abaixo do mínimo (", p.total(), "<", p.minimo, ")")


def admin_os():
    while True:
        op = menu("""
--- ORDEM DE SERVIÇO ---
1 - Ver uma OS
2 - Adicionar peça
3 - Remover peça
4 - Adicionar serviço (mão de obra)
5 - Remover serviço
6 - Marcar remontagem como concluída
0 - Voltar""")
        if op == 0:
            return
        ordem = escolher_os()
        if ordem is None:
            continue
        if op == 1:
            mostrar_os(ordem)
        elif op == 2:
            produto = estoque.buscar(ler("Código da peça/fluido: "))
            if produto is None:
                print("Produto não encontrado.")
            elif ordem.adicionar_peca(produto, ler_int("Quantidade: ")):
                print("Peça adicionada (a baixa no estoque é feita no fechamento).")
            else:
                print("Estoque insuficiente. Disponível:", produto.total())
        elif op == 3:
            achou = ordem.remover_peca(ler("Código da peça: "))
            print("Peça não está na OS." if achou is None else "Peça removida.")
        elif op == 4:
            ordem.adicionar_servico(ler("Descrição do serviço: "), ler_float("Valor R$: "))
            print("Serviço adicionado.")
        elif op == 5:
            achou = ordem.remover_servico(ler("Descrição do serviço: "))
            print("Serviço não está na OS." if achou is None else "Serviço removido.")
        elif op == 6:
            ordem.remontagem_concluida = True
            print("Remontagem concluída.")


def fechar_e_pagar():
    ordem = escolher_os()
    if ordem is None:
        return
    mostrar_os(ordem)
    op = ler_int("Pagamento: 1 - PIX | 2 - Cartão | 3 - Dinheiro: ")
    parcelas = 1
    if op == 1:
        forma = "PIX"
    elif op == 2:
        forma = "CARTAO"
        parcelas = ler_int("Parcelas (1 = à vista): ")
    elif op == 3:
        forma = "DINHEIRO"
    else:
        print("Opção inválida.")
        return
    try:
        pagamento = caixa.fechar_os(ordem, estoque, forma, parcelas)
    except ValueError as erro:
        print("Não foi possível fechar:", erro)
        return
    controle_os.remover(ordem.numero)
    print("Pagamento registrado: R$", pagamento.total)
    for p in estoque.alertas_minimo():
        print("ALERTA:", p.nome, "abaixo do mínimo (", p.total(), "<", p.minimo, ")")
    proximo = atendimento.liberar_box()  
    if proximo is None:
        print("Box liberado. Nenhum veículo esperando.")
    else:
        iniciar_atendimento(proximo)


def admin_pagamento():
    while True:
        op = menu("""
--- PAGAMENTO ---
1 - Fechar OS e registrar pagamento
2 - Listar pagamentos
3 - Peças consumidas por cliente/veículo
0 - Voltar""")
        if op == 0:
            return
        if op == 1:
            fechar_e_pagar()
        elif op == 2:
            for p in caixa.pagamentos:
                print("OS", p.numero_os, "|", p.pagador, "|", p.forma, p.parcelas, "x | peças R$",
                      p.valor_pecas, "| mão de obra R$", p.valor_mao_obra, "| total R$", p.total,
                      "|", p.data_hora.strftime("%d/%m/%Y %H:%M"))
        elif op == 3:
            for c in caixa.consumos:
                print(c.cliente, "|", c.placa, "| OS", c.numero_os, "|", c.quantidade, "x", c.nome,
                      "= R$", c.valor)


def area_admin():
    if ler("Senha: ") != SENHA_ADMIN:
        print("Senha incorreta.")
        return
    while True:
        op = menu("""
--- ADMINISTRADOR ---
1 - Clientes e veículos
2 - Atendimento (filas e boxes)
3 - Diagnóstico
4 - Estoque
5 - Ordem de serviço
6 - Pagamento
0 - Voltar""")
        if op == 0:
            return
        elif op == 1:
            admin_clientes()
        elif op == 2:
            admin_atendimento()
        elif op == 3:
            admin_diagnostico()
        elif op == 4:
            admin_estoque()
        elif op == 5:
            admin_os()
        elif op == 6:
            admin_pagamento()


def carregar_exemplo():
    if estoque.buscar("P-010") is not None:
        print("Exemplo já carregado.")
        return
    hoje = date.today()
    clientes.cadastrar_cliente("Maria Souza", "111", "(19) 99999-0001")
    clientes.cadastrar_cliente("João Lima", "222", "(19) 99999-0002")
    clientes.cadastrar_veiculo("111", "ABC1D23", "Gol", "VW", 2018)
    clientes.cadastrar_veiculo("222", "QWE4R56", "Palio", "Fiat", 2012)
    estoque.cadastrar_produto("Pastilha dianteira", "P-010", 150.0, 4)
    estoque.cadastrar_produto("Disco dianteiro", "P-011", 220.0, 2)
    estoque.cadastrar_produto("Fluido de freio", "F-001", 45.0, 5)
    estoque.comprar("P-010", "AutoPeças RC", 90.0, hoje - timedelta(days=60), None, 3)
    estoque.comprar("P-010", "AutoPeças RC", 100.0, hoje - timedelta(days=10), None, 4)
    estoque.comprar("P-011", "AutoPeças RC", 130.0, hoje - timedelta(days=30), None, 3)
    estoque.comprar("F-001", "Fluidos SA", 20.0, hoje - timedelta(days=400), hoje - timedelta(days=5), 4)
    estoque.comprar("F-001", "Fluidos SA", 25.0, hoje - timedelta(days=5), hoje + timedelta(days=300), 3)
    print("Exemplo carregado. Clientes: CPF 111 (placa ABC1D23) e CPF 222 (placa QWE4R56).")


def main():
    print("=== OFICINA MECÂNICA ===")
    while True:
        op = menu("""
--- MENU INICIAL ---
1 - Sou cliente
2 - Sou administrador
3 - Carregar dados de exemplo
0 - Sair""")
        if op == 0:
            print("Até logo!")
            return
        elif op == 1:
            area_cliente()
        elif op == 2:
            area_admin()
        elif op == 3:
            carregar_exemplo()


main()
