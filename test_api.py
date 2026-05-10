from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Eres Prooby, un tutor amigable de Probabilidad y Estadística."
        },
        {
            "role": "user",
            "content": "Hola, 'qué temas puedes enseñarme?"
        }
    ]
)

print(response.choices[0].message.content)