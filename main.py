from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext
import sys
import time
import telegram
import controllers.consulta_datos as consulta_datos
import mensajes as mj
import logging
import os
import telegram
import threading


# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()
# Variables de entorno
TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODO")
# Telegram 
bot = telegram.Bot(token=TOKEN)
updater = Updater(bot.token)
dp = updater.dispatcher
# Jobs
#jobs = updater.job_queue
# Commands
comandos = mj.COMANDOS


if mode == "dev":
    def run(updater):
        updater.start_polling()#timeout=120)
        logger.info("Bot iniciado")
        updater.idle()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,
                              webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
        logger.info("Bot iniciado")
else:
    logger.info("MODO no expecificado")
    sys.exit()  


def extract_arg(arg):
    return arg.split()[1:]


def bienvenida(update, context):
    logger.info(f"Usuario - {update.message.chat['first_name']} - con id - {update.message.chat['id']} - se a conectado.")
    nombre = f"{update.message.chat['first_name']} {update.message.chat['last_name']}"
    mensaje = mj.BIENVENIDA % (nombre)
    update.message.reply_text(mensaje)
        

def ayuda(update, context):
    logger.info(f"Usuario - {update.message.chat['first_name']} - con id - {update.message.chat['id']} - Solicito /help.")
    id = update.message.chat["id"]
    ayudas = ""
    for k in comandos:
        ayudas += f"/{k} : {comandos[k]}\n"
    context.bot.sendMessage(chat_id=id, parse_mode="HTML", text=ayudas)
    

def agregar_mangas(update, context):
    logger.info(f"Usuario - {update.message.chat['first_name']} - con id - {update.message.chat['id']} - Solicito /addm .")
    id = update.message.chat["id"]
    parametros = extract_arg(update.message.text)
    p = consulta_datos.agregar_mangas(parametros=parametros, chat_id=id, logger=logger)
    
    for n in p:
        context.bot.sendMessage(chat_id=id, text=f"{n}")
        
    logger.info(f"Solicitud /addm Finalizada.")
    

def nuevos_mangas(update, context):
    logger.info(f"Usuario - {update.message.chat['first_name']} - con id - {update.message.chat['id']} - Solicito /newm .")
    id = update.message.chat["id"]
    registro = consulta_datos.obtener_nuevos(chat_id=id, logger=logger)
    registro.reverse()
    
    once_down = []
    
    if len(registro) != 0:
        for inx, i in enumerate(registro):
            if i["titulo"] not in once_down:
                consulta_datos.descargar_img(inx, i, logger)
                
                with open(f"img_tmp/{inx}.jpeg", "rb") as imagenfile:
                    context.bot.sendPhoto(chat_id=id, photo=imagenfile)
                once_down.append(i["titulo"])
                    
            mensaje = mj.NUEVAS_PUBLICACIONES % (i["titulo"], i["capitulo"], i["tipo"], i["scan"], i["url"])
            
            context.bot.sendMessage(chat_id=id, parse_mode="HTML", text=mensaje)
            time.sleep(0.1)
    logger.info(f"Solicitud /newm Finalizada.")


#def notificacion_auto(context: CallbackContext):
def notificacion_auto():
    logger.info(f"Envio automatico de notificacion de mangas")
    registro = consulta_datos.mangas_auto(logger=logger)
    registro.reverse()
    
    once_down = []
    
    if len(registro) != 0:
        for inx, i in enumerate(registro):
            if i["titulo"] not in once_down:
                consulta_datos.descargar_img(inx, i, logger)
            
                with open(f"img_tmp/{inx}.jpeg", "rb") as imagenfile:
                    #context.bot.sendPhoto(chat_id=i["chat_id"], photo=imagenfile)
                    updater.bot.sendPhoto(chat_id=i["chat_id"], photo=imagenfile)

                once_down.append(i["titulo"])
                    
            mensaje = mj.NUEVAS_PUBLICACIONES % (i["titulo"], i["capitulo"], i["tipo"], i["scan"], i["url"])
            
            #context.bot.sendMessage(chat_id=i["chat_id"], parse_mode="HTML", text=mensaje)
            updater.bot.sendMessage(chat_id=i["chat_id"], parse_mode="HTML", text=mensaje)
        logger.info(f"Envio automatico finalizado")
    else:
        time.sleep(1)


def start_jobs():
    logger.info("Tarea iniciada")
    tiempo_anterior = 0
    tiempo_actual = 0
    while True:
        tiempo_anterior = tiempo_actual
        time.sleep(1800)
        notificacion_auto()
        tiempo_actual = datetime.now
        logger.info(f"tiempo tarea actual actual: {tiempo_actual} --- tiempo ultima tarea: {tiempo_anterior}")

           
dp.add_handler(CommandHandler("start", bienvenida))
dp.add_handler(CommandHandler(["help", "h"], ayuda))
dp.add_handler(CommandHandler(["agregar_mangas" ,"addm"], agregar_mangas))
dp.add_handler(CommandHandler(["nuevos_mangas" ,"newm"], nuevos_mangas))


if __name__ == "__main__":
    #jobs.run_repeating(notificacion_automatica,1800,10)
    #job_minute = jobs.run_repeating(notificacion_auto, interval=60, first=10)
    logger.info("Tarea inciada... iniciando bot...")
    t = threading.Thread(target=start_jobs)
    t.start()
    run(updater)
    