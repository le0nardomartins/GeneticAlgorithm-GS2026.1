"""
Geração do mapa 2D do ambiente extraterrestre.
"""

import random
import numpy as np

from src.config import (
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    LIVRE, OBSTACULO, IRREGULAR, PERIGO,
    QTD_OBSTACULOS, QTD_IRREGULARES, QTD_PERIGOS,
)


def criar_mapa():
    """
    Gera a grade N x N com obstáculos, terrenos irregulares e áreas perigosas.

    Tipos de célula:
        0  →  terreno livre
        1  →  obstáculo (bloqueia passagem)
        2  →  terreno irregular (custo energético maior)
        3  →  área perigosa (penalidade extra de falha)

    Uma área de segurança de raio 2 é mantida ao redor do início e do
    objetivo para garantir que o robô possa partir e chegar sem bloqueios.
    """
    mapa = np.zeros((TAMANHO_MAPA, TAMANHO_MAPA), dtype=int)

    # Proteger entorno do início e do objetivo (raio 2)
    protegidas = set()
    for origem in [POS_INICIAL, POS_OBJETIVO]:
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                r, c = origem[0] + dr, origem[1] + dc
                if 0 <= r < TAMANHO_MAPA and 0 <= c < TAMANHO_MAPA:
                    protegidas.add((r, c))

    disponiveis = [
        (r, c)
        for r in range(TAMANHO_MAPA)
        for c in range(TAMANHO_MAPA)
        if (r, c) not in protegidas
    ]
    random.shuffle(disponiveis)

    idx = 0

    for _ in range(QTD_OBSTACULOS):
        if idx < len(disponiveis):
            r, c = disponiveis[idx]
            mapa[r][c] = OBSTACULO
            idx += 1

    for _ in range(QTD_IRREGULARES):
        if idx < len(disponiveis):
            r, c = disponiveis[idx]
            if mapa[r][c] == LIVRE:
                mapa[r][c] = IRREGULAR
            idx += 1

    for _ in range(QTD_PERIGOS):
        if idx < len(disponiveis):
            r, c = disponiveis[idx]
            if mapa[r][c] == LIVRE:
                mapa[r][c] = PERIGO
            idx += 1

    # Garantir que início e objetivo permanecem livres
    mapa[POS_INICIAL[0]][POS_INICIAL[1]]   = LIVRE
    mapa[POS_OBJETIVO[0]][POS_OBJETIVO[1]] = LIVRE

    return mapa
