# %%
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from tabulate import tabulate

# %%
def convolucao_espacial(imagem, kernel):
    return convolve2d(imagem, kernel, mode='same', boundary='symm')

def convolucao_frequencia(imagem, kernel):
    # Ajusta tamanhos para potência de 2 (melhora eficiência da FFT)
    linhas = cv2.getOptimalDFTSize(imagem.shape[0])
    colunas = cv2.getOptimalDFTSize(imagem.shape[1])
    
    # Aplica padding
    imagem_padded = cv2.copyMakeBorder(imagem, 0, linhas - imagem.shape[0], 
                                      0, colunas - imagem.shape[1], 
                                      cv2.BORDER_CONSTANT, value=0)
    kernel_padded = cv2.copyMakeBorder(kernel, 0, linhas - kernel.shape[0], 
                                      0, colunas - kernel.shape[1], 
                                      cv2.BORDER_CONSTANT, value=0)
    
    # Transformada de Fourier
    fft_im = np.fft.fft2(imagem_padded)
    fft_kernel = np.fft.fft2(kernel_padded)
    
    # Multiplicação no domínio da frequência
    fft_result = fft_im * fft_kernel
    
    # Transformada inversa
    result_padded = np.real(np.fft.ifft2(fft_result))
    
    # Remove padding
    return result_padded[:imagem.shape[0], :imagem.shape[1]]

# %%
imagem = cv2.imread('caminho para imagem', cv2.IMREAD_GRAYSCALE)  # Substitua por uma imagem sua
imagem = imagem.astype(np.float32) / 255.0

# %%
kernel_pequeno = np.ones((3, 3)) / 9.0  # Média 3x3
kernel_grande = np.ones((15, 15)) / 225.0  # Média 15x15
kernel_gaussiano = cv2.getGaussianKernel(15, 5) @ cv2.getGaussianKernel(15, 5).T

kernels = {
    "Pequeno (3x3)": kernel_pequeno,
    "Grande (15x15)": kernel_grande,
    "Gaussiano (15x15)": kernel_gaussiano
}

# %%
resultados = []
for nome, kernel in kernels.items():
    print(f"\nTestando kernel {nome}:")
    
    # Domínio espacial
    inicio = time.time()
    result_espacial = convolucao_espacial(imagem, kernel)
    tempo_espacial = time.time() - inicio
    
    # Domínio da frequência
    inicio = time.time()
    result_freq = convolucao_frequencia(imagem, kernel)
    tempo_freq = time.time() - inicio
    
    # Calcula diferença entre resultados
    diferenca = np.max(np.abs(result_espacial - result_freq))
    ganho = tempo_espacial / max(tempo_freq, 1e-9)  # Evita divisão por zero
    
    resultados.append((nome, tempo_espacial, tempo_freq, ganho, diferenca))
    
    print(f"Espacial: {tempo_espacial:.4f}s, Frequência: {tempo_freq:.4f}s")
    print(f"Ganho: {ganho:.1f}x, Diferença máxima: {diferenca:.6f}")


# %%
print("\nRESULTADOS COMPARATIVOS:")
tabela = []
headers = ["Kernel", "Espacial (s)", "Frequência (s)", "Ganho", "Diferença Máxima"]

for nome, esp, freq, ganho, diff in resultados:
    tabela.append([
        nome,
        f"{esp:.6f}",
        f"{freq:.6f}",
        f"{ganho:.1f}x",
        f"{diff:.6e}"
    ])

print(tabulate(tabela, headers=headers, tablefmt="grid"))

# %%
# Plota os tempos
plt.figure(figsize=(10, 6))
nomes = [r[0] for r in resultados]
tempos_esp = [r[1] for r in resultados]
tempos_freq = [r[2] for r in resultados]

x = np.arange(len(nomes))
width = 0.35

plt.bar(x - width/2, tempos_esp, width, label='Domínio Espacial')
plt.bar(x + width/2, tempos_freq, width, label='Domínio da Frequência')
plt.ylabel('Tempo (s)')
plt.title('Comparação de Desempenho de Convolução')
plt.xticks(x, nomes)
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()


