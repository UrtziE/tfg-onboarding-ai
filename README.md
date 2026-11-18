# 🤖 AI Onboarding Reviewer (GrAL / TFG)

Sistema automatizado basado en Inteligencia Artificial Generativa (LLM) para asistir a desarrolladores *junior* durante su proceso de *onboarding*. Analiza automáticamente los *commits* y *Pull Requests* en GitHub comparándolos con los estándares internos de la empresa, proporciona *feedback* didáctico en tiempo real y genera informes periódicos de evolución para el mentor técnico.

---

## 📁 Estructura del Proyecto

```text
├── .github/workflows/       # Flujos de automatización (GitHub Actions)
├── prompts/                 # Plantillas de prompts desacopladas del código
├── reglas/                  # Estándares y buenas prácticas de la empresa
├── historial/               # Registro cronológico de errores detectados (JSON)
├── src/                     # Código fuente en Python (reviewer.py y mentor_report.py)
├── .env.example             # Plantilla de variables de entorno para ejecución local
├── .gitignore               # Archivos excluidos del control de versiones
└── requirements.txt         # Dependencias de Python
```

---

## ⚙️ Configuración de Variables de Entorno (`.env`)

Para ejecutar o probar los scripts en local, crea un archivo llamado `.env` en la raíz del proyecto tomando como base `.env.example`.

### 1. `GITHUB_TOKEN` (Token de acceso personal de GitHub)
Necesario para que Python pueda leer los *commits* / *Pull Requests* y publicar comentarios o *Issues* en el repositorio.
1. Inicia sesión en **GitHub** y haz clic en tu foto de perfil (arriba a la derecha) → **Settings**.
2. En el menú lateral izquierdo, baja hasta el final y entra en **Developer settings**.
3. Selecciona **Personal access tokens** → **Tokens (classic)**.
4. Haz clic en **Generate new token** → **Generate new token (classic)**.
5. Ponle un nombre descriptivo (ej. `TFG Onboarding Local`), selecciona la expiración y marca la casilla principal **`repo`** (control total de repositorios).
6. Pulsa **Generate token**, copia el código generado (empieza por `ghp_...`) y pégalo en tu `.env`.

### 2. `OPENAI_API_KEY` (Clave de API del modelo LLM)
Necesaria para enviar el código modificado (*diff*) y las reglas al modelo de lenguaje.
1. Entra en [platform.openai.com](https://platform.openai.com/) e inicia sesión.
2. En el menú lateral izquierdo, ve a **API keys** (o en el icono de ajustes → *API keys*).
3. Haz clic en **Create new secret key**, asígnale un nombre (ej. `TFG-Reviewer`) y pulsa **Create secret key**.
4. Copia la clave generada (empieza por `sk-...`) y pégala en tu `.env`. *(Nota: asegúrate de tener saldo disponible en Billing).*

### 3. `GITHUB_REPOSITORY` (Identificador del repositorio)
Es el nombre de tu usuario u organización seguido de una barra y el nombre del repositorio.
* **Cómo obtenerlo:** Mira la URL de tu repositorio en el navegador (`https://github.com/usuario/mi-repo`). El valor que debes poner es únicamente `usuario/mi-repo`.

### 4. `GITHUB_EVENT_NAME` y `GITHUB_SHA` *(Solo para pruebas en local)*
Cuando el sistema corre en GitHub Actions, GitHub rellena estos datos automáticamente. Si quieres probar `src/reviewer.py` desde tu ordenador:
* **`GITHUB_EVENT_NAME`**: Escribe `push` para simular la revisión de un *commit*.
* **`GITHUB_SHA`**: Es el identificador único de 40 caracteres del *commit* que quieres analizar.
  * **Cómo obtenerlo:** Entra a tu repositorio en GitHub, haz clic en **Commits**, busca el *commit* de prueba que quieras analizar y pulsa el icono de **copiar SHA completo** (a la derecha del título del *commit*). Pégalo en el `.env`.

---

## 🚀 Ejecución en Local (Pruebas)

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Rellena tu archivo `.env` siguiendo los pasos anteriores.

3. Ejecuta el revisor de código sobre el *commit* indicado en `GITHUB_SHA`:
   ```bash
   python src/reviewer.py
   ```

4. Para probar la generación del informe ejecutivo para el mentor (requiere que `historial/evolucion_junior.json` tenga al menos un registro):
   ```bash
   python src/mentor_report.py
   ```

---

## 🔄 Despliegue Automático en GitHub Actions

Para que el sistema funcione de forma autónoma en la nube ante cada nuevo *commit* o *Pull Request*:
1. Ve a tu repositorio en GitHub → **Settings** → **Secrets and variables** → **Actions**.
2. Pulsa **New repository secret**, crea el secreto **`OPENAI_API_KEY`** y pega tu clave de OpenAI (`GITHUB_TOKEN` y `GITHUB_REPOSITORY` los provee GitHub automáticamente).
3. En **Settings** → **Actions** → **General**, baja hasta **Workflow permissions**, selecciona **Read and write permissions** y guarda los cambios.