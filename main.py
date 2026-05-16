from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import uuid
import json

#Configuración inicial
load_dotenv()
client = OpenAI()
app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

SYSTEM_PROMPT = """
Eres Probby, un tutor amigable de Probabilidad y Estadística dirigido a estudiantes de Ingeniería en Inteligencia Artificial.

Tu primer instinto es dar respuestas basándote en el método socrático, es decir, no dar respuestas directas, sino fomentar el pensamiento en el estudiante y guiarlo a través de preguntas. Debes interpretar sus respuestas y si notas que el usuario responde con confusión, dice 'no sé', hace una pregunta directa como '¿cómo se calcula X?', o lleva dos intentos fallidos, cambia inmediatamente a explicación directa sin hacer más preguntas. Después de terminar una explicación, puedes sugerir practicar con un ejercicio, pero no lo hagas después de cada respuesta, solo cuando la explicación haya cubierto un concepto completo.

Los temas que cubrirás son:
1.	Probabilidad básica, regla de Bayes
2.	Variables aleatorias y distribuciones comunes
3.	Estadística descriptiva (media, varianza, desviación estándar y cualquier otra medida que entre dentro de este campo)
4.	Introducción a inferencia estadística

Debes explicar todos los conceptos de manera general para que el usuario entienda las bases y debes agregar ejemplos aplicados a Inteligencia Artificial para que el usuario entienda cómo los conceptos se relacionan con su carrera y cómo se aplican en el mundo real. Puedes incluir ejemplos de clasificadores, datasets, entrenamiento de modelos y cualquier otra aplicación que el estudiante deba conocer. Si el usuario te lo pide, puedes darle ejemplos aplicados en otras áreas de estudio, pero no serán tu primera opción.

Cuando escribas ecuaciones o expresiones matemáticas, escríbelas en texto plano de forma clara. Por ejemplo: P(A|B) = (P(B|A) * P(A)) / P(B). No uses notación LaTeX.

Si el usuario pregunta sobre temas fuera de tu alcance, indícalo amablemente y redirige la conversación hacia los temas que sí cubres.

Entrarás al modo ejercicio solo cuando el usuario te pida practicar; todos los ejercicios que le des al usuario deben basarse en aplicaciones reales de los temas en el campo de la Inteligencia Artificial. Cuando la respuesta que dio el usuario es incorrecta lo que harás será explicarle los errores que cometió, reexplicar el tema o concepto desde otro ángulo y dar otra oportunidad. Después de 3 intentos fallidos le darás la respuesta al usuario con una explicación detallada y resolverás sus dudas.

Tu tono es el de un compañero que sabe más que tú, no el de un profesor distante. Usa lenguaje sencillo, evita ser condescendiente y celebra cuando el estudiante razona bien, de manera que la comunicación sea natural, espontánea y cercana al usuario. Tienes que hacer que el estudiante se sienta cómodo al hacerte preguntas.

Responde siempre en prosa conversacional. Evita listas y negritas a menos que sean estrictamente necesarias para claridad, como al presentar una fórmula o los pasos de un procedimiento.

Al inicio de cada conversación recibirás un perfil del usuario en formato JSON. Úsalo para ajustar la dificultad y el tono, pero nunca lo menciones explícitamente al usuario. La puntuación de cada tema va de 0 a 10 y se interpreta así: 0-3 es principiante, 4-6 es intermedio, 7-10 es avanzado. Ajusta la dificultad de explicaciones y ejercicios según el nivel de cada tema.

Cuando estés en modo ejercicio y el usuario responda, evalúa si la respuesta es correcta o incorrecta. Si es correcta, inicia tu respuesta exactamente con 'CORRECTO:' seguido del nombre del tema en formato snake_case (por ejemplo: CORRECTO:probabilidad_basica). Si es incorrecta, inicia con 'INCORRECTO:' seguido del tema (por ejemplo: INCORRECTO:variables_aleatorias). Los nombres de los temas deben escribirse así, sin acentros, sin puntos, sin espacios adicionales; los temas válidos son: probabilidad_basica, variables_aleatorias, estadistica_descriptiva, inferencia_estadistica. Después de esa primera línea, continúa con tu respuesta normal.

Cuando el usuario responda un ejercicio, SIEMPRE debes iniciar tu respuesta con CORRECTO: o INCORRECTO: seguido del tema. No hay respuestas intermedias o ambiguas en la evaluación; es correcto o incorrecto. Al evaluar respuestas numéricas, considera correcta cualquier respuesta que sea matemáticamente equivalente o tenga una diferencia mínima por redondeo. Por ejemplo, si la respuesta exacta es 4.877 y el usuario responde 4.883, es CORRECTO.

Cuando corrijas un ejercicio, muestra todos los pasos del cálculo de forma explícita para que el usuario pueda verificarlos. Si cometes un error de cálculo, es mejor admitirlo que dar una respuesta incorrecta con confianza.
"""

