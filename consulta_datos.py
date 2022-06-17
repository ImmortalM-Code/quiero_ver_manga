import subprocess
import requests
import urllib.request
import models
import conectar
import manejo_datos
import procesar_html
import models
import conectar

def agregar_mangas(parametros, chat_id):
    session = models.iniciar_db()
    verify_chat = [i.chat_id for i in session.query(models.Users).filter_by(chat_id=chat_id)]
    
    if len(verify_chat) == 0:
        chat = models.Users(chat_id)
        session.add(chat)
        session.commit()
        verify_chat = [i.chat_id for i in session.query(models.Users).filter_by(chat_id=chat_id)]
    
    if len(verify_chat) != 0:
        nombres = []
        for p in parametros:
            soup = conectar.ChargeWeb(p)
            html_procesado = procesar_html.procesar_manga(soup)
            g = manejo_datos.guardar_manga(html_procesado, chat_id, session=session)
            if g:
                nombres.append("ya existe, y si fuera el caso los generos se actualizaran.")
            else:
                n = f'{html_procesado["titulo"]} fue agregado'
                nombres.append(n)
        return nombres

    session.close()


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
                    
                    
    session.close()
    return registros


def mangas_auto():
    session = models.iniciar_db()
    mangas_db = [i for i in session.query(models.Mangas)]
    
    nuevos = procesar_html.ultimas_publicaciones(page=1)
    
    registro = []
    
    for i in nuevos:
        for j in mangas_db:
            if i['titulo'] == j.title:
                if i["hora"].strip().strip(" h") == "0":
                    i['chat_id'] = j.chat_id
                    registro.append(i)
                    
    
    session.close()
    return registro