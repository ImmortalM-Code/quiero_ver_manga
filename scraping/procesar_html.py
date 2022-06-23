import bs4
import re
import scraping.conectar as conectar

def obtener_capitulos(datos):
    base = datos.find("div", id="chapters")
    seccion_caps = base.find_all("li")
    
    capitulos = []
    
    for c in seccion_caps:
        if c.find("a", class_="btn-collapse").__class__ is bs4.element.Tag:
            n_capitulo = c.find("a", class_="btn-collapse").get_text(strip=True, separator=" ")
            scanners = []
            
            scans = c.find("div", class_="card chapter-list-element").find_all("li")
            
            for scan in scans:
                scanners.append({
                    "scan" : scan.find("div", class_="col-4 col-md-6 text-truncate").get_text(strip=True, separator=" "),
                    "fecha" : scan.find("div", class_="col-4 col-md-2 text-center").get_text(strip=True, separator=" ")
                })
        
            capitulos.append({
                "capitulo" : n_capitulo,
                "scanners" : scanners
            })
    
    return capitulos


def procesar_manga(datos):
    registro = {}
    # Datos de el encabezado
    base = datos.find("div", class_="col-12 col-md-9 element-header-content-text")
    generos_bruto = base.find_all("h6")
    #titulo = re.compile(r"[a-zA-Z].+").search(titulo_completo)[0]                  respaldo
    titulo = base.find("h2", class_="element-subtitle").get_text()
    html_anio = base.find("h1", class_="element-title my-2").find("small")
    anio = ""
    
    if html_anio != None:
        anio = re.compile(r"(?<=\( ).+(?= \))").search(html_anio.get_text())[0]
    else:
        anio = "Sin Año"
    
    estado_ex = re.compile(r'book-status.+(?=">[A-Z])').search(str(base))[0]
    estado = base.find("span", class_=estado_ex).get_text()
    
    generos = []
    for g in generos_bruto:
        generos.append(g.get_text())
    
    
    registro["titulo"] = titulo,
    registro["año"] = anio,
    registro["estado"] = estado,
    registro["generos"] = generos,
    #registro["capitulos"] = obtener_capitulos(datos)
    
    
    return registro


def ultimas_publicaciones(datos=None, page=1):
    pag = 0
    if page==1:
        pag=0
        datos = conectar.ChargeWeb("https://lectortmo.com/latest_uploads?page=1&uploads_mode=thumbnail")
    elif page==2:
        pag=30
        datos = conectar.ChargeWeb("https://lectortmo.com/latest_uploads?page=2&uploads_mode=thumbnail")
    elif page==3:
        pag=60
        datos = conectar.ChargeWeb("https://lectortmo.com/latest_uploads?page=3&uploads_mode=thumbnail")
    elif page==4:
        pag=90
        datos = conectar.ChargeWeb("https://lectortmo.com/latest_uploads?page=4&uploads_mode=thumbnail")
    
    ultimos_caps = []
    img_prosesada = lambda texto : re.compile(r"(?<=\(').+?(?='\))").search(str(texto))[0]
    base = datos.find("div", class_="col-12 col-lg-8 col-xl-9")
    capitulos = base.find("div", class_="row").find_all("div", class_="col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 mt-2 upload-file-row")
    
    for i,c in enumerate(capitulos):
        capitulo = ""
        if c.a.div.span.get_text() == "ONE SHOT": capitulo = "0" 
        else: capitulo = c.a.find("div", class_="thumbnail-footer").find("span", class_="number").get_text()
        ultimos_caps.append({
            "titulo" : c.find("div", class_="thumbnail-title").find("h4", class_="text-truncate").get_text(),
            "capitulo" : capitulo,
            "tipo" : c.a.div.span.get_text(),
            "imagen" : img_prosesada(c.find("div", class_=f"thumbnail upload upload-thumbnail-{pag+i}").find(f"style")),
            "url" : c.a['href'],
            "scan" : c.find("span", class_="groups").get_text(),
            "hora" : c.find("div", class_="upload_time badge").get_text()
        })
    
    return ultimos_caps
