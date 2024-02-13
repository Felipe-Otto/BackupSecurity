import pandas as pd
import difflib

# Exemplo de DataFrames
data1 = {'Name': ['Alice Park', 'Charlie Kang', 'Anna Choi', 'Mudei HEhe', 'Grace Shin',
                       'Henry Yoon', 'Adicionei hehe'],
              'Role': ['Data Analyst', 'Project Manager', 'Mudei hehe',
                       'Front-end Developer', 'HR Manager', 'Systems Analyst', 'add emprego novo']}

data2 = {'Name': ['Sophia Kim', 'David Lee', 'Dona Park', 'William Choi', 'Olivia Kim', 'Novo'],
               'Role': ['Business Analyst', 'Full-stack Developer', 'Data Analyst', 'Project Manager',
                        'Systems Analyst', 'Data Analyst']}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Ajustar o limiar de correspondência
limiar_correspondencia = 1  # Ajuste conforme necessário


# Função para encontrar correspondência
def encontrar_correspondencia(row, df, threshold):
    correspondencias = {}

    for coluna in df.columns:
        # Verificar se a coluna é do tipo str antes de aplicar a comparação de strings
        if pd.api.types.is_string_dtype(df[coluna]):
            correspondencias[coluna] = difflib.get_close_matches(row[coluna], df[coluna], n=1, cutoff=threshold)
        else:
            correspondencias[coluna] = [row[coluna]]

    # Selecionar a melhor correspondência para cada coluna se existir
    melhor_correspondencia = {coluna: correspondencias[coluna][0] if correspondencias[coluna] else None for coluna in
                              df.columns}

    return melhor_correspondencia


# Aplicar a função para encontrar correspondências
df1[['Correspondencia_' + coluna for coluna in df1.columns]] = df1.apply(encontrar_correspondencia, df=df2, axis=1,
                                                                         threshold=limiar_correspondencia,
                                                                         result_type='expand')

# Exibir o resultado
print(df1)