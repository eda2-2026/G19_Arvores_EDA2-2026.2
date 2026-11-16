## 💻 Sobre o Projeto

O **Simulador de Árvore Rubro-Negra** é uma aplicação desenvolvida em Python com o objetivo de auxiliar no aprendizado de Estruturas de Dados 2, especialmente no estudo das Árvores Rubro-Negras (Red-Black Trees).

A proposta é oferecer um ambiente interativo no qual o estudante possa visualizar o funcionamento dessa estrutura, compreender como os elementos são inseridos e removidos e acompanhar as operações necessárias para manter o balanceamento da árvore.

Diferentemente de uma abordagem exclusivamente teórica, o simulador busca tornar os conceitos mais intuitivos por meio de representações gráficas, permitindo observar as alterações na estrutura, as rotações e as mudanças de cores dos nós durante as operações.

## 👥 Alunos Integrantes

*   **[Cauã Nicolas Pereira de Oliveira]** - *231026670*
*   **[João Lucas Ramos dos Reis]** - *211061930*


## 🎥 Vídeo de Apresentação do Projeto

Produzimos um vídeo demonstrativo detalhando o funcionamento prático da nossa *(projeto)*, o reaproveitamento da estrutura criada em Orientação a Objetos e a explicação da lógica brute do algoritmo...

▶️ **[Clique aqui para assistir diretamente no YouTube](link_do_video)**

> 💡 *Nota: Caso o player acima não carregue ou o link não funcione, você também pode copiar e colar a seguinte URL no seu navegador:*  
> `link_do_video`

## 🧠 O Algoritmo: (...)

A Árvore Rubro-Negra é uma estrutura de dados baseada em uma Árvore Binária de Busca (ABB), na qual cada nó possui uma informação adicional: sua cor, que pode ser vermelha ou preta.

Essa estrutura utiliza regras específicas para manter o balanceamento, evitando que a árvore se torne excessivamente desproporcional e garantindo operações eficientes.

### Propriedades da Árvore Rubro-Negra

1. Todo nó é vermelho ou preto.
2. A raiz da árvore é sempre preta.
3. Todas as folhas NIL (nós sentinela que representam posições vazias) são pretas.
4. Um nó vermelho não pode possuir um filho vermelho.
5. Todos os caminhos de um nó até suas folhas descendentes NIL possuem a mesma quantidade de nós pretos.

### Operações de balanceamento

Para preservar essas propriedades após alterações na árvore, o algoritmo utiliza duas operações principais:

**Rotação à esquerda:** reorganiza os nós deslocando um filho direito para a posição superior.

**Rotação à direita:** reorganiza os nós deslocando um filho esquerdo para a posição superior.

Além das rotações, o algoritmo utiliza a recoloração dos nós para corrigir possíveis violações das propriedades da estrutura.

Na **inserção**, um novo nó é inicialmente vermelho. Em seguida, o algoritmo verifica se sua inserção provocou alguma violação e, quando necessário, aplica os casos de correção, envolvendo rotações e recolorações.

Na **remoção**, o algoritmo verifica se a exclusão comprometeu a quantidade de nós pretos nos caminhos da árvore, aplicando os casos de correção correspondentes.

---

## 📊 Complexidade

| Operação | Complexidade |
| :--- | :--- |
| `busca` | (O(log n))|
| `inserção` | (O(log n))|
| `remoção` | (O(log n))|
| `rotação à esquerda` | (O(1))|
| `rotação à direita` | (O(1))|
| `percurso completo` | (O(n))|

---

## 📁 Arquivos do Projeto

| Arquivo | Função |
| :--- | :--- |
| `no.py` | Classe dos nós e cores |
| `arvore_rubronegra.py` | Estrutura, rotações e validação |
| `insercao.py` | Inserção e histórico das operações |
| `remocao.py` | Remoção e histórico das operações|
| `visualizacao.py` | Desenho SVG com destaque dos nós |
| `controles.py` | Navegação Anterior, Próximo e Reiniciar |
| `informacoes.py` | Explicação dos casos |
| `app.py` | Integração de tudo |

## 🛠️ Tecnologias Utilizadas

* **Python** (Linguagem utilizada para implementar a estrutura de dados e os algoritmos.)
* **Streamlit** (Desenvolvimento da interface interativa e dos controles do simulador.)
* **SVG (Scalable Vector Graphics)** (Representação gráfica da árvore, dos nós e das conexões entre eles.)

## 🔧 Como Executar o Projeto
## Simulador de Árvore Rubro-Negra — Front-end

Interface inicial em Streamlit com visualização SVG demonstrativa.

## Executar
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install streamlit
streamlit run app.py
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
