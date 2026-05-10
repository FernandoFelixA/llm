max_mensajes = 20

def recortar_historial(historial):
    system = historial[0]
    conversacion = historial[1:]
    if len(conversacion) > max_mensajes:
        conversacion = conversacion[-max_mensajes:]
    return [system] + conversacion

