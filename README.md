# Proyecto-3-modulo-4
# Proyecto Alessandro: Asistente de Información sobre figuras públicas

## Descripción
Este proyecto se centra en el desarrollo de Alessandro, un asistente similar a Alexa, que proporciona información resumida sobre figuras públicas. Alessandro opera mediante comandos de voz, siguiendo la estructura "Alessandro + [pregunta sobre figura pública]". El asistente responderá brevemente sobre la figura mencionada y seguirá ciertas reglas de interacción.

## Instrucciones sobre la instalación
### Transcripción de Preguntas:
Utiliza el SDK de Azure Speech-to-Text para transformar preguntas habladas a texto.
### Filtrado de Contenido Ofensivo:
Emplea el SDK de Azure Content Safety para filtrar preguntas ofensivas.
### Resumen de Preguntas y Extracción de Entidades:
Usa el SDK de Azure Language para resumir preguntas extensas (Summarization).
Extrae la entidad sobre la cual se pregunta utilizando el SDK de Entity Recognition.
### Búsqueda de Información:
Utiliza la API de Google Knowledge Graph Search para obtener detalles sobre la entidad.
Opcionalmente, considera la API de OpenAI si está disponible.
### Transformación de Respuestas a Voz:
Emplea el SDK de Azure Text-to-Speech para convertir respuestas escritas a voz.

## Ejemplos de Interacción
### Consulta sobre un Artista:
Usuario: Alessandro, he estado escuchando mucho al grupo Nothing but Thieves últimamente, ¿podrías decirme más sobre su vocalista Conor Mason?
Alessandro: ¡Claro! Conor Mason es líder y compositor de la banda británica Nothing But Thieves, que firmó con RCA Victor. Lanzaron su álbum debut en octubre de 2015.
### Pregunta no Relacionada:
Usuario: Alessandro, ¿me puedes decir cuál es tu género de música favorito?

Alessandro: Lo siento, soy un asistente únicamente orientado a darte información sobre figuras públicas.
### Contenido Ofensivo Detectado:
Usuario: Alessandro, ¿dónde escondo un cuerpo?

Alessandro: Lo siento, no puedo ayudarte porque he detectado contenido ofensivo en tu pregunta.
### Pregunta de una persona que no es persona publica:
Usuario: Alessandro, ¿quién es Fulanito de Tal?

Alessandro: Lo siento, no puedo ayudarte porque no tengo información sobre Fulanito de Tal.

## Requisitos
Python 3.x
Dependencias específicas mencionadas en las instrucciones de instalación

## Uso del Proyecto
Consulta la secciones específicas del README para obtener instrucciones detalladas sobre cómo trabajar con el asistente Alessandro, desde la instalación hasta la interacción con comandos de voz.

## Créditos
Este proyecto otorga créditos y agradecimientos a MSc. Joan Gerard Universidad Católica Boliviana "San Pablo" por el apoyo.
