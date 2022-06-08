import json
import conectar
import procesar_html
import db as db
import manejo_datos


url_web = "https://lectortmo.com/latest_uploads?page=1&uploads_mode=thumbnail"

#soup = conectar.ChargeWeb(url_web)

print(procesar_html.ultimas_publicaciones(page=1))

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
