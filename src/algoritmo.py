"""Loop principal do Algoritmo Genético."""

from copy import deepcopy

from src.config import (
    TAMANHO_POPULACAO, NUM_GERACOES, ELITISMO,
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    QTD_OBSTACULOS, QTD_IRREGULARES, QTD_PERIGOS,
    TAXA_CROSSOVER, TAXA_MUTACAO, TAMANHO_ROTA,
)
from src.individuo  import gerar_populacao
from src.fitness    import calcular_fitness
from src.operadores import selecionar_pais, aplicar_crossover, aplicar_mutacao


def _banner_inicio():
    print("\n" + "=" * 65)
    print("  ROVER GENETIC NAVIGATOR — Algoritmo Genético")
    print("=" * 65)
    print(f"  Mapa         : {TAMANHO_MAPA}×{TAMANHO_MAPA}")
    print(f"  Início       : {POS_INICIAL}    Objetivo: {POS_OBJETIVO}")
    print(f"  Obstáculos   : {QTD_OBSTACULOS}   "
          f"Irregulares: {QTD_IRREGULARES}   Perigos: {QTD_PERIGOS}")
    print(f"  Populacao    : {TAMANHO_POPULACAO}  Gerações: {NUM_GERACOES}")
    print(f"  Tamanho rota : {TAMANHO_ROTA} genes")
    print(f"  Crossover    : {TAXA_CROSSOVER}   "
          f"Mutação: {TAXA_MUTACAO}   Elitismo: {ELITISMO}")
    print("=" * 65)
    print(f"  {'Gen':>4}  {'Melhor Fit':>11}  {'Fit Médio':>10}  "
          f"{'Colisões':>9}  {'Energia':>7}  {'Dist':>4}  Chegou")
    print("-" * 65)


def _imprimir_geracao(gen, fit_melhor, fit_media, stats):
    dist   = (abs(stats["posicao_final"][0] - POS_OBJETIVO[0]) +
              abs(stats["posicao_final"][1] - POS_OBJETIVO[1]))
    status = "SIM ✓" if stats["chegou"] else ("DESTRUIDO" if stats["destruido"] else "NAO")
    dano   = f"{stats['nivel_dano']*100:.0f}%"
    print(f"  {gen:>4}  {fit_melhor:>11.2f}  {fit_media:>10.2f}  "
          f"{stats['colisoes']:>9}  {stats['energia']:>7}  "
          f"{dist:>4}  {status}  dano={dano}")


def _banner_resultado(fitness, stats, geracao):
    dist = (abs(stats["posicao_final"][0] - POS_OBJETIVO[0]) +
            abs(stats["posicao_final"][1] - POS_OBJETIVO[1]))
    print("\n" + "=" * 65)
    print("  RESULTADO FINAL")
    print("=" * 65)
    print(f"  Melhor Fitness         : {fitness:.4f}")
    print(f"  Geração da melhor rota : {geracao}")
    print(f"  Chegou ao objetivo     : {'SIM ✓' if stats['chegou'] else 'NÃO ✗'}")
    print(f"  Distância final        : {dist} células")
    print(f"  Energia consumida      : {stats['energia']} unidades")
    print(f"  Colisões               : {stats['colisoes']}")
    print(f"  Tentativas fora do mapa: {stats['fora_mapa']}")
    print(f"  Passos executados      : {stats['passos']}")
    print(f"  Terrenos irregulares   : {stats['irregulares']}")
    print(f"  Areas perigosas        : {stats['perigos']}")
    print(f"  Robo destruido         : {'SIM ✗' if stats['destruido'] else 'NAO ✓'}")
    print(f"  Nivel de dano final    : {stats['nivel_dano']*100:.0f}%")
    print(f"  Nivel de desgaste      : {stats['nivel_desgaste']*100:.0f}%")
    print("=" * 65)


def executar_algoritmo_genetico(mapa):
    """Roda todas as gerações e retorna o melhor indivíduo encontrado."""
    _banner_inicio()

    populacao = gerar_populacao()

    historico_melhor = []
    historico_media  = []

    melhor_ind_global   = None
    melhor_fit_global   = float("-inf")
    melhor_stats_global = None
    geracao_melhor      = 0

    for geracao in range(NUM_GERACOES):

        resultados = [calcular_fitness(ind, mapa) for ind in populacao]
        fitnesses  = [r[0] for r in resultados]
        stats_pop  = [r[1] for r in resultados]

        idx_melhor   = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
        fit_melhor   = fitnesses[idx_melhor]
        fit_media    = sum(fitnesses) / len(fitnesses)
        stats_melhor = stats_pop[idx_melhor]

        historico_melhor.append(fit_melhor)
        historico_media.append(fit_media)

        if fit_melhor > melhor_fit_global:
            melhor_fit_global   = fit_melhor
            melhor_ind_global   = deepcopy(populacao[idx_melhor])
            melhor_stats_global = deepcopy(stats_melhor)
            geracao_melhor      = geracao + 1

        if (geracao + 1) % 10 == 0 or geracao == 0:
            _imprimir_geracao(geracao + 1, fit_melhor, fit_media, stats_melhor)

        # Os melhores da geração passam direto para a próxima (elitismo)
        ordem = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)
        elite = [deepcopy(populacao[i]) for i in ordem[:ELITISMO]]

        nova_pop = elite[:]
        while len(nova_pop) < TAMANHO_POPULACAO:
            pai1 = selecionar_pais(populacao, fitnesses)
            pai2 = selecionar_pais(populacao, fitnesses)
            f1, f2 = aplicar_crossover(pai1, pai2)
            f1 = aplicar_mutacao(f1)
            f2 = aplicar_mutacao(f2)
            nova_pop.append(f1)
            if len(nova_pop) < TAMANHO_POPULACAO:
                nova_pop.append(f2)

        populacao = nova_pop

    _banner_resultado(melhor_fit_global, melhor_stats_global, geracao_melhor)
    return (melhor_ind_global, melhor_stats_global,
            historico_melhor, historico_media, geracao_melhor)
