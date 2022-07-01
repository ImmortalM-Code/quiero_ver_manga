import os
import urllib.request
import db_models.models as models
import scraping.conectar as conectar
import controllers.guardar_datos as guardar_datos
import scraping.procesar_html as procesar_html
import db_models.models as models
import scraping.conectar as conectar

def agregar_mangas(parametros, chat_id, logger):
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
            g = guardar_datos.guardar_manga(html_procesado, chat_id, session=session)
            if g:
                logger.info(f"manga existente {g}...")
                nombres.append("ya existe, y si fuera el caso los generos se actualizaran.")
            else:
                n = f'{html_procesado["titulo"]} fue agregado'
                logger.info(f"Agregado manga {g}...")
                nombres.append(n)
        return nombres

    session.close()


def obtener_nuevos(chat_id, logger):
    session = models.iniciar_db()
    chats = [i for i in session.query(models.Users)]
    mangas = [i for i in session.query(models.Mangas)]
    html_procesado = [procesar_html.ultimas_publicaciones(page=1), procesar_html.ultimas_publicaciones(page=2),
                      procesar_html.ultimas_publicaciones(page=3), procesar_html.ultimas_publicaciones(page=4)]
    logger.info(f"procesando mangas...")
    nuevos = [i for i in html_procesado]
    
    registros = []
    
    for c in chats:
        mangas = [i for i in session.query(models.Mangas).filter_by(chat_id=c.chat_id)]
        for m in mangas:
            for x in nuevos:
                for n in x:
                    if n["titulo"] == m.title and c.chat_id == chat_id:
                        logger.info(f"agragando {n['titulo']} a registro de envios...")
                        registros.append(n)
                    
                    
    session.close()
    return registros


def mangas_auto(logger):
    session = models.iniciar_db()
    mangas_db = [i for i in session.query(models.Mangas)]
    
    nuevos = [procesar_html.ultimas_publicaciones(page=1), procesar_html.ultimas_publicaciones(page=2),
              procesar_html.ultimas_publicaciones(page=3), procesar_html.ultimas_publicaciones(page=4)]
    
    logger.info(f"procesando mangas...")
    
    registro = []
    
    for x in nuevos:
        for i in x:
            for j in mangas_db:
                if i['titulo'] == j.title:
                    if i["hora"].strip().strip(" h") == "0":
                        logger.info(f"agregando {i['titulo']} a registro de envios...")
                        i['chat_id'] = j.chat_id
                        registro.append(i)
                    
    
    session.close()
    return registro


def descargar_img(inx, datos, logger):
    try:
        with open(f"img_tmp/{inx}.jpeg", "wb") as imagenfile:
            try:
                url = urllib.request.Request(datos["imagen"], headers=conectar.hdr)
                logger.info(f"Descargando: img_tmp/{inx}.jpeg...")
                imagenfile.write(urllib.request.urlopen(url).read())
                logger.info(f"imagen img_tmp/{inx}.jpeg Descargada")
            except ConnectionResetError as ex:
                print(f"Error {ex} - {repr(ex)}")
    
    except FileNotFoundError as ex:
            os.mkdir("img_tmp/")
            descargar_img(inx, datos, logger)

