from datetime import datetime
from estruturas import Lista

FORMAS = ("PIX", "CARTAO", "DINHEIRO")


class Pagamento:
    def __init__(self, pagador, numero_os, forma, parcelas, valor_pecas, valor_mao_obra):
        self.pagador = pagador
        self.numero_os = numero_os
        self.forma = forma
        self.parcelas = parcelas
        self.valor_pecas = valor_pecas
        self.valor_mao_obra = valor_mao_obra
        self.total = valor_pecas + valor_mao_obra
        self.data_hora = datetime.now()


class Consumo:
    def __init__(self, cliente, placa, numero_os, codigo, nome, quantidade, valor):
        self.cliente = cliente
        self.placa = placa
        self.numero_os = numero_os
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor


class Caixa:
    def __init__(self):
        self.pagamentos = Lista()
        self.consumos = Lista()

    def fechar_os(self, ordem, estoque, forma, parcelas=1):
        if not ordem.remontagem_concluida:
            raise ValueError("A OS só pode ser fechada após a remontagem do veículo.")
        if forma not in FORMAS:
            raise ValueError("Forma de pagamento inválida.")
        if forma != "CARTAO":
            parcelas = 1

        for item in ordem.pecas:
            produto = estoque.buscar(item.codigo)
            if produto is None or produto.total() < item.quantidade:
                raise ValueError("Estoque insuficiente para: " + item.nome)

        for item in ordem.pecas:
            estoque.dar_baixa(item.codigo, item.quantidade)
            self.consumos.adicionar(Consumo(ordem.cliente, ordem.placa, ordem.numero,
                                            item.codigo, item.nome, item.quantidade,
                                            item.quantidade * item.preco_unitario))

        pagamento = Pagamento(ordem.cliente, ordem.numero, forma, parcelas,
                              ordem.valor_pecas(), ordem.valor_mao_obra())
        self.pagamentos.adicionar(pagamento)
        return pagamento
