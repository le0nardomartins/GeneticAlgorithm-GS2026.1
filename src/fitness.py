"""Calcula o fitness de uma rota — quanto maior, melhor."""

from src.config import (
    POS_OBJETIVO,
    PESO_DISTANCIA, PESO_COLISAO, PESO_FORA_MAPA,
    PESO_ENERGIA, PESO_PERIGO, PESO_IRREGULAR,
    PESO_COMPRIMENTO, PESO_REVISITA, PESO_REGRESSO,
    RECOMPENSA_CHEGAR, PENALIDADE_DESTRUICAO,
)
from src.simulacao import simular_rota


def calcular_fitness(individuo, mapa):
    """Simula a rota e converte as métricas em um único valor de fitness."""
    stats = simular_rota(individuo, mapa)

    pl, pc = stats["posicao_final"]
    gl, gc = POS_OBJETIVO
    distancia = abs(pl - gl) + abs(pc - gc)

    fitness  = -PESO_DISTANCIA  * distancia
    fitness -= PESO_COLISAO     * stats["colisoes"]
    fitness -= PESO_FORA_MAPA   * stats["fora_mapa"]
    fitness -= PESO_ENERGIA     * stats["energia"]
    fitness -= PESO_PERIGO      * stats["custo_perigo_ponderado"]
    fitness -= PESO_IRREGULAR   * stats["custo_irregular_ponderado"]
    fitness -= PESO_COMPRIMENTO * stats["passos"]
    fitness -= PESO_REVISITA    * stats["revisitas"]
    fitness -= PESO_REGRESSO    * stats["passos_regressivos"]

    if stats["destruido"]:
        fitness -= PENALIDADE_DESTRUICAO

    if stats["chegou"]:
        fitness += RECOMPENSA_CHEGAR

    return fitness, stats
