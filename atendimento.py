from datetime import datetime
from estruturas import Fila


class Chegada:
    def __init__(self, placa, cliente, queixa, guincho):
        self.placa = placa
        self.cliente = cliente
        self.data_hora = datetime.now()
        self.queixa = queixa
        self.guincho = guincho


class Atendimento:
    def __init__(self, num_boxes):
        self.fila_guincho = Fila()
        self.fila_normal = Fila()
        self.boxes_livres = num_boxes

    def registrar_chegada(self, placa, cliente, queixa, guincho=False):
        chegada = Chegada(placa, cliente, queixa, guincho)
        if guincho:
            self.fila_guincho.enfileirar(chegada)
        else:
            self.fila_normal.enfileirar(chegada)
        return chegada

    def indicar_proximo(self):
        if not self.fila_guincho.vazia():
            return self.fila_guincho.primeiro()
        return self.fila_normal.primeiro()

    def chamar_proximo(self):
        if self.boxes_livres == 0:
            return None
        if not self.fila_guincho.vazia():
            chegada = self.fila_guincho.desenfileirar()
        else:
            chegada = self.fila_normal.desenfileirar()
        if chegada is not None:
            self.boxes_livres -= 1
        return chegada

    def posicao(self, placa):
        pos = 1
        for c in self.fila_guincho:
            if c.placa == placa:
                return pos
            pos += 1
        for c in self.fila_normal:
            if c.placa == placa:
                return pos
            pos += 1
        return None

    def liberar_box(self):
        self.boxes_livres += 1
        return self.chamar_proximo()
