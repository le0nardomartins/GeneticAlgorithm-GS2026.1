"""
Simulação do robô seguindo uma rota (indivíduo) sobre o mapa.
"""

import random

from src.config import (
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    OBSTACULO, IRREGULAR, PERIGO,
    MOVIMENTOS, CUSTO_ENERGIA,
    INCREMENTO_DANO,
)


def simular_rota(individuo, mapa):
    """
    Executa a sequência de movimentos do indivíduo e coleta métricas.

    Regras de movimento:
    - Sair do mapa   → fora_mapa += 1, movimento ignorado.
    - Obstáculo      → colisoes += 1, movimento ignorado.
    - Célula já visitada → revisitas += 1 (movimento executado, mas penalizado).
    - Objetivo       → simulação encerrada imediatamente.

    Sistema de dano (células de perigo):
    - Ao pisar em PERIGO, primeiro verifica destruição com chance = nivel_dano.
    - Se sobreviver, acumula INCREMENTO_DANO (0.25 por célula).
    - Destruição encerra a missão imediatamente (destruido = True).

    Progressão de risco:
        1ª célula de perigo → 0%  de destruição → sai com 25% de dano
        2ª célula de perigo → 25% de destruição → sai com 50% de dano
        3ª célula de perigo → 50% de destruição → sai com 75% de dano
        4ª célula de perigo → 75% de destruição → sai com 100% de dano
        5ª célula de perigo → destruição garantida
    """
    linha, coluna = POS_INICIAL
    caminho   = [(linha, coluna)]
    visitadas = {(linha, coluna)}   # conjunto de células já pisadas

    colisoes    = 0
    fora_mapa   = 0
    energia     = 0
    irregulares = 0
    perigos     = 0
    passos      = 0
    revisitas   = 0
    chegou      = False
    destruido   = False
    nivel_dano  = 0.0   # 0.0 = intacto, 1.0 = completamente destruído

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

        linha, coluna = nl, nc
        passos += 1
        caminho.append((linha, coluna))
        energia += CUSTO_ENERGIA.get(tipo, 1)

        # Contar revisita antes de registrar a célula como visitada
        if (linha, coluna) in visitadas:
            revisitas += 1
        else:
            visitadas.add((linha, coluna))

        if tipo == IRREGULAR:
            irregulares += 1

        elif tipo == PERIGO:
            perigos += 1
            if random.random() < nivel_dano:
                destruido = True
                break
            nivel_dano = min(1.0, nivel_dano + INCREMENTO_DANO)

        if (linha, coluna) == POS_OBJETIVO:
            chegou = True
            break

    return {
        "posicao_final": (linha, coluna),
        "caminho":        caminho,
        "colisoes":       colisoes,
        "fora_mapa":      fora_mapa,
        "energia":        energia,
        "irregulares":    irregulares,
        "perigos":        perigos,
        "passos":         passos,
        "revisitas":      revisitas,
        "chegou":         chegou,
        "destruido":      destruido,
        "nivel_dano":     nivel_dano,
    }
