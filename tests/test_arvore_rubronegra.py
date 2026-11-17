"""
Testes unitários para a Árvore Rubro-Negra.

Executar todos os testes:
    python -m pytest tests/ -v
    ou
    python -m unittest tests.test_arvore_rubronegra -v
"""

import unittest
import random

from arvore.arvore_rubronegra import ArvoreRubroNegra
from arvore.no import VERMELHO, PRETO


# ─── Helpers ────────────────────────────────────────────────────────

def inorder(arvore, no=None):
    """Retorna a lista de chaves em ordem simétrica (in-order)."""
    if no is None:
        no = arvore.raiz
    if no == arvore.NIL:
        return []
    return inorder(arvore, no.esquerda) + [no.chave] + inorder(arvore, no.direita)


def verificar_propriedades(arvore):
    """
    Verifica todas as propriedades da árvore rubro-negra.
    Retorna (ok, lista_de_erros).
    """
    erros = []

    # P2: Raiz é preta
    if arvore.raiz != arvore.NIL and arvore.raiz.cor != PRETO:
        erros.append(f"Raiz não é preta (cor={arvore.raiz.cor})")

    # P3: Sentinela NIL é preta
    if arvore.NIL.cor != PRETO:
        erros.append(f"NIL não é preto (cor={arvore.NIL.cor})")

    # P4: Nó vermelho não tem filho vermelho
    def _check_red_red(no):
        if no == arvore.NIL:
            return
        if no.cor == VERMELHO:
            if no.esquerda.cor == VERMELHO:
                erros.append(
                    f"Nó vermelho {no.chave} tem filho esquerdo vermelho {no.esquerda.chave}"
                )
            if no.direita.cor == VERMELHO:
                erros.append(
                    f"Nó vermelho {no.chave} tem filho direito vermelho {no.direita.chave}"
                )
        _check_red_red(no.esquerda)
        _check_red_red(no.direita)

    _check_red_red(arvore.raiz)

    # P5: Todos os caminhos têm a mesma black-height
    def _black_height(no):
        if no == arvore.NIL:
            return 1
        bh_esq = _black_height(no.esquerda)
        bh_dir = _black_height(no.direita)
        if bh_esq == -1 or bh_dir == -1:
            return -1
        if bh_esq != bh_dir:
            erros.append(
                f"Black-height diferente no nó {no.chave}: esq={bh_esq}, dir={bh_dir}"
            )
            return -1
        return bh_esq + (1 if no.cor == PRETO else 0)

    _black_height(arvore.raiz)

    # Integridade dos ponteiros pai
    def _check_pai(no, pai_esperado):
        if no == arvore.NIL:
            return
        if no.pai != pai_esperado:
            chave_esperada = pai_esperado.chave if pai_esperado else None
            chave_real = no.pai.chave if no.pai else None
            erros.append(
                f"Nó {no.chave}: pai esperado={chave_esperada}, pai real={chave_real}"
            )
        _check_pai(no.esquerda, no)
        _check_pai(no.direita, no)

    _check_pai(arvore.raiz, None)

    # Propriedade BST (ordem)
    def _check_bst(no, minimo=float("-inf"), maximo=float("inf")):
        if no == arvore.NIL:
            return
        if no.chave <= minimo or no.chave >= maximo:
            erros.append(
                f"Nó {no.chave} viola ordem BST (intervalo esperado: ({minimo}, {maximo}))"
            )
        _check_bst(no.esquerda, minimo, no.chave)
        _check_bst(no.direita, no.chave, maximo)

    _check_bst(arvore.raiz)

    return len(erros) == 0, erros


def assertArvoreValida(test_case, arvore, msg=""):
    """Atalho para usar dentro dos testes unitários."""
    ok, erros = verificar_propriedades(arvore)
    test_case.assertTrue(ok, f"Propriedades violadas{' — ' + msg if msg else ''}:\n" + "\n".join(erros))


# ─── Testes de Inserção ────────────────────────────────────────────

