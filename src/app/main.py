from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
import pickle
import os

# ------------- Carregamento do modelo treinado (serializado) -----------------
modelo = pickle.load(open("../../models/modelo.sav", "rb"))
colunas = ["tamanho", "ano", "garagem"]


# ---------------------------- Aplicação --------------------------------------
app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ.get("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get("BASIC_AUTH_PASSWORD")

basic_auth = BasicAuth(app)

# Index
@app.route("/")
def home():
    return "Minha primeira API."

# Sentimento (polaridade de frase)
@app.route("/sentimento/<frase>")
@basic_auth.required
def sentimento(frase):
    translator = Translator()
    frase_en = translator.translate(frase, dest='en')
    
    tb = TextBlob(frase_en.text)
    polaridade = tb.sentiment.polarity

    return "Polaridade: {}".format(polaridade)

# Cotação de imóvel por tamanho
@app.route("/cotacao/", methods=["POST"])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]

    preco = modelo.predict([dados_input])

    return jsonify(preco=preco[0])


app.run(debug=True, host="0.0.0.0")