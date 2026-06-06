"""
Configurações globais do Rover
Todos os parâmetros ajustáveis do projeto estão centralizados aqui
"""

import random
import numpy as np
import os

# ── Reprodutibilidade ───────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ── Saída ───────────────────────────────────────────────────────────
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Mapa ────────────────────────────────────────────────────────────
TAMANHO_MAPA = 20   # Grade N × N

# Início e objetivo sorteados aleatoriamente entre os 4 cantos do mapa.
# random.sample garante que nunca caem no mesmo canto.
_MARGEM = 1
_CANTOS = [
    (_MARGEM,              _MARGEM),               # superior-esquerdo
    (_MARGEM,              TAMANHO_MAPA - 1 - _MARGEM),  # superior-direito
    (TAMANHO_MAPA - 1 - _MARGEM, _MARGEM),               # inferior-esquerdo
    (TAMANHO_MAPA - 1 - _MARGEM, TAMANHO_MAPA - 1 - _MARGEM),  # inferior-direito
]
_sorteio     = random.sample(_CANTOS, 2)
POS_INICIAL  = _sorteio[0]
POS_OBJETIVO = _sorteio[1]

# Tipos de célula
LIVRE     = 0   # Terreno livre      — custo de energia: 1
OBSTACULO = 1   # Obstáculo          — bloqueia movimento
IRREGULAR = 2   # Terreno irregular  — custo de energia: 3
PERIGO    = 3   # Área de alto risco — custo de energia: 5

# Quantidade de cada tipo gerada no mapa
QTD_OBSTACULOS  = 100
QTD_IRREGULARES = 55
QTD_PERIGOS     = 40

# ── Movimentos ──────────────────────────────────────────────────────
# Cada gene do cromossomo é um inteiro 0-3 que indexa esta lista
MOVIMENTOS = [
    (-1,  0),   # 0 → cima
    ( 1,  0),   # 1 → baixo
    ( 0, -1),   # 2 → esquerda
    ( 0,  1),   # 3 → direita
]
NOMES_MOV = ["↑ cima", "↓ baixo", "← esq", "→ dir"]

# Custo de energia por tipo de terreno
CUSTO_ENERGIA = {LIVRE: 1, IRREGULAR: 3, PERIGO: 5}

# ── Sistema de dano ──────────────────────────────────────────────────
# A cada célula de perigo pisada:
#   1. Verifica destruição: chance = nivel_dano atual (0.0 → 1.0)
#   2. Se sobreviver: nivel_dano += INCREMENTO_DANO
INCREMENTO_DANO      = 0.35   # Dano acumulado por célula de perigo sobrevivida
PENALIDADE_DESTRUICAO = 400.0  # Penalidade extra no fitness se destruído

# ── Algoritmo Genético ──────────────────────────────────────────────
TAMANHO_POPULACAO = 200   # ↑120→200: mais diversidade genética
NUM_GERACOES      = 1000   # Número de gerações
TAXA_CROSSOVER    = 0.85  # Probabilidade de crossover
TAXA_MUTACAO      = 0.08  # ↓0.12→0.08: menos ruído em cromossomo mais longo
TAMANHO_ROTA      = 120 
ELITISMO          = 10    # ↑6→10: preserva mais soluções de qualidade

# ── Pesos da função fitness ──────────────────────────────────────────
PESO_DISTANCIA    = 10.0   # ↑5→10: gradiente mais forte em direção ao objetivo
PESO_COLISAO      = 20.0   # Penalidade por colisão com obstáculo
PESO_FORA_MAPA    = 15.0   # Penalidade por tentativa fora dos limites
PESO_ENERGIA      = 0.4    # Penalidade por energia consumida
PESO_PERIGO       = 8.0    # Penalidade extra por área perigosa
PESO_COMPRIMENTO  = 0.3    # ↑0.15→0.3: mais pressão para rotas mais curtas
PESO_REVISITA     = 6.0    # ↑3→6: penalidade mais forte para eliminar voltas desnecessárias
RECOMPENSA_CHEGAR = 2000.0 # Bônus dominante garante que chegar > não chegar
