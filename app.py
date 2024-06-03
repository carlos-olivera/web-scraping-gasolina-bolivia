import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import os
import time

class GetGasStations:
    def __init__(self):
        self.url = "https://biopetrol.com.bo/guiamobile/main/donde/134"
        
        # Obtener variables de entorno
        mongo_username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
        mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
        mongo_database = os.getenv('MONGO_INITDB_DATABASE')

        # Verificar que las variables de entorno estén definidas
        if not mongo_username or not mongo_password or not mongo_database:
            raise ValueError("Las variables de entorno MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD y MONGO_INITDB_DATABASE deben estar definidas.")
        
        print(f"Conectando a MongoDB con usuario: {mongo_username}, base de datos: {mongo_database}")
        
        self.mongo_client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@database:27017/")
        self.db = self.mongo_client[mongo_database]
        self.collection = self.db['surtidores']

    def updateGasStations(self):
        # Obtener el contenido HTML desde la URL
        response = requests.get(self.url)
        html_content = response.content

        # Parsear el contenido HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Verificar si se obtuvo contenido HTML
        if not html_content:
            print("Error: No se pudo obtener el contenido HTML.")
            return
        else:
            print("Contenido HTML obtenido exitosamente.")

        # Encontrar el contenedor principal
        container = soup.find('div', class_='container')

        # Verificar si se encontró el contenedor principal
        if not container:
            print("Error: No se encontró el contenedor principal.")
            return
        else:
            print("Contenedor principal encontrado.")

        # Lista para almacenar los datos de las gasolineras
        gas_stations = []

        # Encontrar todas las fichas de gasolineras
        gas_station_cards = container.select('div.btn-bio-app.rounded')

        # Verificar si se encontraron fichas de gasolineras
        if not gas_station_cards:
            print("Error: No se encontraron fichas de gasolineras.")
            return
        else:
            print(f"Se encontraron {len(gas_station_cards)} fichas de gasolineras.")

        for card in gas_station_cards:
            try:
                description = card.find('div', class_='col-12 m-0 p-0 text-center font-18 font-weight-bold bg-oscuro-1 py-2 mb-1 rounded-top').text.strip()
                
                # Obtener y convertir el valor de litros disponibles
                liters_available_str = card.find_all('div', class_='col-12 mx-0 px-4 text-right text-bio-appx text-dark')[0].text.strip()
                liters_available = float(liters_available_str.replace(' Lts.', '').replace(',', ''))
                
                # Obtener y convertir la fecha y hora de medición
                datetime_str = card.find_all('div', class_='col-12 mx-0 px-4 text-right text-bio-appx text-dark')[1].text.strip()
                datetime_measurement = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                
                # Obtener el texto de ubicación
                location_text = card.find('div', class_='px-1 col-12').text.strip()
                
                gas_station_data = {
                    'creationTime': datetime.now().isoformat(),
                    'description': description,
                    'value': liters_available,
                    'readdatetime': datetime_measurement.isoformat(),
                    'locationText': location_text
                }

                gas_stations.append(gas_station_data)
                
                print(f"Gasolinera encontrada: {description}, Litros: {liters_available}, Fecha y hora: {datetime_measurement}, Ubicación: {location_text}")
            except Exception as e:
                print(f"Error al procesar una ficha de gasolinera: {e}")

        # Insertar datos en MongoDB
        if gas_stations:
            self.collection.insert_many(gas_stations)
            print("Datos insertados en MongoDB.")

    def start(self):
        while True:
            self.updateGasStations()
            print("Esperando 15 minutos para la próxima actualización...")
            time.sleep(900)  # Esperar 900 segundos (15 minutos)

if __name__ == "__main__":
    print("Iniciando....")
    try:
        gas_stations_updater = GetGasStations()
        gas_stations_updater.start()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
