"""
Carga fechas de shows en la DB.
Requiere DATABASE_URL en .env apuntando a Neon.
"""
from dotenv import load_dotenv
load_dotenv()

from app.database import engine, create_db_and_tables
from app.models.user import User, Event
from sqlmodel import Session, select
from datetime import date

create_db_and_tables()

shows = [
    # Punk / Hardcore / Post-punk
    {"band": "Bane + Stick To Your Guns",       "date": date(2026, 5, 3),  "venue": "Uniclub",                    "city": "Buenos Aires", "genres": "hardcore, punk"},
    {"band": "Expulsados, Mal Pasar, Quebraditos","date": date(2026, 5, 9), "venue": "Mamadera Bar",               "city": "San Juan",     "genres": "punk"},
    {"band": "The Chameleons",                   "date": date(2026, 5, 14), "venue": "Buenos Aires",               "city": "Buenos Aires", "genres": "post-punk"},
    {"band": "Mon Laferte",                      "date": date(2026, 5, 21), "venue": "Movistar Arena",             "city": "Buenos Aires", "genres": "pop, rock"},
    # Metal / Nu-metal
    {"band": "Six Feet Under + Swallow The Sun", "date": date(2026, 5, 4),  "venue": "Buenos Aires",              "city": "Buenos Aires", "genres": "metal, death metal"},
    {"band": "Vader",                            "date": date(2026, 5, 10), "venue": "Marquee Session",            "city": "Buenos Aires", "genres": "death metal"},
    {"band": "Korn",                             "date": date(2026, 5, 10), "venue": "Parque Sarmiento",           "city": "Buenos Aires", "genres": "nu-metal"},
    {"band": "Groove Metal Fest Vol. 3",         "date": date(2026, 5, 15), "venue": "Groove",                    "city": "Buenos Aires", "genres": "metal"},
    {"band": "Draconian",                        "date": date(2026, 5, 17), "venue": "Teatro Flores",              "city": "Buenos Aires", "genres": "doom metal"},
    {"band": "Cult of Fire",                     "date": date(2026, 5, 17), "venue": "Uniclub",                   "city": "Buenos Aires", "genres": "black metal"},
    {"band": "The Amity Affliction",             "date": date(2026, 5, 22), "venue": "Uniclub",                   "city": "Buenos Aires", "genres": "metalcore"},
    {"band": "Drowning Pool",                    "date": date(2026, 5, 26), "venue": "Teatro Vorterix",            "city": "Buenos Aires", "genres": "nu-metal"},
    {"band": "Buenos Aires Nu Metal Fest",       "date": date(2026, 5, 29), "venue": "Arkham Multiespacio",        "city": "Buenos Aires", "genres": "nu-metal"},
    # Indie Rock
    {"band": "Gauchito Club",                    "date": date(2026, 5, 2),  "venue": "Buenos Aires",              "city": "Buenos Aires", "genres": "indie"},
    {"band": "Portugal. The Man",                "date": date(2026, 5, 14), "venue": "C Art Media",               "city": "Buenos Aires", "genres": "indie rock"},
    {"band": "POGOFEST",                         "date": date(2026, 5, 19), "venue": "Teatro Vorterix",            "city": "Buenos Aires", "genres": "indie rock"},
    {"band": "Wolf Alice",                       "date": date(2026, 5, 25), "venue": "C Art Media",               "city": "Buenos Aires", "genres": "indie rock"},
    {"band": "Horsegirl",                        "date": date(2026, 5, 26), "venue": "Niceto Club",               "city": "Buenos Aires", "genres": "indie rock"},
    # Trap
    {"band": "Smile Trap Sessions",              "date": date(2026, 5, 9),  "venue": "Museum Live",               "city": "Buenos Aires", "genres": "trap"},
    {"band": "Modo Diablo",                      "date": date(2026, 5, 10), "venue": "Estadio Malvinas Argentinas","city": "Buenos Aires", "genres": "trap"},
    {"band": "Ca7riel & Paco Amoroso",           "date": date(2026, 5, 14), "venue": "Movistar Arena",            "city": "Buenos Aires", "genres": "trap, rap"},
    # Junio - Metal
    {"band": "Buenos Aires Nu Metal Fest",       "date": date(2026, 6, 6),  "venue": "Mole Club",                 "city": "Mar del Plata", "genres": "nu-metal"},
    {"band": "Tygers of Pan Tang",               "date": date(2026, 6, 2),  "venue": "Uniclub",                   "city": "Buenos Aires", "genres": "heavy metal"},
    {"band": "Masacre",                          "date": date(2026, 6, 19), "venue": "Marquee Session Live",       "city": "Buenos Aires", "genres": "death metal"},
    {"band": "Bertoncelli",                      "date": date(2026, 6, 20), "venue": "Buenos Aires",              "city": "Buenos Aires", "genres": "rock"},
    {"band": "Drowning Pool",                    "date": date(2026, 6, 26), "venue": "Teatro Vorterix",            "city": "Buenos Aires", "genres": "nu-metal"},
    # Junio - Indie / Rock
    {"band": "Pulp",                             "date": date(2026, 6, 12), "venue": "Movistar Arena",            "city": "Buenos Aires", "genres": "indie rock, britpop"},
    {"band": "Shame",                            "date": date(2026, 6, 17), "venue": "Niceto Club",               "city": "Buenos Aires", "genres": "post-punk"},
    {"band": "Andrés Calamaro",                  "date": date(2026, 6, 3),  "venue": "Movistar Arena",            "city": "Buenos Aires", "genres": "rock"},
    {"band": "Soda Stereo",                      "date": date(2026, 6, 4),  "venue": "Movistar Arena",            "city": "Buenos Aires", "genres": "rock"},
    {"band": "Guasones",                         "date": date(2026, 6, 6),  "venue": "Estadio Atenas",            "city": "La Plata",     "genres": "rock"},
    {"band": "WOS",                              "date": date(2026, 6, 12), "venue": "Club Alemán",               "city": "Buenos Aires", "genres": "rap, hip-hop"},
    {"band": "Las Pastillas del Abuelo",         "date": date(2026, 6, 14), "venue": "Estadio Centro",            "city": "Buenos Aires", "genres": "rock"},
    {"band": "La Vela Puerca",                   "date": date(2026, 6, 20), "venue": "Garage Club",               "city": "Buenos Aires", "genres": "rock"},
    {"band": "Nonpalidece",                      "date": date(2026, 6, 20), "venue": "Arena Sur",                 "city": "Buenos Aires", "genres": "reggae"},
    {"band": "Babasónicos",                      "date": date(2026, 6, 25), "venue": "Movistar Arena",            "city": "Buenos Aires", "genres": "rock"},
    {"band": "Redd Kross",                       "date": date(2026, 6, 24), "venue": "Uniclub",                   "city": "Buenos Aires", "genres": "rock"},
    {"band": "Wolf Alice",                       "date": date(2026, 6, 28), "venue": "C Complejo Art Media",      "city": "Buenos Aires", "genres": "indie rock"},
]

with Session(engine) as session:
    # Crear un usuario "Bandeo" para las fechas cargadas por el admin
    admin_user = session.exec(
        select(User).where(User.edit_token == "bandeo-admin-shows")
    ).first()

    if not admin_user:
        from app.utils import generate_edit_token
        admin_user = User(
            display_name="Bandeo",
            role="BANDA",
            edit_token="bandeo-admin-shows",
            status="approved"
        )
        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)

    count = 0
    for show in shows:
        event = Event(
            user_id=admin_user.id,
            band_name=show["band"],
            date=show["date"],
            venue=show["venue"],
            city=show["city"],
            details=show["genres"],
            status="approved"
        )
        session.add(event)
        count += 1

    session.commit()
    print(f"{count} fechas cargadas")
