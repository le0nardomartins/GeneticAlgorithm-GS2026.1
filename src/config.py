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
TAMANHO_MAPA    = 20        # Grade N × N
POS_INICIAL     = (1,  1)   # Célula de partida  (linha, coluna)
POS_OBJETIVO    = (18, 18)  # Célula destino      (linha, coluna)

# Tipos de célula
LIVRE     = 0   # Terreno livre      — custo de energia: 1
OBSTACULO = 1   # Obstáculo          — bloqueia movimento
IRREGULAR = 2   # Terreno irregular  — custo de energia: 3
PERIGO    = 3   # Área de alto risco — custo de energia: 5

# Quantidade de cada tipo gerada no mapa
QTD_OBSTACULOS  = 45
QTD_IRREGULARES = 35
QTD_PERIGOS     = 20

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

# ── Algoritmo Genético ──────────────────────────────────────────────
TAMANHO_POPULACAO = 120   # Indivíduos por geração
NUM_GERACOES      = 200   # Total de gerações
TAXA_CROSSOVER    = 0.85  # Probabilidade de crossover
TAXA_MUTACAO      = 0.12  # Probabilidade de mutação por gene
TAMANHO_ROTA      = 75    # Genes (movimentos) por indivíduo
ELITISMO          = 6     # Melhores indivíduos preservados

# ── Pesos da função fitness ──────────────────────────────────────────
PESO_DISTANCIA    = 5.0    # Penalidade por distância até o objetivo
PESO_COLISAO      = 20.0   # Penalidade por colisão com obstáculo
PESO_FORA_MAPA    = 15.0   # Penalidade por tentativa fora dos limites
PESO_ENERGIA      = 0.4    # Penalidade por energia consumida
PESO_PERIGO       = 8.0    # Penalidade extra por área perigosa
PESO_COMPRIMENTO  = 0.2    # Penalidade pelo comprimento da rota
RECOMPENSA_CHEGAR = 1000.0 # Bônus por alcançar o objetivo
