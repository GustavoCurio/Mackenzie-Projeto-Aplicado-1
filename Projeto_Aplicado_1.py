import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS REAIS
# -------------------------------------------------------------------

df = pd.read_csv('contratos_aet.csv', sep=';', encoding='latin1')

# -------------------------------------------------------------------
# 2. TRATAMENTO LGPD E LIMPEZA DE DADOS
# -------------------------------------------------------------------
if 'Nome_Cliente' in df.columns:
    df['Nome_Cliente_Anonimo'] = ['Cliente_' + str(i + 1) for i in range(len(df))]
    # Removi a coluna original com os nomes verdadeiros para evitar vazamentos
    df = df.drop(columns=['Nome_Cliente'])

if 'Data_Solicitacao' in df.columns and 'Data_Assinatura' in df.columns:
    df['Data_Solicitacao'] = pd.to_datetime(df['Data_Solicitacao'], format='%d/%m/%Y', errors='coerce')
    df['Data_Assinatura'] = pd.to_datetime(df['Data_Assinatura'], format='%d/%m/%Y', errors='coerce')

    df['Tempo_Total_Dias'] = (df['Data_Assinatura'] - df['Data_Solicitacao']).dt.days

# Remove linhas onde não foi possível calcular o tempo (ex: contrato ainda não assinado)
df = df.dropna(subset=['Tempo_Total_Dias'])

# -------------------------------------------------------------------
# 3. ANÁLISE EXPLORATÓRIA (ESTATÍSTICA DESCRITIVA)
# -------------------------------------------------------------------
print("--- Dimensões do Dataset Pós-Limpeza ---")
print(f"Total de Contratos Analisados: {df.shape[0]}")

print("\n--- Resumo Estatístico do Tempo de Aprovação (Gargalos) ---")
print(df[['Tempo_Total_Dias']].describe())

# -------------------------------------------------------------------
# 4. VISUALIZAÇÃO GRÁFICA DOS RESULTADOS
# -------------------------------------------------------------------
sns.set_theme(style="whitegrid")

# Boxplot: Mostra a variação e aponta as anomalias (outliers) no tempo
plt.figure(figsize=(10, 6))
sns.boxplot(x='Tipo_Contrato', y='Tempo_Total_Dias', data=df, hue='Tipo_Contrato', palette='Set2', legend=False)
plt.title('AET Consultoria: Distribuição do Tempo de Aprovação por Área')
plt.xlabel('Tipo de Contrato')
plt.ylabel('Tempo Total (Dias)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Histograma: Mostra a volumetria geral
plt.figure(figsize=(8, 5))
sns.histplot(df['Tempo_Total_Dias'], bins=30, kde=True, color='indigo')
plt.title('AET Consultoria: Frequência do Tempo de Aprovação')
plt.xlabel('Quantidade de Dias')
plt.ylabel('Volume de Contratos')
plt.show()