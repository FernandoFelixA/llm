# Proyecto 8: LLM

## Descripción

Probby es un tutor virtual inteligente cuya finalidad es ayudar a estudiantes de Ingeniería en Inteligencia Artificial en sus materias de Probabilidad y Estadística a entender los temas del curso y relacionarlos a su campo de estudio.

Los temas que Probby abarca son:

1. Probabilidad básica, regla de Bayes
2. Variables aleatorias y distribuciones comunes
3. Estadística descriptiva (media, varianza, desviación estándar, etc.)
4. Introducción a inferencia estadística

Probby está a disposición de los estudiantes para responder sus consultas, dar ejemplos y fomentar la práctica con ejercicios relacionados a la carrera que están estudiando. Este tutor virtual inteligente utiliza el modelo GPT-4o mini para responder preguntas con lenguaje natural y explicar paso a paso cada tema que se le consulte, dentro de los mencionados anteriormente.

---

## Tecnologías usadas

En el proyecto se utilizan las siguientes tecnologías:

1. OpenAI API
2. FastAPI
3. Python-dotenv
4. Uvicorn
5. Pydantic
6. HTML, CSS y JavaScript

El modelo GPT-4o mini es el cerebro de Probby, con el que da respuestas a los usuarios. La comunicación con el modelo se hace por medio de la API de OpenAI y la librería python-dotenv.

FastAPI y Uvicorn se utilizan para ejecutar Probby como aplicación en un servidor local, que presenta una interfaz más amigable a los estudiantes para hacer preguntas.

La librería Pydantic se utiliza para definir la estructura de los mensajes dentro del código.

La interfaz de usuario está construida con HTML, CSS y JavaScript vanilla, sin frameworks adicionales. La comunicación entre el frontend y el backend se realiza mediante fetch API.

---

## Instalación

Antes de la instalación es importante asegurarse de tener instalado Python 3.10 o superior.

Los pasos para ejecutar el programa son:

1. Abrir la terminal (Windows o Linux)

2. Clonar el repositorio ejecutando uno de los siguientes comandos:

HTTPS:

```bash
    git clone https://github.com/FernandoFelixA/llm.git
    cd llm
```

SSH:

```bash
    git clone git@github.com:FernandoFelixA/llm.git
    cd llm
```

3. Crear y activar entorno virtual:

En Windows:

```bash
    python -m venv .venv
    .venv\Scripts\activate
```

En Linux:

```bash
    python3 -m venv .venv
    source .venv/bin/activate
```

4. Instalar dependencias:

```bash
    pip install -r requirements.txt
```

5. Crear un archivo `.env` en la raíz del proyecto. Puedes hacerlo desde la terminal con:

En Windows:

```bash
    echo OPENAI_API_KEY=tu_api_key_aqui > .env
```

En Linux:

```bash
    echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
```

