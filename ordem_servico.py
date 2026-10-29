from datetime import datetime
from estruturas import Lista


class ItemPeca:
    def __init__(self, codigo, nome, quantidade, preco_unitario):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario


class Servico:
    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor


class OrdemServico:
    def __init__(self, numero, placa, cliente, mecanico):
        self.numero = numero
        self.placa = placa
        self.cliente = cliente
        self.mecanico = mecanico
        self.data_abertura = datetime.now()
        self.pecas = Lista()
        self.servicos = Lista()
        self.remontagem_concluida = False

    def adicionar_peca(self, produto, quantidade):
        if produto.total() < quantidade:
            return False
        item = self.pecas.buscar(lambda i: i.codigo == produto.codigo)
        if item is not None:
            if produto.total() < item.quantidade + quantidade:
                return False
            item.quantidade += quantidade
        else:
            self.pecas.adicionar(ItemPeca(produto.codigo, produto.nome, quantidade, produto.preco_venda))
        return True

    def remover_peca(self, codigo):
        return self.pecas.remover(lambda i: i.codigo == codigo)

    def adicionar_servico(self, descricao, valor):
        self.servicos.adicionar(Servico(descricao, valor))

    def remover_servico(self, descricao):
        return self.servicos.remover(lambda s: s.descricao == descricao)

    def valor_pecas(self):
        soma = 0
        for item in self.pecas:
            soma += item.quantidade * item.preco_unitario
        return soma

    def valor_mao_obra(self):
        soma = 0
        for servico in self.servicos:
            soma += servico.valor
        return soma

    def total(self):
        return self.valor_pecas() + self.valor_mao_obra()


class ControleOS:

    def __init__(self):
        self.abertas = Lista()
        self.proximo_numero = 1

    def abrir(self, placa, cliente, mecanico):
        os_nova = OrdemServico(self.proximo_numero, placa, cliente, mecanico)
        self.proximo_numero += 1
        self.abertas.adicionar(os_nova)
        return os_nova

    def buscar(self, numero):
        return self.abertas.buscar(lambda o: o.numero == numero)

    def remover(self, numero):
        return self.abertas.remover(lambda o: o.numero == numero)
