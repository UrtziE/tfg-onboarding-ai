import os
import json
from github import Github
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
client = OpenAI(api_key=OPENAI_API_KEY)


def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def generar_resumen():
    historial = json.loads(leer_archivo("historial/evolucion_junior.json"))

    if not historial:
        print("El historial está vacío. No hay datos suficientes para generar el informe.")
        return

    prompt_sistema = leer_archivo("prompts/prompt_mentor.txt")

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": json.dumps(historial, ensure_ascii=False)}
        ],
        temperature=0.3
    )

    informe = respuesta.choices[0].message.content

    repo.create_issue(
        title="📊 Informe de Evolución de Onboarding (Desarrollador Junior)",
        body=informe
    )
    print("Informe generado y publicado como Issue en GitHub.")


if __name__ == "__main__":
    generar_resumen()