Reemplaza `tu_api_key_aqui` con tu API key real. Puedes obtenerla en [platform.openai.com](https://platform.openai.com). Si no tienes una cuenta, deberás crear una y agregar créditos en la sección Billing antes de poder usar la API.

> **Importante:** nunca compartas ni subas el archivo `.env` a un repositorio público. Este archivo ya está incluido en el `.gitignore` del proyecto.

6. Iniciar el servidor:

```bash
    uvicorn main:app --reload
```

7. Abrir el archivo `frontend/index.html` en el navegador.

---

## Uso

Una vez abierto el archivo `frontend/index.html` en el navegador se mostrará la interfaz del chat por medio del cual el estudiante se comunicará con Probby.

El chat siempre inicia con el primer mensaje del usuario. La interfaz contiene una caja de texto para escribir la consulta y un botón para Enviar. El usuario también puede enviar mensajes presionando la tecla Enter.

Si la consulta del usuario está dentro de los temas abarcados por Probby, éste responderá con una explicación. Si no está dentro de los temas, Probby se lo hará saber al usuario e intentará dirigir la conversación a uno de los temas que sí abarca.

Probby aplica el método socrático para enseñar, lo que asegura que el estudiante sea animado a pensar por medio de preguntas y podría ayudarlo a encontrar respuestas por sí mismo. En caso de que el usuario no tenga una idea del tema, puede pedir una explicación directa y Probby se la dará sin más preguntas.

Si el usuario quiere practicar un tema, puede pedir ejercicios directamente a Probby y éste evaluará sus respuestas. Siempre explicará detalladamente las respuestas a sus ejercicios.

A medida que avance la conversación y el usuario responda ejercicios, Probby registra el progreso por tema e intenta ajustar la dificultad y el tono de sus explicaciones según el nivel detectado.

---

## Decisiones de diseño

Se tomó la decisión de crear un tutor inteligente que implemente el método socrático como enfoque pedagógico porque así se fomenta un diálogo a través del cual se estimula el pensamiento crítico en el estudiante por medio de preguntas abiertas. La idea es que Probby no sea solo un chat que le da respuestas a los estudiantes, sino que los anime a pensar en cómo aplicar los conceptos de Probabilidad y Estadística para que establezcan relaciones entre lo teórico y lo práctico en su carrera de Inteligencia Artificial.

El enfoque del método socrático podría ser un poco pesado para algunos estudiantes que busquen una respuesta rápida o no puedan responder a las preguntas que Probby les haga. Probby decidirá no aplicar el método socrático cuando detecte que el usuario está muy confundido o el usuario le pida explícitamente una explicación directa.

Se implementó un perfil de sesión que calcula la puntuación del usuario en cada uno de los 4 temas (mencionados en el apartado Descripción). Cada tema tiene su propia puntuación y Probby ajusta la dificultad por tema. Esto se hizo así porque hay estudiantes que pueden tener un nivel avanzado en un tema y nivel básico o intermedio en otros, así el nivel que tenga el usuario en un tema no impacta en la dificultad de los demás.

La elección del modelo `gpt-4o-mini` se hizo considerando que para este tutor en particular, enfocado en temas de introducción a Probabilidad y Estadística, la potencia es más que suficiente, lo que asegura que no se haga un consumo excesivo de tokens por consulta de manera innecesaria.

---

## Limitaciones conocidas

Al momento de escribir este documento, Probby tiene las siguientes limitaciones:

1. **Evaluación de ejercicios inconsistente.** Esta es la limitación más importante. Debido a la prioridad conversacional de Probby sobre su rol de evaluador, no siempre califica como Correcto o Incorrecto un ejercicio resuelto por el usuario. Esto a veces impide que el perfil se actualice correctamente.

2. **Errores de cálculo matemático.** El modelo a veces comete errores aritméticos al corregir ejercicios numéricos. Probby aún no es una calculadora 100% confiable.

3. **El perfil de sesión no persiste entre sesiones.** Si el usuario cierra el navegador y vuelve, el perfil se reinicia desde cero. No hay almacenamiento en base de datos.

4. **Tolerancia al redondeo inconsistente.** Probby no siempre aplica el redondeo correctamente, por lo que podría tomar una respuesta en decimal como incorrecta, aunque por redondeo sí sea correcta.

5. **Una sola sesión por pestaña.** Si el usuario abre dos pestañas, son dos sesiones independientes sin relación entre sí.

Estas limitaciones tienen que ver más con el rol de Probby como evaluador de ejercicios y a pesar de ellas, actualmente Probby es un gran compañero para ayudar a los estudiantes a entender conceptos y ver ejemplos.

---

## Trabajo futuro

Se contemplan algunas mejoras futuras para Probby:

1. **Implementar un "juez separado"** para solucionar la evaluación de ejercicios inconsistente. La idea es hacer una llamada adicional a la API con una lógica nueva enfocada en evaluar.

2. **Crear una base de datos simple con SQLite** para que al crear una nueva sesión se guarde el perfil. Esto solucionaría la limitación de que el perfil no persiste entre sesiones, y permitiría al usuario continuar su sesión desde donde la dejó y actualizarla.

Con estos dos cambios se espera que Probby sea finalmente un evaluador confiable y por lo tanto un tutor más completo.

## Demo

[Ver demo en video](https://youtu.be/lH-T3daZCls)
