import requests

def obtener_recetas_desde_api(query):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={query}'
    response = requests.get(url)
    return response.json()

recetas = obtener_recetas_desde_api('pasta')
print(recetas)