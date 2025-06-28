from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# Usa tu API Key de OpenAI como variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    speech = request.form.get("SpeechResult", "")

    # Llamada a ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un agente de ventas amable y experto de Frutalia MID. Tu trabajo es ayudar a los negocios a conocer los sabores, beneficios y opciones de jugos naturales. Responde de forma clara, breve y orientada a cerrar ventas."},
            {"role": "user", "content": speech}
        ]
    )

    respuesta_ia = response.choices[0].message.content.strip()

    twiml = f"""<?xml version='1.0' encoding='UTF-8'?>
<Response>
    <Say voice='alice' language='es-MX'>{respuesta_ia}</Say>
    <Pause length='1'/>
    <Redirect>/voice</Redirect>
</Response>"""

    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

