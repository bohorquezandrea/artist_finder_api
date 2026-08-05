# Activar el envío de correo

El código ya está escrito y probado. Solo faltan 3 identificadores que
salen de tu cuenta de EmailJS. Son **públicos por diseño**, no son
contraseñas: van dentro del HTML y cualquiera puede verlos. La protección
real son los dominios permitidos, que configuras en el paso 5.

Mientras no los pongas, el botón sigue funcionando: abre tu cliente de
correo con la playlist escrita. No se rompe nada.

---

## 1. Crear la cuenta

Entra a **https://www.emailjs.com** y regístrate. El plan gratuito da
200 correos al mes, de sobra para un portfolio.

## 2. Conectar tu Gmail

1. Menú lateral → **Email Services** → **Add New Service**
2. Elige **Gmail** → **Connect Account** → autoriza con tu cuenta
3. Cuando quede conectado, copia el **Service ID** (algo como `service_ab12cde`)

## 3. Crear la plantilla

1. Menú lateral → **Email Templates** → **Create New Template**
2. En **Settings**, el campo **To Email** debe quedar exactamente así:

   ```
   {{to_email}}
   ```

   Esto es lo que hace que el correo llegue a la persona creada y no a ti.

3. En **Subject**:

   ```
   Tu playlist de Artist Finder
   ```

4. En el **cuerpo**, pega esto tal cual:

   ```
   Hola {{to_name}},

   Aquí está tu playlist, armada a partir de: {{artistas}}.

   {{playlist}}

   {{message}}
   ```

5. Guarda y copia el **Template ID** (algo como `template_xy34zab`)

## 4. Copiar la clave pública

Menú lateral → **Account** → **General** → copia la **Public Key**.

## 5. Restringir los dominios (importante)

Menú lateral → **Account** → **Security** → **Allow-list**

Añade:

```
bohorquezandrea.github.io
```

Sin esto, cualquiera podría copiar tus identificadores y mandar correos
desde tu cuenta hasta agotar tu cuota. Con la lista, solo funciona desde
tu sitio.

## 6. Pegarlos en el código

Abre `index.html` y busca cerca de la línea 300:

```js
var EMAILJS = {
  publicKey:  '',   // Account -> General -> Public Key
  serviceId:  '',   // Email Services -> Service ID
  templateId: ''    // Email Templates -> Template ID
};
```

Rellena las tres comillas, guarda y sube:

```bash
cd ~/Dev/repos-andrea/artist_finder_api
git add index.html
git commit -m "Activar envio de correo"
git push
```

En un par de minutos GitHub Pages lo publica y el botón envía de verdad.

---

## Qué hace el código

- Carga el SDK de EmailJS **solo al pulsar el botón**, no al abrir la
  página, para no penalizar la carga de quien nunca lo use.
- Muestra estado: `Enviando…` → `Listo, la playlist va en camino a…`
- Si el envío falla, avisa y ofrece un enlace de respaldo para abrirlo en
  el cliente de correo. Nunca se queda en silencio.
- Si la persona no tiene un correo válido, lo dice antes de intentarlo.

## Una advertencia

La página deja escribir cualquier correo. Con EmailJS activo, eso
significa que alguien podría usar tu formulario para mandar correos a
terceros desde tu cuenta. Para una demo de portfolio con 200 correos al
mes y la lista de dominios activada, el riesgo es bajo. Pero si algún día
esto crece, el envío debería pasar por un servidor tuyo con validación.
