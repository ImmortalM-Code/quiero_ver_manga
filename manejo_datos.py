import conectar
import procesar_html
import db as db



def guardar_manga(datos : dict):
    
    engine, dbase, session = db.iniciar_db()
    # Verificar y agregar el manga a la base de datos
    verify_manga = [i.title for i in session.query(db.Mangas).filter_by(title=datos["titulo"][0])]
    if len(verify_manga) == 0:
        mangas = db.Mangas(title=datos["titulo"][0], years=datos["año"][0], state=datos["estado"][0], users_id=1)
        session.add(mangas)
        session.commit()
    
    # verificar repetidos y guardar generos en la base de datos
    recive_genre = [i for i in datos["generos"][0]]
    
    genre = session.query(db.Genres).all()
    verify_genre = [g.genre for g in genre]
    
    for i in verify_genre:
        for j in recive_genre:
            if i == j:
                recive_genre.remove(i)

    if len(recive_genre) != 0:      
        for g in recive_genre:
            genre = db.Genres(genre=g)
            session.add(genre)
            session.commit()
            genre = session.query(db.Genres).all()
    
    # Revisar y guardar generos de mangas
    # obtener el id del manga
    manga_id = [i.id for i in session.query(db.Mangas).filter_by(title=datos["titulo"][0])][0]
    # verificar repetidos y obtener los generos asociados al manga en la base de datos
    verify_mangas_g = [i.genre for i in session.query(db.Genres).join(
            db.Mangas_genres, db.Genres.id == db.Mangas_genres.genres_id ).filter(
            db.Mangas_genres.mangas_id == manga_id)]
    
    
    if len(verify_mangas_g) == 0:
            verify_mangas_g = datos["generos"][0]
    else:
        for i in datos["generos"][0]:
            for j in verify_mangas_g:
                if i == j:
                    verify_mangas_g.remove(i)

    
    if len(verify_mangas_g) != 0:
        for g in verify_mangas_g:
            genre_id = [i.id for i in genre if i.genre == g][0]
            print(genre_id, g)
            mangas_genres = db.Mangas_genres(mangas_id=manga_id, genres_id=genre_id)
            session.add(mangas_genres)
            session.commit()
