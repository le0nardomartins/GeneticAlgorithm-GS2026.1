"""
Visualizações com Matplotlib:
  1. plotar_mapa             — ambiente extraterrestre
  2. plotar_melhor_rota      — rota do robô sobre o mapa
  3. plotar_evolucao_fitness — curvas de fitness por geração
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

from src.config import (
    TAMANHO_MAPA, POS_INICIAL, POS_OBJETIVO,
    NUM_GERACOES, RECOMPENSA_CHEGAR,
)


# ── Helpers compartilhados ───────────────────────────────────────────

def _paleta_mapa():
    cmap   = mcolors.ListedColormap(["#e8e8e8", "#3a3a3a", "#e07b00", "#b30000"])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
    norm   = mcolors.BoundaryNorm(bounds, cmap.N)
    return cmap, norm


def _legenda_base():
    return [
        mpatches.Patch(color="#e8e8e8", label="Terreno livre"),
        mpatches.Patch(color="#3a3a3a", label="Obstáculo"),
        mpatches.Patch(color="#e07b00", label="Terreno irregular"),
        mpatches.Patch(color="#b30000", label="Área perigosa"),
        mpatches.Patch(color="lime",    label="Início (S)"),
        mpatches.Patch(color="gold",    label="Objetivo (G)"),
    ]


def _grade(ax):
    ax.set_xticks(np.arange(-0.5, TAMANHO_MAPA, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, TAMANHO_MAPA, 1), minor=True)
    ax.grid(which="minor", color="gray", linewidth=0.25)
    ax.tick_params(which="minor", size=0)


def _marcadores(ax):
    si, sj = POS_INICIAL
    ax.add_patch(plt.Circle((sj, si), 0.42, color="lime", zorder=5))
    ax.text(sj, si, "S", ha="center", va="center",
            fontsize=9, fontweight="bold", color="black", zorder=6)

    gi, gj = POS_OBJETIVO
    ax.add_patch(plt.Circle((gj, gi), 0.42, color="gold", zorder=5))
    ax.text(gj, gi, "G", ha="center", va="center",
            fontsize=9, fontweight="bold", color="black", zorder=6)


def _base_mapa(mapa):
    """Cria figura com o mapa colorido, grade e marcadores."""
    fig, ax = plt.subplots(figsize=(9, 9))
    cmap, norm = _paleta_mapa()
    ax.imshow(mapa, cmap=cmap, norm=norm, origin="upper", aspect="equal")
    _grade(ax)
    _marcadores(ax)
    ax.set_xlabel("Coluna", fontsize=10)
    ax.set_ylabel("Linha",  fontsize=10)
    return fig, ax


# ── Visualizações públicas ───────────────────────────────────────────

def plotar_mapa(mapa, titulo="Mapa do Ambiente Extraterrestre - Superfície de Marte"):
    """Visualização 1: mapa inicial com legenda de tipos de terreno."""
    fig, ax = _base_mapa(mapa)
    ax.legend(handles=_legenda_base(), loc="upper right",
              fontsize=8, framealpha=0.9, edgecolor="gray")
    ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    return fig


def plotar_melhor_rota(mapa, stats, fitness, geracao):
    """Visualização 2: melhor rota sobreposta ao mapa com setas de direção."""
    fig, ax = _base_mapa(mapa)

    caminho = stats["caminho"]
    if len(caminho) > 1:
        linhas  = [p[0] for p in caminho]
        colunas = [p[1] for p in caminho]

        ax.plot(colunas, linhas, "b-", linewidth=2.2, zorder=4, alpha=0.75)
        ax.scatter(colunas[1:-1], linhas[1:-1],
                   c="deepskyblue", s=18, zorder=5, alpha=0.9)

        passo_seta = max(1, len(caminho) // 12)
        for k in range(0, len(caminho) - 1, passo_seta):
            r1, c1 = caminho[k]
            r2, c2 = caminho[k + 1]
            ax.annotate("", xy=(c2, r2), xytext=(c1, r1),
                        arrowprops=dict(arrowstyle="->", color="navy",
                                        lw=1.6, mutation_scale=14),
                        zorder=6)

    if not stats["chegou"]:
        fl, fc = stats["posicao_final"]
        ax.add_patch(plt.Circle((fc, fl), 0.38, color="magenta", zorder=7))
        ax.text(fc, fl, "R", ha="center", va="center",
                fontsize=8, fontweight="bold", color="white", zorder=8)

    status = "OBJETIVO ALCANÇADO ✓" if stats["chegou"] else "Objetivo NÃO alcançado ✗"
    titulo = (f"Melhor Rota — Geração {geracao}  |  Fitness: {fitness:.1f}\n"
              f"Passos: {stats['passos']}  |  Energia: {stats['energia']}  |  {status}")
    ax.set_title(titulo, fontsize=11, fontweight="bold", pad=10)

    legenda = _legenda_base()
    legenda.append(mpatches.Patch(color="deepskyblue",
                                  label=f"Rota do robô ({stats['passos']} passos)"))
    if not stats["chegou"]:
        legenda.append(mpatches.Patch(color="magenta", label="Posição final (R)"))
    ax.legend(handles=legenda, loc="upper right",
              fontsize=8, framealpha=0.9, edgecolor="gray")

    plt.tight_layout()
    return fig


def plotar_evolucao_fitness(historico_melhor, historico_media, geracao_melhor):
    """
    Visualização 3: curvas de melhor fitness e fitness médio por geração.
    Marca com linha vertical a geração em que a melhor solução apareceu.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    geracoes = range(1, len(historico_melhor) + 1)

    ax.plot(geracoes, historico_melhor, "b-",  linewidth=2,
            label="Melhor fitness", zorder=3)
    ax.plot(geracoes, historico_media,  "r--", linewidth=1.5,
            label="Fitness médio",  alpha=0.75, zorder=2)

    ax.axvline(x=geracao_melhor, color="green", linestyle=":", linewidth=1.8,
               label=f"Melhor solução (Gen {geracao_melhor})", zorder=4)
    ax.scatter([geracao_melhor], [historico_melhor[geracao_melhor - 1]],
               color="green", s=100, zorder=5)

    ax.axhline(y=0, color="gray", linewidth=0.8, alpha=0.35)
    ax.axhline(y=RECOMPENSA_CHEGAR, color="gold", linestyle="--",
               linewidth=1.2, alpha=0.6,
               label=f"Limiar de chegada ({RECOMPENSA_CHEGAR:.0f})")

    ax.fill_between(geracoes, historico_melhor, historico_media,
                    alpha=0.08, color="blue")

    ax.annotate(f"  Gen 1\n  {historico_melhor[0]:.0f}",
                xy=(1, historico_melhor[0]), fontsize=8, color="navy")
    ax.annotate(f"  Gen {NUM_GERACOES}\n  {historico_melhor[-1]:.0f}",
                xy=(NUM_GERACOES, historico_melhor[-1]), fontsize=8, color="navy")

    ax.set_xlabel("Geração", fontsize=11)
    ax.set_ylabel("Fitness", fontsize=11)
    ax.set_title("Evolução do Fitness ao Longo das Gerações - Rover Genetic Navigator",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig
