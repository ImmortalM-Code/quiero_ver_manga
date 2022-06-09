import models
import conectar
import manejo_datos
import procesar_html
import models

def capitulos_nuevos(parametros, chat_id):
    session = models.iniciar_db()
    verify_chat = None
    try:
        verify_chat = [i.chat_id for i in session.query(models.Users).filter_by(chat_id=chat_id)]
        print(len(verify_chat))
    except IndexError:
        chat = models.Users(chat_id)
        session.add(chat)
        session.commit()
        
        verify_chat = [i.chat_id for i in session.query(models.Users).filter_by(chat_id=chat_id)]
    
    if len(verify_chat) != 0:
        for p in parametros:
            soup = conectar.ChargeWeb(p)
            html_procesado = procesar_html.procesar_manga(soup)
            manejo_datos.guardar_manga(html_procesado, chat_id)
            return html_procesado["titulo"]


def obtener_nuevos():
    pass
