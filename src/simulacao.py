"""
Simulação do robô seguindo uma rota (indivíduo) sobre o mapa.
"""

from src.config import (
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    OBSTACULO, IRREGULAR, PERIGO,
    MOVIMENTOS, CUSTO_ENERGIA,
)


def simular_rota(individuo, mapa):
    """
    Executa a sequência de movimentos do indivíduo e coleta métricas.

    Regras:
    - Tentativa de sair do mapa  → fora_mapa += 1, movimento ignorado.
    - Colisão com obstáculo      → colisoes += 1, movimento ignorado.
    - Chegada ao objetivo        → simulação encerrada imediatamente.

    Retorna um dicionário com todas as métricas operacionais.
    """
    linha, coluna = POS_INICIAL
    caminho = [(linha, coluna)]

    colisoes    = 0
    fora_mapa   = 0
    energia     = 0
    irregulares = 0
    perigos     = 0
    passos      = 0
    chegou      = False

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

        if tipo == IRREGULAR:
            irregulares += 1
        elif tipo == PERIGO:
            perigos += 1

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
        "chegou":         chegou,
    }
