import threading
import time
import urllib.request
import datetime as dt
from scheduler import Scheduler
import scheduler.trigger as trigger
import conectar
import consulta_datos
import telebot
from config import TELEGRAM_TOKEN

schedule = Scheduler()
bot = telebot.TeleBot(TELEGRAM_TOKEN)

commandos = {
    "agregar_mangas" : "o /addm. Agrega mangas de interés con una url de tmo(puedes mandar mas de una url, separadas por espacios) y si el manga existe actualiza los géneros",
    "buscar_mangas" : "o /seam. buscar tus mangas de interés guardados en el registro",
    "nuevos_mangas" : "o /newm. busca las nuevas publicaciones de mangas que coincidan con tus mangas de interés",
    "help" : "o /h. muestra todos lo comandos disponibles"
}

def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=["start"])
def bienvenida(message):
    mensaje = """
    Bienvenido a MangasUWU\n
    Con MangasUWU podras recibir las ultimas notificaciones
    de tus mangas en TuMangaOnline.
    Para empezar ejecuta el comando /help.
    """
    bot.reply_to(message, mensaje)


@bot.message_handler(commands=["help", "h"])
def ayuda(message):
    ayudas = ""
    for k in commandos:
        ayudas+= f"/{k} : {commandos[k]}\n"
    bot.reply_to(message, ayudas)


@bot.message_handler(commands=["agregar_mangas", "addm"])
def agregar_mangas(message):
    parametros = extract_arg(message.text)
    p = consulta_datos.agregar_mangas(parametros=parametros, chat_id=message.chat.id)
    for n in p:
        bot.reply_to(message, f"El manga {n}")
    

@bot.message_handler(commands=["nuevos_mangas", "newm"])
def nuevos_mangas(message):
    registro = consulta_datos.obtener_nuevos(chat_id=message.chat.id)
    registro.reverse()
    if len(registro) != 0:
        for inx,i in enumerate(registro):
            formato = f"""
<b>{i["titulo"]}</b>
{i["capitulo"]}
{i["tipo"]}
{i["scan"]}
<a href="{i["url"]}">Ir al manga</a>
        """
            with open(f"img_tmp/{inx}.jpeg", "wb") as imagenfile:
                url = urllib.request.Request(i["imagen"], headers=conectar.hdr)
                imagenfile.write(urllib.request.urlopen(url, timeout=20).read())
                    
            with open(f"img_tmp/{inx}.jpeg", "rb") as imagenfile:
                    bot.send_photo(message.chat.id, photo=imagenfile)
            #bot.send_photo(message.chat.id, photo=i["imagen"])
            bot.send_message(message.chat.id, formato, parse_mode="html", disable_web_page_preview=True)
      

def notificacion_automatica():
    registro = consulta_datos.mangas_auto()
    registro.reverse()
    if len(registro) != 0:
        for i, m in enumerate(registro):
            with open(f"img_tmp/{i}.jpeg", "wb") as imagenfile:
            #imagefile = open("img/"+ str(i) + ".jpeg", 'wb')
                url = urllib.request.Request(m["imagen"], headers=conectar.hdr)
                imagenfile.write(urllib.request.urlopen(url, timeout=20).read())
                
            with open(f"img_tmp/{i}.jpeg", "rb") as imagenfile:
                bot.send_photo(m["chat_id"],photo=imagenfile)
            mensaje = f"""
<b>{m["titulo"]}</b>
{m["capitulo"]}
{m["tipo"]}
{m["scan"]}
<a href="{m["url"]}">Ir al manga</a>
            """
            bot.send_message(m["chat_id"],text=mensaje, parse_mode="html", disable_web_page_preview=True)
    print(schedule)
            

def bucle_bot():
    bot.polling()
    
def bucle_temporizador():
    while True:
        schedule.exec_jobs()
        time.sleep(1)

if __name__ == "__main__":
    print("iniciando bot")
    hilo_bot = threading.Thread(name="hilo_bot", target=bucle_bot)
    hilo_bot.start()
    hilo_temp = threading.Thread(name="hilo_temp", target=bucle_temporizador)
    hilo_temp.start()
    print("Bot iniciado")
    schedule.cyclic(dt.timedelta(minutes=2), notificacion_automatica)
    print(schedule)
