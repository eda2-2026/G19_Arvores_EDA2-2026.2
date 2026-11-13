from .no import No, PRETO
from .insercao import executar_insercao
from .remocao import executar_remocao

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = No(chave=None, cor=PRETO)
        self.raiz = self.NIL

    def inserir(self, chave):
        return executar_insercao(self, chave)

    def remover(self, chave):
        return executar_remocao(self, chave)

    def buscar(self, chave):
        atual = self.raiz
        while atual != self.NIL and chave != atual.chave:
            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return atual

    def rotacao_esquerda(self, x):
        y = x.direita
        x.direita = y.esquerda
        if y.esquerda != self.NIL:
            y.esquerda.pai = x
        y.pai = x.pai
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y

    def rotacao_direita(self, y):
        x = y.esquerda
        y.esquerda = x.direita
        if x.direita != self.NIL:
            x.direita.pai = y
        x.pai = y.pai
        if y.pai is None:
            self.raiz = x
        elif y == y.pai.direita:
            y.pai.direita = x
        else:
            y.pai.esquerda = x
        x.direita = y
        y.pai = x

    def contar_nos(self, no=None):
        if no is None:
            no = self.raiz
        if no == self.NIL:
            return 0
        return 1 + self.contar_nos(no.esquerda) + self.contar_nos(no.direita)

    def altura(self, no=None):
        if no is None:
            no = self.raiz
        if no == self.NIL:
            return 0
        return 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def obter_dados_svg(self, largura=1000, y_inicial=65, espaco_y=95):
        """Calcula automaticamente as posições X e Y de cada nó para o SVG."""
        nodes = list()
        if self.raiz == self.NIL:
            return nodes

        def percorrer(no, nivel, x_min, x_max):
            if no == self.NIL:
                return
            x = (x_min + x_max) / 2
            y = y_inicial + nivel * espaco_y
            nodes.append({
                "value": no.chave,
                "color": no.cor,
                "x": x,
                "y": y,
                "parent": no.pai.chave if no.pai else None
            })
            percorrer(no.esquerda, nivel + 1, x_min, x)
            percorrer(no.direita, nivel + 1, x, x_max)

        percorrer(self.raiz, 0, 40, largura - 40)
        return nodes
