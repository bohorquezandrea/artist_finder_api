from flask import Flask, request, jsonify
import json 
import os
from dotenv import load_dotenv
import requests
load_dotenv(dotenv_path='.env')



app = Flask(__name__)

load_dotenv()

# Para las credenciales de Spotify
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

print("SPOTIFY_CLIENT_SECRET:", SPOTIFY_CLIENT_SECRET)
print("SPOTIFY_CLIENT_ID:", SPOTIFY_CLIENT_ID)

USERS_FILE = 'users.json'

# Funciones para guardar los usuarios
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


# Endpoints para los usuarios

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    users = load_users()

    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email'],
        "artists": []
    }
    users.append(new_user)
    save_users(users)
    return jsonify({"message": "Usuario creado con éxito", "user": new_user}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = load_users()
    return jsonify(users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Usuario no encontrado"}), 404


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    users = load_users()

    user = next((u for u in users if u['id'] ==user_id), None)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']

    save_users(users)
    return jsonify({"message": "Usuario actualizado con éxito", "user": user}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = load_users()
    users = [u for u in users if u ['id'] != user_id]
    save_users(users)
    return jsonify({"message": "Usuario eliminado con éxito"}), 200

# Endpoints para los artistas favoritos

@app.route('/users/<int:user_id>/artists', methods=['POST'])
def add_artist(user_id):
    data = request.get_json()
    users = load_users()

    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    if 'artist_name' not in data:
        return jsonify({"error": "Falta el nombre del artista"}), 400
    
    user['artists'].append(data['artist_name'])
    save_users(users)
    return jsonify({"message": "Artista agregado con éxito", "artists": user['artists']}), 201

@app.route('/users/<int:user_id>/artists', methods=['GET'])
def get_artists(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user['artists']), 200
    return jsonify({"error": "Usuario no encontrado"}), 404


# Integrar la API de Spotify
def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error al obtener el token de Spotify:", response.json())
        return None
    

# Para consultar la informacion de un artista
@app.route('/spotify/artist/<string:artist_name>', methods=['GET'])
def get_artist(artist_name):
    token = get_spotify_token()
    if not token:
        return jsonify({"error": "No se pudo obtener el token de Spotify"}), 500
    
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("artists", {}).get("items", [])
        if len(data) > 0:
            artist = data[0]
            return jsonify({
                "name": artist["name"],
                "genres": artist["genres"],
                "followers": artist["followers"]["total"],
                "popularity": artist["popularity"],
                "url": artist["external_urls"]["spotify"],
                "image": artist["images"][0]["url"] if artist["images"] else None
            }), 200
        else:
            return jsonify({"error": "Artista no encontrado"}), 404
    else:
        return jsonify({"error": "Error al consultar la API de Spotify"}), response.status_code

@app.route('/spotify/song/<string:song_name>', methods=['GET'])
def get_song(song_name):
    """Obtener información de una canción en Spotify."""
    token = get_spotify_token()
    if not token:
        return jsonify({"error": "No se pudo obtener el token de Spotify"}), 500

    url = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("tracks", {}).get("items", [])
        if len(data) > 0:
            track = data[0]
            return jsonify({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"],
                "url": track["external_urls"]["spotify"],
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None
            }), 200
        else:
            return jsonify({"error": "Canción no encontrada"}), 404
    else:
        return jsonify({"error": "Error al consultar la API de Spotify"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

