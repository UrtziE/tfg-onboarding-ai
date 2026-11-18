import os
import json
from datetime import datetime
from github import Github
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
EVENT_NAME = os.getenv("GITHUB_EVENT_NAME")

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
client = OpenAI(api_key=OPENAI_API_KEY)


def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def obtener_codigo_y_destino():
    """Extrae los cambios (diff) y devuelve el objeto de GitHub donde comentar."""
    diff_texto = ""

    if EVENT_NAME == "pull_request":
        with open(os.getenv("GITHUB_EVENT_PATH"), "r", encoding="utf-8") as f:
            event_data = json.load(f)
        pr_number = event_data["pull_request"]["number"]
        pr = repo.get_pull(pr_number)

        for file in pr.get_files():
            if file.patch:
                diff_texto += f"\n--- Archivo: {file.filename} ---\n{file.patch}\n"
        return diff_texto, pr, f"PR #{pr_number}"

    elif EVENT_NAME == "push":
        sha = os.getenv("GITHUB_SHA")
        commit = repo.get_commit(sha)

        if "[skip-ai]" in commit.commit.message:
            return None, None, None

        for file in commit.files:
            if file.patch:
                diff_texto += f"\n--- Archivo: {file.filename} ---\n{file.patch}\n"
        return diff_texto, commit, f"Commit {sha[:7]}"

    return None, None, None


def analizar_con_ia(diff, reglas):
    plantilla_prompt = leer_archivo("prompts/prompt_revisor.txt")
    prompt_sistema = plantilla_prompt.format(reglas=reglas)

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Analiza este diff:\n{diff}"}
        ],
        temperature=0.2
    )
    return json.loads(respuesta.choices[0].message.content)


def guardar_historial(identificador, errores):
    ruta = "historial/evolucion_junior.json"
    historial = json.loads(leer_archivo(ruta))

    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "origen": identificador,
        "errores_detectados": errores
    })

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)


def main():
    diff, destino, identificador = obtener_codigo_y_destino()
    if not diff:
        print("No hay cambios de código relevantes para analizar.")
        return

    reglas = leer_archivo("reglas/estandares_empresa.md")
    resultado = analizar_con_ia(diff, reglas)

    mensaje = f"### 🤖 Feedback de Onboarding ({identificador})\n\n{resultado['comentario_markdown']}"

    if EVENT_NAME == "pull_request":
        destino.create_issue_comment(mensaje)
    elif EVENT_NAME == "push":
        destino.create_comment(mensaje)

    guardar_historial(identificador, resultado["errores"])
    print(f"Revisión completada y publicada en {identificador}.")


if __name__ == "__main__":
    main()