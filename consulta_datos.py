import models
import conectar
import manejo_datos
import procesar_html
import models

def capitulos_nuevos(parametros, chat_id):
    session = models.iniciar_db()
    verify_chat = [i.chat_id for i in session.query(models.Users).filter_by(chat_id=chat_id)]
    print(len(verify_chat))
    if len(verify_chat) == 0:
        chat = models.Users(chat_id)
        session.add(chat)
        session.commit()
        verify_chat = [i.chat_id for i in session.query(models.Users).filter_by(chat_id=chat_id)]
    
    if len(verify_chat) != 0:
        for p in parametros:
            soup = conectar.ChargeWeb(p)
            html_procesado = procesar_html.procesar_manga(soup)
            manejo_datos.guardar_manga(html_procesado, chat_id, session=session)
            return html_procesado["titulo"]
    
    session.close_all()


def obtener_nuevos(chat_id):
    session = models.iniciar_db()
    chats = [i for i in session.query(models.Users)]
    mangas = [i for i in session.query(models.Mangas)]
    html_procesado = procesar_html.ultimas_publicaciones(page=1)
    
    nuevos = [i for i in html_procesado]
    
    registros = []
    
    for c in chats:
        mangas = [i for i in session.query(models.Mangas).filter_by(chat_id=c.chat_id)]
        for m in mangas:
            for n in nuevos:
                if n["titulo"] == m.title and c.chat_id == chat_id:
                    registros.append(n)
                    
                    
    session.close_all()
    return registros


def mangas_auto():
    pass
