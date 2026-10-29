class No:
    def __init__(self, dado):
        self.dado = dado
        self.prox = None


class Lista:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def adicionar(self, dado):  # O(1)
        novo = No(dado)
        if self.inicio is None:
            self.inicio = novo
        else:
            self.fim.prox = novo
        self.fim = novo
        self.tamanho += 1

    def buscar(self, criterio):  # O(n)
        """Devolve o primeiro dado para o qual criterio(dado) for True."""
        atual = self.inicio
        while atual is not None:
            if criterio(atual.dado):
                return atual.dado
            atual = atual.prox
        return None

    def remover(self, criterio):  # O(n)
        """Remove e devolve o primeiro dado que satisfaz o critério."""
        anterior = None
        atual = self.inicio
        while atual is not None:
            if criterio(atual.dado):
                if anterior is None:
                    self.inicio = atual.prox
                else:
                    anterior.prox = atual.prox
                if atual is self.fim:
                    self.fim = anterior
                self.tamanho -= 1
                return atual.dado
            anterior = atual
            atual = atual.prox
        return None

    def __iter__(self):  # permite usar "for x in lista"
        atual = self.inicio
        while atual is not None:
            yield atual.dado
            atual = atual.prox


class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def vazia(self):
        return self.inicio is None

    def enfileirar(self, dado):  # O(1)
        novo = No(dado)
        if self.fim is None:
            self.inicio = novo
        else:
            self.fim.prox = novo
        self.fim = novo
        self.tamanho += 1

    def desenfileirar(self):  # O(1)
        if self.inicio is None:
            return None
        dado = self.inicio.dado
        self.inicio = self.inicio.prox
        if self.inicio is None:
            self.fim = None
        self.tamanho -= 1
        return dado

    def primeiro(self):  # espiar sem remover
        if self.inicio is None:
            return None
        return self.inicio.dado

    def __iter__(self):
        atual = self.inicio
        while atual is not None:
            yield atual.dado
            atual = atual.prox


class NoArvore:
    def __init__(self, valor):
        self.valor = valor
        self.filhos = Lista()

    def adicionar_filho(self, valor):
        filho = NoArvore(valor)
        self.filhos.adicionar(filho)
        return filho

    def pre_ordem(self, visitar, nivel=0):  # O(n)
        visitar(self.valor, nivel)
        for filho in self.filhos:
            filho.pre_ordem(visitar, nivel + 1)

    def buscar(self, criterio):  # O(n)
        if criterio(self.valor):
            return self
        for filho in self.filhos:
            achado = filho.buscar(criterio)
            if achado is not None:
                return achado
        return None
