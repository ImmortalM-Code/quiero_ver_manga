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
    "agregar_mangas" : "o /addm. Agrega mangas de interes con una url de tmo y si el manga existe actualiza los generos",
    "buscar_mangas" : "o /seam. buscar tus mangas de interes guardados en el registro",
    "nuevos_mangas" : "o /newm. busca las nuevas publicaciones de mangas que coincidan con tus mangas de interes",
    "help" : "o /h. muestra todos lo comandos disponibles"
}

def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=["start"])
def bienvenida(message):
    mensaje = """
    Bienvenido a MangasUWU\n
    Para iniciar a recibir notificaciones
    sobre las ultimos capitulos de tu mangas de interes
    tienes que agregar mangas al registro
    con el comando /agregarmangas.
    
    usa el comando /help para mas comandos
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
    p = consulta_datos.capitulos_nuevos(parametros=parametros, chat_id=message.chat.id)
    bot.reply_to(message, f"Manga {p} agregado")
    

@bot.message_handler(commands=["nuevos_mangas", "newm"])
def nuevos_mangas(message):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
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
        bot.send_message(message.chat.id, formato, parse_mode="html", disable_web_page_preview=False)
        

print("iniciando bot")
bot.infinity_polling()
