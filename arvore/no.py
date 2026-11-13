VERMELHO = "red"
PRETO = "black"

class No:
    def __init__(self, chave, cor=VERMELHO, esquerda=None, direita=None, pai=None):
        self.chave = chave
        self.cor = cor
        self.esquerda = esquerda
        self.direita = direita
        self.pai = pai