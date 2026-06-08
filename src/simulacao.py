"""Simula o robô percorrendo uma rota e coleta as métricas de desempenho."""

import random

from src.config import (
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    OBSTACULO, IRREGULAR, PERIGO,
    MOVIMENTOS, CUSTO_ENERGIA,
    INCREMENTO_DANO, FATOR_ESCALA_DANO,
    INCREMENTO_DESGASTE, FATOR_ESCALA_IRREGULAR,
)

_GL, _GC = POS_OBJETIVO


def simular_rota(individuo, mapa):
    """Executa os genes do indivíduo e retorna todas as métricas da rota."""
    linha, coluna = POS_INICIAL
    caminho   = [(linha, coluna)]
    visitadas = {(linha, coluna)}

    colisoes               = 0
    fora_mapa              = 0
    energia                = 0
    irregulares            = 0
    perigos                = 0
    custo_perigo_ponderado    = 0.0
    custo_irregular_ponderado = 0.0
    passos                 = 0
    revisitas              = 0
    passos_regressivos     = 0
    chegou                 = False
    destruido              = False
    nivel_dano             = 0.0  # sobe com zonas de perigo, pode causar destruição
    nivel_desgaste         = 0.0  # sobe com terreno irregular, só aumenta o custo

    for gene in individuo:
        dl, dc = MOVIMENTOS[gene]
        nl, nc = linha + dl, coluna + dc

        if not (0 <= nl < TAMANHO_MAPA and 0 <= nc < TAMANHO_MAPA):
            fora_mapa += 1
            continue

        tipo = mapa[nl][nc]

        if tipo == OBSTACULO:
            colisoes += 1
            continue

        dist_antes = abs(linha - _GL) + abs(coluna - _GC)
        linha, coluna = nl, nc
        passos += 1
        caminho.append((linha, coluna))
        energia += CUSTO_ENERGIA.get(tipo, 1)

        if abs(linha - _GL) + abs(coluna - _GC) >= dist_antes:
            passos_regressivos += 1

        if (linha, coluna) in visitadas:
            revisitas += 1
        else:
            visitadas.add((linha, coluna))

        if tipo == IRREGULAR:
            irregulares += 1
            # Custo cresce levemente a cada célula irregular acumulada
            custo_irregular_ponderado += 1.0 + nivel_desgaste * FATOR_ESCALA_IRREGULAR
            nivel_desgaste = min(1.0, nivel_desgaste + INCREMENTO_DESGASTE)

        elif tipo == PERIGO:
            perigos += 1
            # Robô já danificado paga muito mais por entrar em nova zona de risco
            custo_perigo_ponderado += 1.0 + nivel_dano * FATOR_ESCALA_DANO
            if random.random() < nivel_dano:
                destruido = True
                break
            nivel_dano = min(1.0, nivel_dano + INCREMENTO_DANO)

        if (linha, coluna) == POS_OBJETIVO:
            chegou = True
            break

    return {
        "posicao_final":             (linha, coluna),
        "caminho":                    caminho,
        "colisoes":                   colisoes,
        "fora_mapa":                  fora_mapa,
        "energia":                    energia,
        "irregulares":                irregulares,
        "perigos":                    perigos,
        "custo_perigo_ponderado":     custo_perigo_ponderado,
        "custo_irregular_ponderado":  custo_irregular_ponderado,
        "passos":                     passos,
        "revisitas":                  revisitas,
        "passos_regressivos":         passos_regressivos,
        "chegou":                     chegou,
        "destruido":                  destruido,
        "nivel_dano":                 nivel_dano,
        "nivel_desgaste":             nivel_desgaste,
    }
