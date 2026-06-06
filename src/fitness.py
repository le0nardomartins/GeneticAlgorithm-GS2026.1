"""
Função fitness: avalia a qualidade de uma rota (indivíduo).
"""

from src.config import (
    POS_OBJETIVO,
    PESO_DISTANCIA, PESO_COLISAO, PESO_FORA_MAPA,
    PESO_ENERGIA, PESO_PERIGO, PESO_COMPRIMENTO, PESO_REVISITA,
    RECOMPENSA_CHEGAR, PENALIDADE_DESTRUICAO,
)
from src.simulacao import simular_rota


def calcular_fitness(individuo, mapa):
    """
    Calcula o fitness de um indivíduo e retorna também as métricas da rota.

    Fórmula:
        fitness = - PESO_DISTANCIA      × distância_manhattan
                  - PESO_COLISAO        × colisões
                  - PESO_FORA_MAPA      × tentativas_fora_mapa
                  - PESO_ENERGIA        × energia_consumida
                  - PESO_PERIGO         × áreas_perigosas
                  - PESO_COMPRIMENTO    × passos
                  - PENALIDADE_DESTRUICAO  (se destruído)
                  + RECOMPENSA_CHEGAR      (se chegou ao objetivo)

    Quanto MAIOR o valor, MELHOR a rota.

    Componentes:
    - Distância:    gradiente que puxa o robô em direção ao objetivo.
    - Chegada:      bônus dominante — chegar sempre supera não chegar.
    - Destruído:    penalidade pesada — missão encerrada por dano total.
    - Colisões:     dano físico ao robô → penalidade alta.
    - Fora do mapa: rota inválida → penalidade moderada.
    - Energia:      missão espacial exige frugalidade → penalidade leve.
    - Perigo:       cada célula perigosa atravessada aumenta risco futuro.
    - Comprimento:  desempata rotas de mesma qualidade, preferindo as curtas.
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
    fitness -= PESO_REVISITA     * stats["revisitas"]

    if stats["destruido"]:
        fitness -= PENALIDADE_DESTRUICAO

    if stats["chegou"]:
        fitness += RECOMPENSA_CHEGAR

    return fitness, stats
