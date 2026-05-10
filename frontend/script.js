let sessionId = null;

// 1. Al cargar la página

async function iniciarSesion() {
  // Llama a /nueva-sesion y guarda el session_id en la variable sessionId
  const respuesta = await fetch("http://127.0.0.1:8000/nueva-sesion", {
    method: "POST",
  });
  const datos = await respuesta.json();
  sessionId = datos.session_id;
}

// 2. Al enviar un mensaje

async function enviarMensaje() {
  // Lee el texto del input
  let inputMensaje = document.getElementById("input-mensaje");
  let mensaje = inputMensaje.value;
  agregarMensaje(mensaje, "usuario");

  // Limpia el input
  document.getElementById("input-mensaje").value = "";

  // Indicador
  const indicador = document.createElement("div");
  indicador.id = "indicador";
  indicador.className = "probby";
  indicador.innerHTML = `
    <div class="puntos-animados">
    <span></span>
    <span></span>
    <span></span>
    </div> `;
  document.getElementById("chat").appendChild(indicador);

  // Llama a /chat con session Id y el mensaje
  const consulta = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      mensaje: mensaje,
    }),
  });
  const datos = await consulta.json();
  let respuesta;

  document.getElementById("indicador").remove();
  if (datos.error) {
    respuesta = datos.error;
  } else {
    respuesta = datos.respuesta;
  }
  agregarMensaje(respuesta, "probby");
}

// 3. Mostrar un mensaje en el chat
function agregarMensaje(texto, autor) {
  const div = document.createElement("div");
  div.className = autor;
  if (autor === "probby") {
    div.innerHTML = marked.parse(texto);
    document.getElementById("chat").appendChild(div);
    MathJax.typesetPromise([div]);
  } else {
    div.textContent = texto;
    document.getElementById("chat").appendChild(div);
  }
}

//Eventos
document
  .getElementById("boton-enviar")
  .addEventListener("click", enviarMensaje);

iniciarSesion();
