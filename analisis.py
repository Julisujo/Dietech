import pandas as pd

def analizar_csv(ruta_csv):
    df = pd.read_csv(ruta_csv)
    print(df.head())
    print(df.describe())
    print(df['tipo'].value_counts())
    recetas_bajas_en_calorias = df[df['calorias'] < 500]
    print(recetas_bajas_en_calorias)
    media_calorias_por_categoria = df.groupby('categoria')['calorias'].mean()
    print(media_calorias_por_categoria)

analizar_csv('ruta/a/tu/archivo.csv')