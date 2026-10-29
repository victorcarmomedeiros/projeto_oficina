"""1) Controle de clientes e veículos.

COMBINAÇÃO: Lista de clientes, onde cada cliente contém uma Lista de veículos.
"""
from estruturas import Lista


class Veiculo:
    def __init__(self, placa, modelo, marca, ano):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano


class Cliente:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.veiculos = Lista()  # sem limite de veículos


class ControleClientes:
    def __init__(self):
        self.clientes = Lista()

    def cadastrar_cliente(self, nome, cpf, telefone):
        if self.buscar_por_cpf(cpf) is not None:
            return None  # CPF já cadastrado
        cliente = Cliente(nome, cpf, telefone)
        self.clientes.adicionar(cliente)
        return cliente

    def buscar_por_cpf(self, cpf):
        return self.clientes.buscar(lambda c: c.cpf == cpf)

    def buscar_por_placa(self, placa):
        """Percorre a lista de clientes e, dentro de cada um, a lista de veículos."""
        for cliente in self.clientes:
            veiculo = cliente.veiculos.buscar(lambda v: v.placa == placa)
            if veiculo is not None:
                return cliente, veiculo
        return None, None

    def remover_cliente(self, cpf):
        return self.clientes.remover(lambda c: c.cpf == cpf)

    def cadastrar_veiculo(self, cpf, placa, modelo, marca, ano):
        cliente = self.buscar_por_cpf(cpf)
        if cliente is None:
            return None
        if self.buscar_por_placa(placa)[0] is not None:
            return None  # placa já cadastrada
        veiculo = Veiculo(placa, modelo, marca, ano)
        cliente.veiculos.adicionar(veiculo)
        return veiculo

    def remover_veiculo(self, placa):
        cliente, veiculo = self.buscar_por_placa(placa)
        if cliente is None:
            return None
        return cliente.veiculos.remover(lambda v: v.placa == placa)
