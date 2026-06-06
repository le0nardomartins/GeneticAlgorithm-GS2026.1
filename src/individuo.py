"""
Representação dos indivíduos (cromossomos) da população.
"""

import random
from src.config import TAMANHO_ROTA, TAMANHO_POPULACAO


def gerar_individuo():
    """
    Cria um cromossomo aleatório com TAMANHO_ROTA genes.

    Cada gene é um inteiro de 0 a 3 que representa um movimento:
        0 → cima  |  1 → baixo  |  2 → esquerda  |  3 → direita

    Exemplo (5 genes):  [3, 1, 3, 1, 3]  ->  →↓→↓→
    """
    return [random.randint(0, 3) for _ in range(TAMANHO_ROTA)]


def gerar_populacao():
    """
    Gera a população inicial com TAMANHO_POPULACAO indivíduos aleatórios.

    A geração completamente aleatória garante máxima diversidade genética
    na geração zero, evitando viés inicial no espaço de busca.
    """
    return [gerar_individuo() for _ in range(TAMANHO_POPULACAO)]
