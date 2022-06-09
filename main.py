import json
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
        

print("iniciando bot")
bot.infinity_polling()
#soup = conectar.ChargeWeb(url_web)

#print(procesar_html.ultimas_publicaciones(page=1))

#manejo_datos.guardar_manga(obtener_datos.procesar_manga(soup))

#datos = obtener_datos.procesar_datos(soup)

#datos = obtener_datos.obtener_capitulos(soup)

#engine, dbase, session = db.iniciar_db()


"""user = db.Users(name="Javier", number=959791603, number_code=56)
session.add(user)
session.commit()"""

"""users = session.query(db.Users).all()
for user in users:
    print(user)"""

"""
with open("capitulos.json", "w") as file:
    json.dump(datos, file, indent=4)"""