class TestInsercao(unittest.TestCase):

    def test_inserir_raiz(self):
        """Inserir um único elemento deve criar a raiz preta."""
        arv = ArvoreRubroNegra()
        sucesso, _ = arv.inserir(10)
        self.assertTrue(sucesso)
        self.assertEqual(arv.raiz.chave, 10)
        self.assertEqual(arv.raiz.cor, PRETO)
        assertArvoreValida(self, arv)

    def test_inserir_dois_elementos(self):
        """Inserir dois elementos: raiz preta, filho vermelho."""
        arv = ArvoreRubroNegra()
        arv.inserir(10)
        arv.inserir(5)
        assertArvoreValida(self, arv)
        self.assertEqual(arv.contar_nos(), 2)

    def test_inserir_tres_elementos_rotacao(self):
        """Três inserções crescentes forçam rotação à esquerda."""
        arv = ArvoreRubroNegra()
        arv.inserir(10)
        arv.inserir(20)
        arv.inserir(30)
        assertArvoreValida(self, arv)
        self.assertEqual(inorder(arv), [10, 20, 30])

    def test_rejeitar_duplicata(self):
        """Inserir chave duplicada deve retornar False."""
        arv = ArvoreRubroNegra()
        arv.inserir(10)
        sucesso, msg = arv.inserir(10)
        self.assertFalse(sucesso)
        self.assertIn("já existe", msg)
        self.assertEqual(arv.contar_nos(), 1)

    def test_insercao_sequencial_crescente(self):
        """Inserir 1 a 30 em ordem crescente — pior caso para BST, OK para RB."""
        arv = ArvoreRubroNegra()
        for i in range(1, 31):
            arv.inserir(i)
            assertArvoreValida(self, arv, f"após inserir {i}")
        self.assertEqual(inorder(arv), list(range(1, 31)))
        self.assertEqual(arv.contar_nos(), 30)

    def test_insercao_sequencial_decrescente(self):
        """Inserir 30 a 1 em ordem decrescente."""
        arv = ArvoreRubroNegra()
        for i in range(30, 0, -1):
            arv.inserir(i)
            assertArvoreValida(self, arv, f"após inserir {i}")
        self.assertEqual(inorder(arv), list(range(1, 31)))

    def test_insercao_caso_tio_vermelho(self):
        """Força recoloração (tio vermelho) em ambos os lados."""
        arv = ArvoreRubroNegra()
        for v in [20, 10, 30, 5]:
            arv.inserir(v)
        assertArvoreValida(self, arv)

    def test_insercao_caso_tio_preto_rotacao_simples(self):
        """Força rotação simples (tio preto, nó externo)."""
        arv = ArvoreRubroNegra()
        for v in [30, 20, 10]:
            arv.inserir(v)
        assertArvoreValida(self, arv)
        self.assertEqual(arv.raiz.chave, 20)

    def test_insercao_caso_tio_preto_rotacao_dupla(self):
        """Força rotação dupla (tio preto, nó interno)."""
        arv = ArvoreRubroNegra()
        for v in [30, 10, 20]:
            arv.inserir(v)
        assertArvoreValida(self, arv)
        self.assertEqual(arv.raiz.chave, 20)

    def test_altura_logaritmica(self):
        """A altura deve ser no máximo 2·log₂(n+1)."""
        import math
        arv = ArvoreRubroNegra()
        n = 100
        for i in range(1, n + 1):
            arv.inserir(i)
        altura_max = 2 * math.log2(n + 1)
        self.assertLessEqual(arv.altura(), altura_max + 1)


# ─── Testes de Remoção ─────────────────────────────────────────────

