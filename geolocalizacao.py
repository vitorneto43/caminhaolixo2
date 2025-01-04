# geolocalizacao.py
import requests


def obter_localizacao_ip():
    # URL da API de geolocalização por IP
    response = requests.get("https://ipinfo.io/json")

    if response.status_code == 200:
        dados = response.json()
        cidade = dados.get("city")
        pais = dados.get("country")
        localizacao = dados.get("loc").split(",")  # latitude, longitude
        latitude, longitude = localizacao[0], localizacao[1]

        return {"cidade": cidade, "pais": pais, "latitude": latitude, "longitude": longitude}

    return None
