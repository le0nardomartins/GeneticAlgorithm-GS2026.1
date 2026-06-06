# Rover Genetic Navigator

Otimização de rotas para robô autônomo de inspeção espacial usando Algoritmos Genéticos.

---

## Instalação

**Pré-requisito:** Python 3.8 ou superior.

```bash
pip install -r requirements.txt
```

---

## Como usar

Execute a partir da raiz do projeto:

```bash
python main.py
```

A cada execução a pasta `output/` é limpa automaticamente e o novo arquivo é gerado.

---

## Imagem gerada

O projeto produz um único arquivo em `output/`:

### `painel_completo.png`

Painel unificado com 3 visualizações em uma só imagem:

**Linha superior esquerda — Mapa do Ambiente**

Mostra o mapa 20×20 do terreno extraterrestre antes de qualquer simulação.

| Cor | Tipo |
|---|---|
| Cinza claro | Terreno livre |
| Cinza escuro | Obstáculo (rocha / cratera) |
| Laranja | Terreno irregular (maior consumo de energia) |
| Vermelho | Área perigosa (risco de falha) |
| Verde | Posição inicial do robô (S) |
| Dourado | Objetivo da missão (G) |

---

**Linha superior direita — Melhor Rota**

Mostra a melhor rota encontrada pelo Algoritmo Genético desenhada sobre o mapa.

- **Linha azul** — caminho percorrido pelo robô
- **Setas** — direção de cada movimento
- **Pontos azuis claros** — células visitadas ao longo do trajeto
- **Círculo verde (S)** — ponto de partida
- **Círculo dourado (G)** — objetivo da missão
- **Círculo magenta (R)** — posição final caso o robô não tenha alcançado o objetivo

O título exibe o fitness, o número de passos, a energia consumida e se o objetivo foi alcançado.

---

**Linha inferior — Evolução do Fitness**

Mostra como a qualidade das rotas evoluiu ao longo das gerações.

- **Linha azul** — melhor fitness encontrado em cada geração
- **Linha vermelha tracejada** — fitness médio da população
- **Linha verde pontilhada** — geração em que a melhor solução global foi encontrada
- **Linha dourada tracejada** — limiar de referência para rotas que chegam ao objetivo

Quanto mais a linha azul se aproxima ou supera o limiar dourado, melhor o algoritmo se saiu na missão.
