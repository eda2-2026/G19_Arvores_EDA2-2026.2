from .no import No, VERMELHO, PRETO

def executar_insercao(arvore, chave):
    novo_no = No(chave=chave, cor=VERMELHO, esquerda=arvore.NIL, direita=arvore.NIL)
    pai = None
    atual = arvore.raiz

    while atual != arvore.NIL:
        pai = atual
        if novo_no.chave == atual.chave:
            return False, f"O valor {chave} já existe na árvore."
        elif novo_no.chave < atual.chave:
            atual = atual.esquerda
        else:
            atual = atual.direita

    novo_no.pai = pai
    if pai is None:
        arvore.raiz = novo_no
    elif novo_no.chave < pai.chave:
        pai.esquerda = novo_no
    else:
        pai.direita = novo_no

    if novo_no.pai is None:
        novo_no.cor = PRETO
        return True, f"Valor {chave} inserido como raiz (preto)."

    if novo_no.pai.pai is None:
        return True, f"Valor {chave} inserido como filho direto da raiz."

    _corrigir_insercao(arvore, novo_no)
    return True, f"Valor {chave} inserido e árvore rebalanceada com sucesso."

def _corrigir_insercao(arvore, k):
    while k.pai.cor == VERMELHO:
        if k.pai == k.pai.pai.direita:
            tio = k.pai.pai.esquerda
            if tio.cor == VERMELHO:
                tio.cor = PRETO
                k.pai.cor = PRETO
                k.pai.pai.cor = VERMELHO
                k = k.pai.pai
            else:
                if k == k.pai.esquerda:
                    k = k.pai
                    arvore.rotacao_direita(k)
                k.pai.cor = PRETO
                k.pai.pai.cor = VERMELHO
                arvore.rotacao_esquerda(k.pai.pai)
        else:
            tio = k.pai.pai.direita
            if tio.cor == VERMELHO:
                tio.cor = PRETO
                k.pai.cor = PRETO
                k.pai.pai.cor = VERMELHO
                k = k.pai.pai
            else:
                if k == k.pai.direita:
                    k = k.pai
                    arvore.rotacao_esquerda(k)
                k.pai.cor = PRETO
                k.pai.pai.cor = VERMELHO
                arvore.rotacao_direita(k.pai.pai)
        if k == arvore.raiz:
            break
    arvore.raiz.cor = PRETO