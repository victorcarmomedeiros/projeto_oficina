from estruturas import Lista, Fila


class Lote:
    def __init__(self, numero, fornecedor, preco_compra, data_compra, validade, quantidade):
        self.numero = numero
        self.fornecedor = fornecedor
        self.preco_compra = preco_compra
        self.data_compra = data_compra
        self.validade = validade  
        self.quantidade = quantidade


class Produto:
    def __init__(self, nome, codigo, preco_venda, minimo):
        self.nome = nome
        self.codigo = codigo
        self.preco_venda = preco_venda
        self.minimo = minimo
        self.lotes = Fila()

    def total(self):
        soma = 0
        for lote in self.lotes:
            soma += lote.quantidade
        return soma


class Perda:
    def __init__(self, produto, lote, data):
        self.produto = produto
        self.lote = lote
        self.data = data


class Estoque:
    def __init__(self):
        self.produtos = Lista()
        self.perdas = Lista()
        self.proximo_lote = 1

    def cadastrar_produto(self, nome, codigo, preco_venda, minimo):
        produto = Produto(nome, codigo, preco_venda, minimo)
        self.produtos.adicionar(produto)
        return produto

    def buscar(self, codigo):
        return self.produtos.buscar(lambda p: p.codigo == codigo)

    def comprar(self, codigo, fornecedor, preco_compra, data_compra, validade, quantidade):
        produto = self.buscar(codigo)
        if produto is None:
            return None
        lote = Lote(self.proximo_lote, fornecedor, preco_compra, data_compra, validade, quantidade)
        self.proximo_lote += 1
        produto.lotes.enfileirar(lote)  # lote novo entra no fim da fila
        return lote

    def dar_baixa(self, codigo, quantidade):
        produto = self.buscar(codigo)
        if produto is None or produto.total() < quantidade:
            return False
        while quantidade > 0:
            lote = produto.lotes.primeiro()
            if lote.quantidade <= quantidade:
                quantidade -= lote.quantidade
                produto.lotes.desenfileirar()  # lote esgotado
            else:
                lote.quantidade -= quantidade
                quantidade = 0
        return True

    def descartar_vencidos(self, hoje):
        for produto in self.produtos:
            nova_fila = Fila()
            while not produto.lotes.vazia():
                lote = produto.lotes.desenfileirar()
                if lote.validade is not None and lote.validade < hoje:
                    self.perdas.adicionar(Perda(produto, lote, hoje))
                else:
                    nova_fila.enfileirar(lote)
            produto.lotes = nova_fila

    def ajustar_lote(self, codigo, numero_lote, nova_quantidade):
        produto = self.buscar(codigo)
        if produto is None:
            return False
        for lote in produto.lotes:
            if lote.numero == numero_lote:
                lote.quantidade = nova_quantidade
                return True
        return False

    def alertas_minimo(self):
        alertas = Lista()
        for produto in self.produtos:
            if produto.total() < produto.minimo:
                alertas.adicionar(produto)
        return alertas
