import urllib.request
import conectar
import procesar_html
import models as models
import manejo_datos
import consulta_datos
import telebot
from config import TELEGRAM_TOKEN

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

    for i in registro:
        formato = f"""
<b>{i["titulo"]}</b>
{i["capitulo"]}
{i["tipo"]}
{i["scan"]}
<a href="{i["url"]}">Ir al manga</a>
        """
        #bot.send_photo(message.chat.id, photo=i["imagen"])
        bot.send_message(message.chat.id, formato, parse_mode="html", disable_web_page_preview=True)
        

print("iniciando bot")
bot.infinity_polling()
