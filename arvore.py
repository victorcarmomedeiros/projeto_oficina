from estruturas import NoArvore, Lista


class Componente:
    def __init__(self, nome, codigo=None):
        self.nome = nome
        self.codigo = codigo  
        self.estado = "OK"


def construir_arvore():
    raiz = NoArvore(Componente("Veículo"))

    motor = raiz.adicionar_filho(Componente("Motor"))
    ignicao = motor.adicionar_filho(Componente("Sistema de ignição"))
    ignicao.adicionar_filho(Componente("Vela", "P-001"))
    ignicao.adicionar_filho(Componente("Bobina", "P-002"))
    motor.adicionar_filho(Componente("Correia dentada", "P-003"))

    freios = raiz.adicionar_filho(Componente("Freios"))
    freios.adicionar_filho(Componente("Pastilha dianteira", "P-010"))
    freios.adicionar_filho(Componente("Disco dianteiro", "P-011"))

    suspensao = raiz.adicionar_filho(Componente("Suspensão"))
    suspensao.adicionar_filho(Componente("Amortecedor", "P-020"))
    suspensao.adicionar_filho(Componente("Bandeja", "P-021"))
    return raiz


def exibir_arvore(raiz):
    def mostrar(comp, nivel):
        texto = "    " * nivel + "- " + comp.nome
        if comp.codigo is not None:
            texto += " [" + comp.codigo + "]"
        texto += " (" + comp.estado + ")"
        print(texto)

    raiz.pre_ordem(mostrar)


def marcar_defeito(raiz, nome):
    no = raiz.buscar(lambda c: c.nome == nome)
    if no is None:
        return False
    no.valor.estado = "Com defeito"
    return True


def listar_pecas_com_defeito(raiz):
    defeitos = Lista()

    def verificar(comp, nivel):
        if comp.codigo is not None and comp.estado == "Com defeito":
            defeitos.adicionar(comp)

    raiz.pre_ordem(verificar)
    return defeitos
