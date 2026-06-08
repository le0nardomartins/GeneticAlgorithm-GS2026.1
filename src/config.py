"""Parâmetros centrais do projeto — mude aqui para ajustar o comportamento."""

import random
import numpy as np
import os

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Mapa ---
TAMANHO_MAPA = 20

# Início e objetivo sorteados em cantos opostos
_MARGEM = 1
_CANTOS = [
    (_MARGEM,                    _MARGEM),
    (_MARGEM,                    TAMANHO_MAPA - 1 - _MARGEM),
    (TAMANHO_MAPA - 1 - _MARGEM, _MARGEM),
    (TAMANHO_MAPA - 1 - _MARGEM, TAMANHO_MAPA - 1 - _MARGEM),
]
_sorteio     = random.sample(_CANTOS, 2)
POS_INICIAL  = _sorteio[0]
POS_OBJETIVO = _sorteio[1]

LIVRE     = 0  # passagem normal
OBSTACULO = 1  # bloqueado
IRREGULAR = 2  # passa, mas gasta mais energia e desgasta o robô
PERIGO    = 3  # risco de destruição

QTD_OBSTACULOS  = 80
QTD_IRREGULARES = 55
QTD_PERIGOS     = 40

# Direções possíveis: cima, baixo, esquerda, direita
MOVIMENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
NOMES_MOV  = ["↑ cima", "↓ baixo", "← esq", "→ dir"]

# Energia gasta por tipo de célula
CUSTO_ENERGIA = {LIVRE: 1, IRREGULAR: 3, PERIGO: 5}

# --- Sistema de dano (zonas de perigo) ---
# Cada zona de perigo aumenta a chance de destruição no próximo.
# 1ª zona → 0% de chance → sai com 25% de dano
# 2ª zona → 25% de chance → sai com 50% de dano  e assim por diante
INCREMENTO_DANO       = 0.25
PENALIDADE_DESTRUICAO = 400.0
FATOR_ESCALA_DANO     = 8.0   # quanto mais danificado, mais cara é cada nova zona de perigo

# --- Sistema de desgaste (terreno irregular) ---
# Terreno irregular não destrói, mas acumula desgaste e fica cada vez mais custoso
INCREMENTO_DESGASTE   = 0.08  # incremento suave, menor que o de perigo
FATOR_ESCALA_IRREGULAR = 2.0  # escala leve — bem menos agressivo que o perigo

# --- Algoritmo Genético ---
TAMANHO_POPULACAO = 200
NUM_GERACOES      = 500
TAXA_CROSSOVER    = 0.85
TAXA_MUTACAO      = 0.10
TAMANHO_ROTA      = 120  # mapa denso exige cromossomo longo o suficiente para desviar de obstáculos
ELITISMO          = 10

# --- Pesos do fitness ---
PESO_DISTANCIA    = 10.0
PESO_COLISAO      = 20.0
PESO_FORA_MAPA    = 15.0
PESO_ENERGIA      = 0.4
PESO_PERIGO       = 8.0
PESO_IRREGULAR    = 2.0
PESO_COMPRIMENTO  = 1.0
PESO_REVISITA     = 10.0
PESO_REGRESSO     = 3.0   # baixo: em mapa denso o robô precisa dar voltas, e isso não é punido com força
RECOMPENSA_CHEGAR = 2000.0
