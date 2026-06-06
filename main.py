import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from src.config import LIVRE, OBSTACULO, IRREGULAR, PERIGO, OUTPUT_DIR
from src.mapa import criar_mapa
from src.algoritmo import executar_algoritmo_genetico
from src.fitness import calcular_fitness
from src.visualizacao import plotar_mapa, plotar_melhor_rota, plotar_evolucao_fitness


def limpar_output():
    """Remove todos os arquivos da pasta output antes de cada execucao."""
    arquivos = glob.glob(os.path.join(OUTPUT_DIR, "*"))
    removidos = [f for f in arquivos if os.path.isfile(f)]
    for arquivo in removidos:
        os.remove(arquivo)
    if removidos:
        print(f"      {len(removidos)} arquivo(s) removido(s) de {OUTPUT_DIR}/")
    else:
        print(f"      Pasta {OUTPUT_DIR}/ ja estava vazia.")


def main():
    # [0] Limpar outputs anteriores
    print("\n[0/6] Limpando pasta de saida...")
    limpar_output()

    # [1] Gerar mapa
    print("\n[1/6] Gerando mapa do ambiente extraterrestre...")
    mapa = criar_mapa()
    print(f"      Celulas livres      : {int(np.sum(mapa == LIVRE))}")
    print(f"      Obstaculos          : {int(np.sum(mapa == OBSTACULO))}")
    print(f"      Terrenos irregulares: {int(np.sum(mapa == IRREGULAR))}")
    print(f"      Areas perigosas     : {int(np.sum(mapa == PERIGO))}")

    # [2] Mapa inicial
    print("\n[2/6] Gerando visualizacao do mapa inicial...")
    fig_mapa = plotar_mapa(mapa)
    caminho_mapa = os.path.join(OUTPUT_DIR, "mapa_inicial.png")
    fig_mapa.savefig(caminho_mapa, dpi=150, bbox_inches="tight")
    print(f"      Salvo: {caminho_mapa}")

    # [3] Executar AG
    print("\n[3/6] Executando Algoritmo Genetico...\n")
    melhor_ind, melhor_stats, hist_melhor, hist_media, geracao_melhor = (
        executar_algoritmo_genetico(mapa)
    )

    melhor_fitness, _ = calcular_fitness(melhor_ind, mapa)

    # [4] Melhor rota
    print("\n[4/6] Gerando visualizacao da melhor rota...")
    fig_rota = plotar_melhor_rota(mapa, melhor_stats, melhor_fitness, geracao_melhor)
    caminho_rota = os.path.join(OUTPUT_DIR, "melhor_rota.png")
    fig_rota.savefig(caminho_rota, dpi=150, bbox_inches="tight")
    print(f"      Salvo: {caminho_rota}")

    # [5] Evolucao do fitness
    print("\n[5/6] Gerando grafico de evolucao do fitness...")
    fig_ev = plotar_evolucao_fitness(hist_melhor, hist_media, geracao_melhor)
    caminho_ev = os.path.join(OUTPUT_DIR, "evolucao_fitness.png")
    fig_ev.savefig(caminho_ev, dpi=150, bbox_inches="tight")
    print(f"      Salvo: {caminho_ev}")

    # [6] Exibir
    print("\n[6/6] Exibindo graficos...")
    plt.show()

    print(f"\n  Arquivos salvos em: {OUTPUT_DIR}/")
    print("    - mapa_inicial.png")
    print("    - melhor_rota.png")
    print("    - evolucao_fitness.png\n")


if __name__ == "__main__":
    main()