class TestRemocao(unittest.TestCase):

    def _criar_arvore(self, chaves):
        arv = ArvoreRubroNegra()
        for c in chaves:
            arv.inserir(c)
        return arv

    def test_remover_raiz_unica(self):
        """Remover o único nó da árvore."""
        arv = self._criar_arvore([10])
        sucesso, _ = arv.remover(10)
        self.assertTrue(sucesso)
        self.assertEqual(arv.raiz, arv.NIL)
        assertArvoreValida(self, arv)

    def test_remover_folha(self):
        """Remover uma folha."""
        arv = self._criar_arvore([20, 10, 30])
        arv.remover(10)
        assertArvoreValida(self, arv)
        self.assertNotIn(10, inorder(arv))

    def test_remover_no_com_um_filho(self):
        """Remover nó que tem apenas um filho."""
        arv = self._criar_arvore([20, 10, 30, 5])
        arv.remover(10)
        assertArvoreValida(self, arv)
        self.assertEqual(sorted(inorder(arv)), [5, 20, 30])

    def test_remover_no_com_dois_filhos(self):
        """Remover nó que tem dois filhos (usa sucessor in-order)."""
        arv = self._criar_arvore([20, 10, 30, 5, 15, 25, 40])
        arv.remover(20)
        assertArvoreValida(self, arv)
        self.assertNotIn(20, inorder(arv))
        self.assertEqual(len(inorder(arv)), 6)

    def test_remover_raiz_com_filhos(self):
        """Remover a raiz quando há outros nós."""
        arv = self._criar_arvore([20, 10, 30])
        arv.remover(20)
        assertArvoreValida(self, arv)
        self.assertEqual(sorted(inorder(arv)), [10, 30])

    def test_remover_valor_inexistente(self):
        """Remover valor que não existe deve retornar False."""
        arv = self._criar_arvore([10, 20, 30])
        sucesso, msg = arv.remover(99)
        self.assertFalse(sucesso)
        self.assertIn("não foi encontrado", msg)
        self.assertEqual(arv.contar_nos(), 3)

    def test_remover_de_arvore_vazia(self):
        """Remover de árvore vazia deve retornar False."""
        arv = ArvoreRubroNegra()
        sucesso, _ = arv.remover(1)
        self.assertFalse(sucesso)

    def test_remover_todos_os_nos(self):
        """Remover todos os nós um a um, verificando propriedades a cada passo."""
        chaves = [20, 10, 30, 5, 15, 25, 40, 2, 7, 12, 18, 22, 28, 35, 45]
        arv = self._criar_arvore(chaves)
        for c in chaves:
            arv.remover(c)
            assertArvoreValida(self, arv, f"após remover {c}")
        self.assertEqual(arv.raiz, arv.NIL)

    def test_remover_todos_em_ordem_inversa(self):
        """Remover todos em ordem inversa à inserção."""
        chaves = [20, 10, 30, 5, 15, 25, 40]
        arv = self._criar_arvore(chaves)
        for c in reversed(chaves):
            arv.remover(c)
            assertArvoreValida(self, arv, f"após remover {c}")
        self.assertEqual(arv.raiz, arv.NIL)

    def test_remocao_no_preto_caso_irmao_vermelho(self):
        """Força o caso 1 da correção (irmão vermelho)."""
        arv = self._criar_arvore([10, 5, 20, 15, 30, 25, 35])
        arv.remover(5)
        assertArvoreValida(self, arv)


# ─── Testes de Busca ───────────────────────────────────────────────

class TestBusca(unittest.TestCase):

    def _criar_arvore(self, chaves):
        arv = ArvoreRubroNegra()
        for c in chaves:
            arv.inserir(c)
        return arv

    def test_buscar_existente(self):
        """Buscar chave que existe retorna o nó correto."""
        arv = self._criar_arvore([50, 25, 75, 10, 30])
        for v in [50, 25, 75, 10, 30]:
            resultado = arv.buscar(v)
            self.assertNotEqual(resultado, arv.NIL)
            self.assertEqual(resultado.chave, v)

    def test_buscar_inexistente(self):
        """Buscar chave que não existe retorna NIL."""
        arv = self._criar_arvore([10, 20, 30])
        resultado = arv.buscar(999)
        self.assertEqual(resultado, arv.NIL)

    def test_buscar_em_arvore_vazia(self):
        """Buscar em árvore vazia retorna NIL."""
        arv = ArvoreRubroNegra()
        resultado = arv.buscar(10)
        self.assertEqual(resultado, arv.NIL)


