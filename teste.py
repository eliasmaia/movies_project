import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TMDB_TOKEN')

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "accept": "application/json"
}

def get_movie_details(titulo, ano):
    url = "http://api.themoviedb.org/3/search/movie"
    params = {"query": titulo, "year": ano, "language": "pt-BR"}

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Erro na API: {response.status_code}")
            return None

        # if response.status_code == 200:
        results = response.json().get('results')
        if results:
            movie = results[0]
            return {
                'genero_ids': movie.get('genre_ids'),
                'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
                'id_tmdb': movie.get('id')
            }
        else:
            print(f"Filme nao encontrado:{titulo}")
            return None
            # return None
    except Exception as e:
        print(f"Erro de conexão {e}")
        return None
    


df = pd.read_csv("movies_watched.csv", skipinitialspace=True)

posters = []
ids = []

print("Iniciando enriquecimento de dados")

for index, row in df.iterrows():
    titulo = row['title']
    ano = row['launching_year']

    print(f"[{index + 1}/{len(df)}] Buscando: {titulo} ({ano})...")

    detalhes = get_movie_details(titulo, ano)

    if detalhes:
        posters.append(detalhes['poster'])
        ids.append(detalhes['id_tmdb'])
    else:
        posters.append(None)
        ids.append(None)

    time.sleep(0.2)

    
df['poster_url'] = posters
df['tmdb_id'] = ids

df.to_csv('meus_filmes_enriquecidos.csv', index=False)
print("\nSucesso! Arquivo 'meus_filmes_enriquecidos.csv' gerado." )
