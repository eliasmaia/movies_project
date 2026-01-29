import requests

class TMDBClient:

    IMG_BASE_URL = "https://image.tmdb.org/t/p"

    def __init__(self, token):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }
        self.timeout = 10
    
    def _get_image_url(self, path, size="w500"):
        return f"{self.IMG_BASE_URL}/{size}{path}" if path else None

    def search_movie(self, title, year):
        url = f"{self.base_url}/search/movie"
        params = {"query": title, "year": year, "language": "pt-BR"}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            results = response.json().get('results', [])
            if results:
                    movie = results[0]
                    return {
                        "tmdb_id": movie.get("id"),
                        "title_original": movie.get("original_title"),
                        "poster_url": self._get_image_url(movie.get('poster_path'))
                    }
        except requests.RequestException:
            return None
        return None
    
    def get_movie_details(self, movie_id):
        if not movie_id: return None

        url = f"{self.base_url}/movie/{movie_id}"
        params = {"language": "pt-BR"}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()

                return {
                    "title_pt": data.get("title"),
                    "original_title": data.get("original_title"),
                    "runtime": data.get("runtime", 0),
                    "tagline": data.get("tagline", ""),
                    "genres": ", ".join([g['name'] for g in data.get('genres', [])]),
                    "backdrop_url": self._get_image_url(data.get('backdrop_path')),
                    "poster_url": self._get_image_url(data.get('poster_path'))
                }
        except requests.RequestException:
                return None
        return None
    
    def get_movie_director(self, movie_id):
        if not movie_id: return "Desconhecido"

        url = f"{self.base_url}/movie/{movie_id}/credits"
        
        try:             
            response = requests.get(url, headers=self.headers)
    
            if response.status_code == 200:
                crew = response.json().get('crew', [])
                directors = [m['name'] for m in crew if m['job'] == 'Director']
                return ", ".join(directors) if directors else "Desconhecido"
        except requests.Request.Exception:
             pass
        return "Desconhecido"