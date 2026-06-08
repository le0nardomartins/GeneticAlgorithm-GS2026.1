"""Gera o mapa do ambiente e garante que existe ao menos um caminho navegável."""

import random
import numpy as np
from collections import deque

from src.config import (
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    LIVRE, OBSTACULO, IRREGULAR, PERIGO,
    QTD_OBSTACULOS, QTD_IRREGULARES, QTD_PERIGOS,
)

_MAX_PERIGOS_NO_CAMINHO = 2  # o caminho mais curto pode ter no máximo 2 zonas de perigo


def _caminho_minimo(mapa):
    """BFS — encontra o caminho mais curto sem obstáculos, ou None se não existir."""
    pai  = {POS_INICIAL: None}
    fila = deque([POS_INICIAL])
    while fila:
        linha, coluna = fila.popleft()
        if (linha, coluna) == POS_OBJETIVO:
            caminho, pos = [], POS_OBJETIVO
            while pos is not None:
                caminho.append(pos)
                pos = pai[pos]
            return caminho[::-1]
        for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nl, nc = linha + dl, coluna + dc
            vizinho = (nl, nc)
            if (0 <= nl < TAMANHO_MAPA and 0 <= nc < TAMANHO_MAPA
                    and vizinho not in pai
                    and mapa[nl][nc] != OBSTACULO):
                pai[vizinho] = (linha, coluna)
                fila.append(vizinho)
    return None


def _gerar_mapa():
    mapa = np.zeros((TAMANHO_MAPA, TAMANHO_MAPA), dtype=int)

    # Área protegida ao redor do início e do objetivo (raio 2) — não recebe obstáculos
    protegidas = set()
    for origem in [POS_INICIAL, POS_OBJETIVO]:
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                r, c = origem[0] + dr, origem[1] + dc
                if 0 <= r < TAMANHO_MAPA and 0 <= c < TAMANHO_MAPA:
                    protegidas.add((r, c))

    disponiveis = [
        (r, c) for r in range(TAMANHO_MAPA) for c in range(TAMANHO_MAPA)
        if (r, c) not in protegidas
    ]
    random.shuffle(disponiveis)

    idx = 0
    for tipo, qtd in [(OBSTACULO, QTD_OBSTACULOS),
                      (IRREGULAR, QTD_IRREGULARES),
                      (PERIGO,    QTD_PERIGOS)]:
        for _ in range(qtd):
            if idx < len(disponiveis):
                r, c = disponiveis[idx]
                if mapa[r][c] == LIVRE:
                    mapa[r][c] = tipo
                idx += 1

    mapa[POS_INICIAL[0]][POS_INICIAL[1]]   = LIVRE
    mapa[POS_OBJETIVO[0]][POS_OBJETIVO[1]] = LIVRE
    return mapa


def criar_mapa():
    """Gera um mapa aleatório novo a cada execução, garantindo caminho válido."""
    random.seed()
    np.random.seed()

    tentativas = 0
    while True:
        tentativas += 1
        mapa    = _gerar_mapa()
        caminho = _caminho_minimo(mapa)

        if caminho is None:
            continue  # sem caminho — tenta de novo

        # Remove perigos excedentes no caminho mínimo
        perigos = [(r, c) for r, c in caminho if mapa[r][c] == PERIGO]
        for r, c in perigos[_MAX_PERIGOS_NO_CAMINHO:]:
            mapa[r][c] = LIVRE

        if tentativas > 1:
            print(f"      (mapa regenerado {tentativas}x até garantir caminho válido)")
        return mapa
