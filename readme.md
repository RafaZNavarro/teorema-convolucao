# Demonstração do Teorema da Convolução - Análise de Desempenho

Este programa compara o desempenho da convolução no domínio espacial versus no domínio da frequência, ilustrando o ganho computacional do Teorema da Convolução.

## Funcionalidades Principais

- Implementação de convolução nos domínios espacial e de frequência
- Comparação de desempenho para diferentes kernels
- Análise de precisão numérica entre os métodos
- Visualização gráfica dos tempos de execução
- Tabela comparativa dos resultados

## Requisitos

- Python 3.6+
- Bibliotecas:
  - OpenCV (cv2)
  - NumPy
  - SciPy
  - Matplotlib
  - Tabulate

Instale as dependências com:
pip install opencv-python numpy scipy matplotlib tabulate

## Como Usar

1. Coloque sua imagem no diretório do projeto
2. Atualize o caminho da imagem no código:
   imagem = cv2.imread('caminho_para_imagem', cv2.IMREAD_GRAYSCALE)
3. Execute o script

## Métodos Implementados

1. Convolução Espacial:
   - Implementada com convolve2d do SciPy
   - Processamento direto no domínio espacial
   - Complexidade: O(n²m²) para imagem n×n e kernel m×m

2. Convolução por FFT:
   - Implementa o Teorema da Convolução
   - Usa transformada de Fourier para operação no domínio da frequência
   - Complexidade: O(n² log n)
   - Inclui padding para tamanhos otimizados

## Kernels Testados

1. Pequeno (3x3): Kernel de média 3×3
2. Grande (15x15): Kernel de média 15×15  
3. Gaussiano (15x15): Kernel gaussiano com σ=5

## Saídas do Programa

1. Tabela comparativa contendo:
   - Tempos de execução para cada método
   - Ganho computacional
   - Diferença máxima entre os resultados

2. Gráfico de barras comparando:
   - Tempos no domínio espacial
   - Tempos no domínio da frequência

## Análise Esperada

1. Para kernels pequenos (3x3):
   - Convolução espacial mais rápida
   - Overhead da FFT não compensa

2. Para kernels grandes (15x15):
   - Convolução por FFT significativamente mais rápida
   - Ganhos de 5-15x são típicos

3. Precisão:
   - Diferenças na ordem de 1e-5 a 1e-7
   - Causadas por arredondamentos numéricos

## Exemplo de Saída

+------------------+--------------+----------------+-------+------------------+
| Kernel           | Espacial (s) | Frequência (s) | Ganho | Diferença Máxima |
+==================+==============+================+=======+==================+
| Pequeno (3x3)    |     0.003521 |       0.009824 |   0.4x|       1.19209e-07|
+------------------+--------------+----------------+-------+------------------+
| Grande (15x15)   |     0.251674 |       0.017892 |  14.1x|       1.49012e-07|
+------------------+--------------+----------------+-------+------------------+
| Gaussiano (15x15)|     0.276543 |       0.018127 |  15.3x|       1.78814e-07|
+------------------+--------------+----------------+-------+------------------+

## Aplicações

- Processamento de imagens
- Sistemas de visão computacional
- Análise de desempenho de algoritmos
- Demonstração do Teorema da Convolução