from .no import VERMELHO, PRETO

def executar_remocao(arvore, chave):
    z = arvore.buscar(chave)
    if z == arvore.NIL:
        return False, f"O valor {chave} não foi encontrado na árvore."

    y = z
    y_cor_original = y.cor
    if z.esquerda == arvore.NIL:
        x = z.direita
        _transplante(arvore, z, z.direita)
    elif z.direita == arvore.NIL:
        x = z.esquerda
        _transplante(arvore, z, z.esquerda)
    else:
        y = _minimo(arvore, z.direita)
        y_cor_original = y.cor
        x = y.direita
        if y.pai == z:
            x.pai = y
        else:
            _transplante(arvore, y, y.direita)
            y.direita = z.direita
            y.direita.pai = y

        _transplante(arvore, z, y)
        y.esquerda = z.esquerda
        y.esquerda.pai = y
        y.cor = z.cor

    if y_cor_original == PRETO:
        _corrigir_remocao(arvore, x)

    return True, f"Valor {chave} removido e árvore rebalanceada."

def _transplante(arvore, u, v):
    if u.pai is None:
        arvore.raiz = v
    elif u == u.pai.esquerda:
        u.pai.esquerda = v
    else:
        u.pai.direita = v
    v.pai = u.pai

def _minimo(arvore, no):
    while no.esquerda != arvore.NIL:
        no = no.esquerda
    return no

def _corrigir_remocao(arvore, x):
    while x != arvore.raiz and x.cor == PRETO:
        if x == x.pai.esquerda:
            s = x.pai.direita
            if s.cor == VERMELHO:
                s.cor = PRETO
                x.pai.cor = VERMELHO
                arvore.rotacao_esquerda(x.pai)
                s = x.pai.direita

            if s.esquerda.cor == PRETO and s.direita.cor == PRETO:
                s.cor = VERMELHO
                x = x.pai
            else:
                if s.direita.cor == PRETO:
                    s.esquerda.cor = PRETO
                    s.cor = VERMELHO
                    arvore.rotacao_direita(s)
                    s = x.pai.direita

                s.cor = x.pai.cor
                x.pai.cor = PRETO
                s.direita.cor = PRETO
                arvore.rotacao_esquerda(x.pai)
                x = arvore.raiz
        else:
            s = x.pai.esquerda
            if s.cor == VERMELHO:
                s.cor = PRETO
                x.pai.cor = VERMELHO
                arvore.rotacao_direita(x.pai)
                s = x.pai.esquerda

            if s.direita.cor == PRETO and s.esquerda.cor == PRETO:
                s.cor = VERMELHO
                x = x.pai
            else:
                if s.esquerda.cor == PRETO:
                    s.direita.cor = PRETO
                    s.cor = VERMELHO
                    arvore.rotacao_esquerda(s)
                    s = x.pai.esquerda

                s.cor = x.pai.cor
                x.pai.cor = PRETO
                s.esquerda.cor = PRETO
                arvore.rotacao_direita(x.pai)
                x = arvore.raiz
    x.cor = PRETO
