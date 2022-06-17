import conectar
import procesar_html
import models as models



def guardar_manga(datos : dict, chat_id, session):
    
    #session = db.iniciar_db()
    # Verificar y agregar el manga a la base de datos
    verify_manga = [i.title for i in session.query(models.Mangas).filter_by(title=datos["titulo"][0])]
    if len(verify_manga) == 0:
        mangas = models.Mangas(title=datos["titulo"][0], years=datos["año"][0], state=datos["estado"][0], chat_id=chat_id)
        session.add(mangas)
        session.commit()
    
    # verificar repetidos y guardar generos en la base de datos
    recive_genre = [i for i in datos["generos"][0]]
    
    genre = session.query(models.Genres).all()
    verify_genre = [g.genre for g in genre]
    
    for i in verify_genre:
        for j in recive_genre:
            if i == j:
                recive_genre.remove(i)

    if len(recive_genre) != 0:      
        for g in recive_genre:
            genre = models.Genres(genre=g)
            session.add(genre)
            session.commit()
            genre = session.query(models.Genres).all()
    
    # Revisar y guardar generos de mangas
    # obtener el id del manga
    manga_id = [i.id for i in session.query(models.Mangas).filter_by(title=datos["titulo"][0])][0]
    
    # verificar repetidos y obtener los generos asociados al manga en la base de datos
    verify_mangas_g = [i.genre for i in session.query(models.Genres).join(
            models.Mangas_genres, models.Genres.id == models.Mangas_genres.genres_id ).filter(
            models.Mangas_genres.mangas_id == manga_id)]
    
    
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
            #print(genre_id, g)
            mangas_genres = models.Mangas_genres(mangas_id=manga_id, genres_id=genre_id)
            session.add(mangas_genres)
            session.commit()
    
    session.close()
    
    if len(verify_manga) != 0:
        return True
    else:
        return False
