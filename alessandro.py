#para utilizar el servicio de Speech Service
#!pip install azure-cognitiveservices-speech

#para utilizar el servicio de language de azure
#!pip install azure-ai-textanalytics==5.3.0

#para utilizar el servicio de Content safety
#!pip install azure-ai-contentsafety

from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import time
import json
import re

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractiveSummaryAction
) 
import pandas as pd
import requests


print("Cargar variables de entorno desde archivo .env")
load_dotenv("env.txt", override=True)

#para ejecutar el microno y reconocer nuestra voz y guardarlo en un archivo
#Con los servicios de "Speech Service" de azure
def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-BO")

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return result

#funcion para ver si existe una palabra determinado en el texto
def si_existe_alessandro(s, x):
    r = '.*'.join(x) # Inserta '.*' entre todas las letras de la palabra buscada
    return re.search(r, s) is not None

# Example function for recognizing entities from text
#Con los servicios de "Language" de azure

def entity_recognition_example(client, documents):
    try:
        result = client.recognize_entities(documents = documents)[0]

        #print("Named Entities:\n")
        return result.entities
    
    except Exception as err:
        print("Encountered exception. {}".format(err))



# Autenticarse
def authenticate_client():
    key = os.environ.get('LANGUAGE_KEY')
    endpoint = os.environ.get('LANGUAGE_ENDPOINT')
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def sacar_df_microfono(texto_microfono: str):
    client = authenticate_client()
    document = [texto_microfono]
    entities = entity_recognition_example(client,document)
    data_list = []
    for entity in entities:
        data_list.append([entity.text, entity.category, entity.confidence_score])
    columns = ['Name','Category','Confidence Score']
    df = pd.DataFrame(data_list, columns=columns)
    return df

#funcion para ver cuantos personajes existe en la oracion dictada por el microfono
def verificar_nombra_artista(texto_microfono: str):
    df = sacar_df_microfono(texto_microfono)
    personas = df[df['Category'] == 'Person']
    cantidad = len(personas.axes[0])
    return cantidad

#funcion para extraer el nombre del artista de la oracion dictada por el microfono
def sacar_artista(texto_microfono: str):
    df = sacar_df_microfono(texto_microfono)
    artista = df[df['Category'] == 'Person'].iloc[1].Name
    return artista



#para ver si la oracion es mala antes de procesarla
#con el servicio de Content Safety
def analyze_text(text_input: str):
    
    # analyze text
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=text_input)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    return response


if __name__ == "__main__":
    text = 'Nací viejo, \
    Mi vida ha sido un tránsito brusco de la niñez a la vejez, \
    sin términos medios. No tuve tiempo de ser niño. Nacionalizo una pistola \
    y me pego un tiro.'
#Para analizar el texto



# Ejemplo para resumir texto en este caso no se utiliza por que el servicio de google ya entrega resumido
def sample_extractive_summarization(client, documents):
    document = documents

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=1)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("Error: '{}' - Mensaje: '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            print("Resumen: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )



#buscar el artista en google

def buscardor_artista(artista: str):
    load_dotenv("env.txt", override=True)
    api_key = os.environ.get('API_GOOGLE_KEY')
    # URL base de la API de Knowledge Graph
    url = "https://kgsearch.googleapis.com/v1/entities:search"
    # Parámetros de la consulta
    query = artista
    
    params = {
        "query": query,
        "key": api_key,
        "limit": 1,  # Puedes ajustar el límite según tus necesidades
        "languages": "es"
    }
    # Realizar la solicitud a la API
    response = requests.get(url, params=params)
    data = response.json()
    # Procesar la respuesta
    if "itemListElement" in data and len(data["itemListElement"]) > 0:
        result = data["itemListElement"][0]["result"]
        description = result["detailedDescription"]["articleBody"]
        salida = description.replace("\u200B", "")
        salida = aumentar_palabra_string("¡Claro!, ",salida)
        return salida
    else:
        salida = "Lo siento, no puedo ayudarte porque no tengo informacion sobre "
        salida = aumentar_palabra_string(salida,artista)
        return salida

def aumentar_palabra_string(palabra: str, agregar: str):
    t = list()
    t.append((palabra + agregar))
    nueva_oracion = t[0]
    return nueva_oracion


#Pasar a audio un texto con los servicios de Speech Service

def leer_texto(salida: str):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    # El lenguaje de la voz que habla
    # ver otras voces aqui: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt#prebuilt-neural-voices
    speech_config.speech_synthesis_voice_name='es-BO-MarceloNeural'
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    text = salida
    
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech to text: [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")