# ─── Testes de Rotação ─────────────────────────────────────────────

class TestRotacao(unittest.TestCase):

    def test_rotacao_esquerda_preserva_propriedades(self):
        """Rotação à esquerda via inserções que a forçam."""
        arv = ArvoreRubroNegra()
        for v in [10, 20, 30]:
            arv.inserir(v)
        assertArvoreValida(self, arv)
        # Após rotação, 20 deve ser a raiz
        self.assertEqual(arv.raiz.chave, 20)
        self.assertEqual(arv.raiz.esquerda.chave, 10)
        self.assertEqual(arv.raiz.direita.chave, 30)

    def test_rotacao_direita_preserva_propriedades(self):
        """Rotação à direita via inserções que a forçam."""
        arv = ArvoreRubroNegra()
        for v in [30, 20, 10]:
            arv.inserir(v)
        assertArvoreValida(self, arv)
        self.assertEqual(arv.raiz.chave, 20)
        self.assertEqual(arv.raiz.esquerda.chave, 10)
        self.assertEqual(arv.raiz.direita.chave, 30)


# ─── Testes de Métodos Auxiliares ──────────────────────────────────

class TestMetodosAuxiliares(unittest.TestCase):

    def _criar_arvore(self, chaves):
        arv = ArvoreRubroNegra()
        for c in chaves:
            arv.inserir(c)
        return arv

    def test_contar_nos_vazia(self):
        arv = ArvoreRubroNegra()
        self.assertEqual(arv.contar_nos(), 0)

    def test_contar_nos(self):
        arv = self._criar_arvore([10, 5, 15, 3, 7])
        self.assertEqual(arv.contar_nos(), 5)

    def test_altura_vazia(self):
        arv = ArvoreRubroNegra()
        self.assertEqual(arv.altura(), 0)

    def test_altura_um_no(self):
        arv = self._criar_arvore([10])
        self.assertEqual(arv.altura(), 1)

    def test_obter_dados_svg_vazia(self):
        arv = ArvoreRubroNegra()
        self.assertEqual(arv.obter_dados_svg(), [])

    def test_obter_dados_svg(self):
        arv = self._criar_arvore([20, 10, 30])
        dados = arv.obter_dados_svg()
        self.assertEqual(len(dados), 3)
        valores = {d["value"] for d in dados}
        self.assertEqual(valores, {10, 20, 30})
        for d in dados:
            self.assertIn(d["color"], ("red", "black"))
            self.assertIn("x", d)
            self.assertIn("y", d)


# ─── Stress Tests ──────────────────────────────────────────────────

class TestStress(unittest.TestCase):

    def test_insercao_e_remocao_aleatorias(self):
        """500 inserções seguidas de 500 remoções aleatórias."""
        random.seed(42)
        arv = ArvoreRubroNegra()
        chaves = random.sample(range(1, 2001), 500)

        for c in chaves:
            arv.inserir(c)
        assertArvoreValida(self, arv, "após todas as inserções")
        self.assertEqual(inorder(arv), sorted(chaves))

        random.shuffle(chaves)
        for c in chaves:
            arv.remover(c)
        assertArvoreValida(self, arv, "após todas as remoções")
        self.assertEqual(arv.raiz, arv.NIL)

    def test_operacoes_intercaladas(self):
        """1000 operações intercaladas de inserção e remoção."""
        random.seed(123)
        arv = ArvoreRubroNegra()
        presentes = set()

        for _ in range(1000):
            if len(presentes) == 0 or random.random() < 0.6:
                val = random.randint(1, 500)
                if val not in presentes:
                    arv.inserir(val)
                    presentes.add(val)
            else:
                val = random.choice(list(presentes))
                arv.remover(val)
                presentes.discard(val)

        assertArvoreValida(self, arv, "após operações intercaladas")
        self.assertEqual(inorder(arv), sorted(presentes))


if __name__ == "__main__":
    unittest.main()

