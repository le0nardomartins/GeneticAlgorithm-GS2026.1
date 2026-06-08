import os
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")   # renderiza sem abrir janela
import matplotlib.pyplot as plt

from src.config import LIVRE, OBSTACULO, IRREGULAR, PERIGO, OUTPUT_DIR
from src.mapa import criar_mapa
from src.algoritmo import executar_algoritmo_genetico
from src.fitness import calcular_fitness
from src.visualizacao import plotar_painel_completo


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
    print("\n[0/5] Limpando pasta de saida...")
    limpar_output()

    # [1] Gerar mapa
    print("\n[1/5] Gerando mapa do ambiente extraterrestre...")
    mapa = criar_mapa()
    print(f"      Celulas livres      : {int(np.sum(mapa == LIVRE))}")
    print(f"      Obstaculos          : {int(np.sum(mapa == OBSTACULO))}")
    print(f"      Terrenos irregulares: {int(np.sum(mapa == IRREGULAR))}")
    print(f"      Areas perigosas     : {int(np.sum(mapa == PERIGO))}")

    # [2] Executar AG
    print("\n[2/5] Executando Algoritmo Genetico...\n")
    melhor_ind, melhor_stats, hist_melhor, hist_media, geracao_melhor = (
        executar_algoritmo_genetico(mapa)
    )

    melhor_fitness, _ = calcular_fitness(melhor_ind, mapa)

    # [3] Gerar painel unificado
    print("\n[3/5] Gerando painel unificado...")
    fig = plotar_painel_completo(
        mapa, melhor_stats, melhor_fitness, geracao_melhor,
        hist_melhor, hist_media,
    )

    # [4] Salvar painel
    print("\n[4/5] Salvando painel...")
    caminho = os.path.join(OUTPUT_DIR, "painel_completo.png")
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    print(f"      Salvo: {caminho}")

    # [5] Abrir imagem no visualizador padrão do sistema
    print("\n[5/5] Abrindo imagem...")
    plt.close(fig)
    os.startfile(os.path.abspath(caminho))

    print(f"\n  Arquivo salvo em: {OUTPUT_DIR}/painel_completo.png\n")


if __name__ == "__main__":
    main()
