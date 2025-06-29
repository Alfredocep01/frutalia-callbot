import openai
from openai import OpenAI
from flask import Flask, request, Response
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/voice", methods=["POST"])
def voice():
    prompt_usuario = "Actúa como un asistente telefónico amable de Frutalia MID. Saluda y ofrece información de jugos naturales."

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente telefónico de Frutalia MID."},
            {"role": "user", "content": prompt_usuario}
        ]
    )

    mensaje = respuesta.choices[0].message.content.strip()

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="es-MX">{mensaje}</Say>
</Response>"""

    return Response(twiml, mimetype="text/xml")
