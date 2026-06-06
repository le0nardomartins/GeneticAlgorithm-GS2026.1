"""
Operadores genéticos: seleção, crossover e mutação.
"""

import random
from copy import deepcopy
from src.config import TAXA_CROSSOVER, TAXA_MUTACAO, TAMANHO_ROTA


def selecionar_pais(populacao, fitnesses, tamanho_torneio=5):
    """
    Seleção por Torneio (Tournament Selection).

    Sorteia 'tamanho_torneio' candidatos aleatórios e retorna o melhor.
    Controla a pressão seletiva pelo tamanho do torneio:
    - Torneio menor → mais diversidade.
    - Torneio maior → maior pressão para os melhores.
    """
    candidatos = random.sample(range(len(populacao)), tamanho_torneio)
    vencedor   = max(candidatos, key=lambda i: fitnesses[i])
    return populacao[vencedor]


def aplicar_crossover(pai1, pai2):
    """
    Crossover de Ponto Único (Single-Point Crossover).

    Seleciona um ponto de corte e combina os genes dos dois pais:

        Pai1: [A A A | B B B]      ponto = 3
        Pai2: [C C C | D D D]
                    ↓
        Filho1: [A A A | D D D]
        Filho2: [C C C | B B B]

    Se o sorteio superar TAXA_CROSSOVER, os pais são copiados sem alteração.
    """
    if random.random() > TAXA_CROSSOVER:
        return deepcopy(pai1), deepcopy(pai2)

    ponto  = random.randint(1, TAMANHO_ROTA - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2


def aplicar_mutacao(individuo):
    """
    Mutação Uniforme por Gene.

    Cada gene é substituído por um movimento aleatório com probabilidade
    TAXA_MUTACAO. Introduz diversidade e evita convergência prematura.
    """
    return [
        random.randint(0, 3) if random.random() < TAXA_MUTACAO else gene
        for gene in individuo
    ]
