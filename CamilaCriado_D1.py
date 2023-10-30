import requests
import pandas as pd
import configparser
import os

def make_request_and_create_dataframe(api_key, dep_icao, arr_iata, _fields):
    try:
        parameters = {
            'api_key': api_key,
            'dep_icao': dep_icao,
            'arr_iata': arr_iata,
            '_fields': _fields
        }

        url = "https://airlabs.co/api/v9/flights"

        response = requests.get(url, params=parameters)
        response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa

        data = response.json()

        selected_columns = ["reg_number", "flag", "lat", "lng", "alt", "speed", "flight_number", "airline_iata", "updated", "status", "dep_iata", "arr_iata"]
        
        df = pd.DataFrame(data["response"], columns=selected_columns)

        return df
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return None
    except KeyError as e:
        print(f"Error al procesar la respuesta JSON: {e}")
        return None

if __name__ == "__main__":
    # Obtenemos la ubicación del directorio actual
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Combinamos la ubicación actual con la ruta relativa al archivo config.ini
    config_file_path = os.path.join(current_directory, 'config', 'config.ini')

    # Creamos un objeto ConfigParser y leemos la API key desde el archivo config.ini
    config = configparser.ConfigParser()
    config.read(config_file_path)

    api_key = config['API']['api_key']
    dep_icao = 'SAEZ'
    arr_iata = 'MAD'
    _fields = 'reg_number,flag,lat,lng,alt,speed,flight_number,airline_iata,updated,status,arr_iata,dep_iata'

    result_df = make_request_and_create_dataframe(api_key, dep_icao, arr_iata, _fields)

    if result_df is not None:
        print(result_df.to_string(index=False))
    else:
        print("Se produjo un error durante la solicitud o el procesamiento de datos.")
