import requests

# URL base para la API
base_url = "https://open.canada.ca/data/api/action/"

# Lista de datasets a descargar (nombre y ID)
datasets_to_download = [
    {"title": "Crime Statistics - Incidents and rates for selected offences", "id": "47466568-c38d-8bb9-26d9-331079dad727"}
    
]

def download_dataset(dataset_id, title):
    endpoint = f"package_show?id={dataset_id}"
    response = requests.get(f"{base_url}{endpoint}")
    
    if response.status_code == 200:
        dataset_info = response.json()
        for resource in dataset_info['result']['resources']:
            if resource['format'].lower() == 'csv':
                csv_url = resource['url']
                csv_response = requests.get(csv_url)
                filename = f"{title.replace(' ', '_').lower()}.csv"
                with open(filename, 'wb') as file:
                    file.write(csv_response.content)
                print(f"{title} descargado como {filename}")
    else:
        print(f"Error al obtener el dataset {title}: {response.status_code}")

for dataset in datasets_to_download:
    download_dataset(dataset['id'], dataset['title'])