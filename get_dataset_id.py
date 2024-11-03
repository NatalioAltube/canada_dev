import requests

# URL base para la API
base_url = "https://open.canada.ca/data/api/action/"

# Endpoint para buscar datasets
endpoint = "package_search"

# Título del dataset que estás buscando
search_query = "Crime Statistics - Incidents and rates for selected offences"

# Hacemos una solicitud a la API para buscar el dataset
response = requests.get(f"{base_url}{endpoint}", params={"q": search_query, "rows": 10})

if response.status_code == 200:
    datasets = response.json()
    for dataset in datasets['result']['results']:
        title = dataset['title']
        if search_query.lower() in title.lower():
            dataset_id = dataset['id']
            print(f"Title: {title}\nID: {dataset_id}\n")
else:
    print("Error al conectarse a la API:", response.status_code)
