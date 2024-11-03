import requests

# URL base para la API
base_url = "https://open.canada.ca/data/api/action/"

# Endpoint para listar datasets
endpoint = "package_search"

# Hacemos una solicitud a la API
response = requests.get(f"{base_url}{endpoint}", params={"rows": 100})  # Podemos ajustar 'rows' según sea necesario

# Verificamos si la solicitud fue exitosa
if response.status_code == 200:
    datasets = response.json()
    # Mostramos los títulos de los primeros 10 datasets
    for dataset in datasets['result']['results']:
        print(f"Title: {dataset['title']}\nDescription: {dataset['notes']}\n")
else:
    print("Error al conectarse a la API:", response.status_code)
