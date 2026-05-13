from app.database import create_db_and_tables, engine
from app.models.user import User, Event
from sqlmodel import Session, select
from datetime import date

create_db_and_tables()

with Session(engine) as session:
    users = session.exec(select(User)).all()
    if not users:
        print('No hay usuarios. Corré seed_db.py primero.')
        exit()

    events_data = [
        (users[0],  date(2026, 5, 15), "21:00", "Bar El Farol",      "Av. Corrientes 1234", "Buenos Aires",   "Gratis",   "Presentacion del nuevo EP"),
        (users[1],  date(2026, 5, 15), "23:00", "La Trastienda",     "Balcarce 460",        "Buenos Aires",   "$3000",    None),
        (users[2],  date(2026, 5, 20), "20:30", "Centro Cultural",   "San Martin 450",      "Quilmes",        "A la gorra", "Noche de jazz y blues"),
        (users[3],  date(2026, 5, 22), "22:00", "Club Social",       None,                  "Lomas de Zamora","Gratis",   None),
        (users[4],  date(2026, 5, 28), "21:30", "Espacio Cultural",  "Rivadavia 890",       "Avellaneda",     "$2000",    "Con invitados especiales"),
        (users[0],  date(2026, 5, 28), "23:30", "Bar Underground",   "Lavalle 2100",        "Buenos Aires",   "$1500",    None),
        (users[5],  date(2026, 5, 31), "20:00", "Plaza San Martin",  None,                  "Temperley",      "Gratis",   "Fecha al aire libre"),
    ]

    for user, d, time, venue, address, city, price, details in events_data:
        session.add(Event(
            user_id=user.id, date=d, time=time,
            venue=venue, address=address, city=city,
            price=price, details=details
        ))

    session.commit()
    print(f"✅ {len(events_data)} eventos cargados")