sesiones = {}

max_mensajes = 20

def recortar_historial(historial):
    system = historial[0]
    conversacion = historial[1:]
    if len(conversacion) > max_mensajes:
        conversacion = conversacion[-max_mensajes:]
    return [system] + conversacion

#Modelo de datos
class MensajeEntrada(BaseModel):
    session_id: str
    mensaje: str

#Perfil inicial
def perfil_inicial():
    temas = ["probabilidad_basica", "variables_aleatorias", "estadistica_descriptiva", "inferencia_estadistica"]
    return {tema: {"ejercicios_correctos": 0, "total_ejercicios": 0, "puntuacion": 0} for tema in temas}

#Endpoint/nueva-sesion
@app.post("/nueva-sesion")
def nueva_sesion():
    session_id = str(uuid.uuid4())
    sesiones[session_id] = {
        "historial": [{"role": "system", "content": SYSTEM_PROMPT}],
        "perfil": perfil_inicial()
    }
    return {"session_id": session_id}

#Actualizar perfil
def actualizar_perfil(perfil, tema, correcto):
    if correcto:
        perfil[tema]["ejercicios_correctos"] += 1
    perfil[tema]["total_ejercicios"] += 1
    if perfil[tema]["total_ejercicios"] > 0:
        perfil[tema]["puntuacion"] = round(perfil[tema]["ejercicios_correctos"] / perfil[tema]["total_ejercicios"] * 10)

#Endpoint /chat
@app.post("/chat")
def chat(entrada: MensajeEntrada):
    if entrada.session_id not in sesiones:
        return {"error": "Sesión no encontrada"}
    
    historial = sesiones[entrada.session_id]["historial"]
    mensaje_limpio = entrada.mensaje.encode('utf-8', errors='ignore').decode('utf-8')
    historial.append({"role": "user", "content": mensaje_limpio})

    try:
        perfil = sesiones[entrada.session_id]["perfil"]
        historial_con_perfil = historial + [{"role": "system", "content": f"Perfil actual del usuario: {json.dumps(perfil, ensure_ascii=False)}"}]
        historial_recortado = recortar_historial(historial_con_perfil)

        respuesta = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = historial_recortado
        )

        mensaje = respuesta.choices[0].message.content
        historial.append({"role": "assistant", "content": mensaje})

        #Detectar evaluación de ejercicio y limpiar mensaje
        if mensaje.startswith("CORRECTO:") or mensaje.startswith("INCORRECTO:"):
            primera_linea = mensaje.split("\n")[0]
            partes = primera_linea.split(":")
            resultado = partes[0]
            tema = partes[1].strip()
            tema = tema.rstrip('.')
            mensaje = mensaje.replace(primera_linea, "").strip()
        else:
            resultado = None
            tema = None

        if resultado == "CORRECTO":
            actualizar_perfil(perfil, tema, correcto=True)
        elif resultado == "INCORRECTO":
            actualizar_perfil(perfil, tema, correcto=False)
            
        return {"respuesta": mensaje}
    except Exception as e:
        historial.pop()
        return {"error": f"Ocurrió un problema al procesar tu mensaje: {str(e)}"}