from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# Usa tu clave desde las variables de entorno en Render
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    speech = request.form.get("SpeechResult", "")
    if not speech:
        speech = "Inicia la conversación como asistente de Frutalia MID."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un agente de ventas de Frutalia MID. Saluda, presenta los jugos naturales y ofrece tomar pedidos."},
            {"role": "user", "content": speech}
        ]
    )

    respuesta_ia = response.choices[0].message.content.strip()

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="es-MX">{respuesta_ia}</Say>
    <Pause length="2"/>
    <Redirect>/voice</Redirect>
</Response>"""

    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
