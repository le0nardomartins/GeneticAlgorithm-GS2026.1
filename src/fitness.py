"""
Função fitness: avalia a qualidade de uma rota (indivíduo).
"""

from src.config import (
    POS_OBJETIVO,
    PESO_DISTANCIA, PESO_COLISAO, PESO_FORA_MAPA,
    PESO_ENERGIA, PESO_PERIGO, PESO_COMPRIMENTO,
    RECOMPENSA_CHEGAR,
)
from src.simulacao import simular_rota


def calcular_fitness(individuo, mapa):
    """
    Calcula o fitness de um indivíduo e retorna também as métricas da rota.

    Fórmula:
        fitness = - PESO_DISTANCIA   x distância_manhattan
                  - PESO_COLISAO     x colisões
                  - PESO_FORA_MAPA   x tentativas_fora_mapa
                  - PESO_ENERGIA     x energia_consumida
                  - PESO_PERIGO      x áreas_perigosas
                  - PESO_COMPRIMENTO x passos
                  + RECOMPENSA_CHEGAR   (somente se chegou ao objetivo)

    Quanto MAIOR o valor, MELHOR a rota.

    Componentes:
    - Distância:   pressiona o AG a aproximar o robô do destino.
    - Chegada:     bônus dominante que prioriza rotas completas.
    - Colisões:    representam dano físico → penalidade alta.
    - Fora do mapa: rota inválida → penalidade moderada.
    - Energia:     missão espacial exige frugalidade → penalidade leve.
    - Perigo:      risco sistêmico à integridade do robô.
    - Comprimento: desempata rotas de mesma qualidade, preferindo as curtas.
    """
    stats = simular_rota(individuo, mapa)

    pl, pc = stats["posicao_final"]
    gl, gc = POS_OBJETIVO
    distancia = abs(pl - gl) + abs(pc - gc)

    fitness  = -PESO_DISTANCIA   * distancia
    fitness -= PESO_COLISAO      * stats["colisoes"]
    fitness -= PESO_FORA_MAPA    * stats["fora_mapa"]
    fitness -= PESO_ENERGIA      * stats["energia"]
    fitness -= PESO_PERIGO       * stats["perigos"]
    fitness -= PESO_COMPRIMENTO  * stats["passos"]

    if stats["chegou"]:
        fitness += RECOMPENSA_CHEGAR

    return fitness, stats
