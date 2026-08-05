# Conectar el buscador con Spotify de verdad

El código ya está subido y funcionando. Falta **un paso tuyo de 1 minuto**.

## Por qué esto no compromete nada

La API de Spotify tiene dos formas de autenticarse:

| Flujo | Necesita `client_secret` | Sirve en el navegador |
|---|---|---|
| Client Credentials (el de tu `app.py`) | Sí | No |
| **Authorization Code + PKCE** | **No** | **Sí** |

PKCE existe precisamente para apps sin servidor. En vez del secreto, el
navegador genera un código aleatorio de un solo uso, manda solo su hash
(SHA-256), y al canjear el token demuestra que tiene el original. Nadie
puede reutilizar nada de lo que viaja por la URL.

Tu `client_id` sí es público por diseño: aparece en la URL de cualquier
login de Spotify, de cualquier app. No es una credencial secreta.

**Tu `client_secret` sigue solo en tu `.env` y en tu backend. No lo toqué.**

---

## El paso que falta

1. Entra a **https://developer.spotify.com/dashboard**
2. Abre tu app → **Settings**
3. En **Redirect URIs**, añade exactamente:

   ```
   https://bohorquezandrea.github.io/artist_finder_api/
   ```

   Con la barra final. Si no coincide carácter por carácter, Spotify
   rechaza la conexión.

4. **Save**

Listo. El botón "Conectar Spotify" ya funciona.

---

## Una limitación que debes conocer

Las apps de Spotify nacen en **modo desarrollo**. En ese modo, solo
pueden entrar los usuarios que tú añadas a mano:

**Dashboard → tu app → Settings → User Management** (máximo 25 personas,
por nombre y correo de su cuenta de Spotify).

Cualquier otra persona que pulse "Conectar Spotify" verá un error de
Spotify diciendo que no está autorizada.

Para abrirlo a todo el mundo hay que pedir **Extended Quota Mode**, que
es una solicitud que revisa Spotify a mano y suele tardar semanas.

### Por eso el catálogo local sigue ahí

La página funciona en dos niveles:

- **Sin conectar** (lo que verá casi todo el mundo): busca en el catálogo
  local de 58 artistas y arma la playlist con él. Instantáneo, sin login.
- **Conectado** (tú y quien añadas): busca en **todo Spotify**, con fotos
  de los artistas, y la playlist se arma con sus **top tracks reales** más
  artistas del mismo género según Spotify.

Si el token caduca o falla algo, vuelve solo al catálogo local y avisa.
Nunca se queda en blanco.

---

## Qué hace exactamente

| Acción | Endpoint de Spotify |
|---|---|
| Buscar artista | `GET /v1/search?type=artist` |
| Canciones del artista | `GET /v1/artists/{id}/top-tracks?market=CO` |
| Artistas afines | `GET /v1/search?q=genre:"..."&type=artist` |

Son los mismos datos que devuelve tu `app.py`, pero pedidos desde el
navegador con el token del visitante en vez del tuyo.
