# Artist Finder API - Integración con API de Spotify

## Descripción
Esta API permite gestionar información de usuarios, almacenar sus artistas favoritos y consultar información de artistas y canciones a través de la API de Spotify.

## Características
- CRUD completo de usuarios (crear, leer, actualizar, eliminar)
- Guardado de artistas favoritos para cada usuario
- Consulta de información de artistas y canciones en Spotify
- Uso de variables de entorno para mayor seguridad

---

## Requisitos
- Python 3.10 o superior
- Flask
- Requests
- Python-Dotenv
- Cuenta en Spotify 

---

## Configuración
1. Clona el repositorio:
2. Crea un entorno virtual :
3. Instala las dependencias:
4. Configura las variables de entorno en el archivo .env
5. Crea un archivo users.json vacío
6. Inicia el servidor 

<!-- ENDPOINTS DE LA API -->

## Usuarios 
POST
/users -> crear un nuevo usuario 

GET 
/users -> enlistar todos los usuarios

GET 
/users/<id> -> obtener un usuario por id

PUT 
/users/<id> -> actualizar un usuario

DELETE 
/users/<id> -> eliminar un usuario

## Artistas favoritos
POST
/users/<id>/artists -> agregar un artista favorito

GET 
/users/<id>/artists -> enlistar los artistas favoritos de un usuario

## Integración con Spotify
GET 
/spotify/artist/<artist_name> -> Obtener informacion de un artista

GET
/spotify/song/<song_name> -> obtener información de una canción

