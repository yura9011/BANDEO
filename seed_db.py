from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models.user import User, Profile
from app.utils import get_coordinates, generate_edit_token, clean_phone_number, normalize_text_list
import asyncio

async def seed():
    print("🌱 Cargando perfiles de prueba...")
    create_db_and_tables()

    with Session(engine) as session:
        # Limpiar todo
        for p in session.exec(__import__('sqlmodel').select(Profile)).all():
            session.delete(p)
        for u in session.exec(__import__('sqlmodel').select(User)).all():
            session.delete(u)
        session.commit()

        test_data = [
            # --- MÚSICOS ---
            {
                "display_name": "Pablo Ruiz",
                "role": "MUSICO",
                "city": "Lomas de Zamora",
                "instruments": "Guitarra Eléctrica",
                "genres": "Blues, Rock",
                "bio": "Guitarrista con 15 años de experiencia. Busco banda estable para tocar en vivo. Tengo equipo propio y movilidad.",
                "phone": "541155001001",
                "instagram": "@pabloruizguitar",
                "yt": "https://www.youtube.com/watch?v=Kz9m_pZ5E7Y",
                "spotify": None,
            },
            {
                "display_name": "Carolina Méndez",
                "role": "MUSICO",
                "city": "Adrogué",
                "instruments": "Batería, Percusión",
                "genres": "Jazz, Funk",
                "bio": "Sesionista con 10 años de experiencia. Disponible para grabaciones y fechas en vivo. Tengo batería acústica y electrónica.",
                "phone": "541155002002",
                "instagram": "@caro.drums",
                "yt": None,
                "spotify": None,
            },
            {
                "display_name": "Martín Sosa",
                "role": "MUSICO",
                "city": "Quilmes",
                "instruments": "Bajo",
                "genres": "Metal, Hard Rock",
                "bio": "Bajista de 5 cuerdas. Busco banda formada con fechas. No busco proyecto desde cero.",
                "phone": "541155003003",
                "instagram": None,
                "yt": "https://www.youtube.com/watch?v=I8Z-69vAAn0",
                "spotify": None,
            },
            {
                "display_name": "Sofía Herrera",
                "role": "MUSICO",
                "city": "San Justo",
                "instruments": "Voz",
                "genres": "Pop, Soul, R&B",
                "bio": "Cantante con formación clásica y experiencia en pop. Busco banda o proyecto para grabar y tocar en vivo.",
                "phone": "541155004004",
                "instagram": "@sofiaherreravoz",
                "yt": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "spotify": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
            },
            {
                "display_name": "Diego Ferreyra",
                "role": "MUSICO",
                "city": "Lanús",
                "instruments": "Teclado, Piano",
                "genres": "Rock, Blues, Jazz",
                "bio": "Tecladista versátil. Toco en vivo hace 8 años. Disponible para sesiones y banda estable.",
                "phone": "541155005005",
                "instagram": "@diegokeys",
                "yt": None,
                "spotify": None,
            },
            {
                "display_name": "Ramiro Vega",
                "role": "MUSICO",
                "city": "Florencio Varela",
                "instruments": "Guitarra Acústica, Voz",
                "genres": "Folk, Indie, Acústico",
                "bio": "Músico solista buscando colaboradores para proyecto indie acústico. Tengo temas propios grabados.",
                "phone": "541155006006",
                "instagram": "@ramiro.vega.musica",
                "yt": "https://www.youtube.com/watch?v=Kz9m_pZ5E7Y",
                "spotify": None,
            },
            {
                "display_name": "Lucas Peralta",
                "role": "MUSICO",
                "city": "Avellaneda",
                "instruments": "Saxo Tenor, Saxo Alto",
                "genres": "Jazz, Bossa Nova, Funk",
                "bio": "Saxofonista con 12 años de experiencia. Toco en orquestas y combos de jazz. Disponible para sesiones.",
                "phone": "541155007007",
                "instagram": "@lucassaxo",
                "yt": None,
                "spotify": None,
            },
            {
                "display_name": "Valeria Torres",
                "role": "MUSICO",
                "city": "Temperley",
                "instruments": "Violín",
                "genres": "Clásico, Folk, Post-Rock",
                "bio": "Violinista clásica con ganas de explorar otros géneros. Abierta a proyectos experimentales.",
                "phone": None,
                "instagram": "@vale.violin",
                "yt": None,
                "spotify": None,
            },
            # --- BANDAS ---
            {
                "display_name": "La Octava",
                "role": "BANDA",
                "city": "Temperley",
                "instruments": "Buscamos Bajista",
                "genres": "Rock Alternativo",
                "bio": "Banda de zona sur con 3 años de trayectoria, temas propios y fechas programadas. Ensayamos los jueves en Temperley.",
                "phone": "541155008008",
                "instagram": "@laoctavarock",
                "yt": "https://www.youtube.com/watch?v=Xq3shV89U0A",
                "spotify": None,
            },
            {
                "display_name": "Ezeiza Jazz Trio",
                "role": "BANDA",
                "city": "Ezeiza",
                "instruments": "Buscamos Baterista",
                "genres": "Jazz, Bossa Nova",
                "bio": "Trío de jazz buscando baterista con sutileza y experiencia en jazz. Tocamos en bares y eventos privados.",
                "phone": "541155009009",
                "instagram": "@ezeizajazz",
                "yt": None,
                "spotify": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
            },
            {
                "display_name": "Under Metal",
                "role": "BANDA",
                "city": "Lanús",
                "instruments": "Buscamos Guitarrista",
                "genres": "Thrash Metal, Death Metal",
                "bio": "Proyecto serio con temas propios. Ensayamos en Lanús centro. Buscamos guitarrista con experiencia en metal extremo.",
                "phone": "541155010010",
                "instagram": "@undermetal.arg",
                "yt": "https://www.youtube.com/watch?v=u6_UvP4_uBw",
                "spotify": None,
            },
            {
                "display_name": "Cumbia Villera FC",
                "role": "BANDA",
                "city": "Lomas de Zamora",
                "instruments": "Buscamos Cantante",
                "genres": "Cumbia, Cumbia Villera",
                "bio": "Banda de cumbia con 5 años en la escena. Tocamos en bailes y eventos. Buscamos cantante con presencia escénica.",
                "phone": "541155011011",
                "instagram": "@cumbiavillerafc",
                "yt": None,
                "spotify": None,
            },
            {
                "display_name": "Los Pibes del Indie",
                "role": "BANDA",
                "city": "Quilmes",
                "instruments": "Buscamos Baterista y Bajista",
                "genres": "Indie, Post-Punk, Shoegaze",
                "bio": "Banda nueva con influencias de Interpol, The Cure y Soda Stereo. Buscamos completar la formación para empezar a ensayar.",
                "phone": None,
                "instagram": "@lospibesdelindieok",
                "yt": None,
                "spotify": None,
            },
            {
                "display_name": "Orquesta Típica Sur",
                "role": "BANDA",
                "city": "Avellaneda",
                "instruments": "Buscamos Violinista y Pianista",
                "genres": "Tango, Milonga",
                "bio": "Orquesta típica de tango con 10 músicos. Tocamos en milongas y eventos culturales. Buscamos completar la sección de cuerdas.",
                "phone": "541155012012",
                "instagram": "@orquestatipicasur",
                "yt": "https://www.youtube.com/watch?v=Kz9m_pZ5E7Y",
                "spotify": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
            },
            {
                "display_name": "Reggae Roots BA",
                "role": "BANDA",
                "city": "Florencio Varela",
                "instruments": "Buscamos Bajista y Teclado",
                "genres": "Reggae, Dub, Ska",
                "bio": "Banda de reggae roots con mensaje. Tocamos en plazas, festivales y centros culturales. Buscamos completar la sección rítmica.",
                "phone": "541155013013",
                "instagram": "@reggaerootsba",
                "yt": None,
                "spotify": None,
            },
        ]

        edit_tokens = []

        for item in test_data:
            print(f"  → {item['display_name']} ({item['city']})")

            edit_token = generate_edit_token()

            user = User(
                display_name=item["display_name"],
                role=item["role"],
                edit_token=edit_token
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            edit_tokens.append({
                "name": item["display_name"],
                "token": edit_token,
                "user_id": user.id
            })

            lat, lng = await get_coordinates(item["city"])

            profile = Profile(
                user_id=user.id,
                city=item["city"],
                lat=lat,
                lng=lng,
                instruments=normalize_text_list(item["instruments"]),
                genres=normalize_text_list(item["genres"]),
                bio=item.get("bio"),
                phone=clean_phone_number(item["phone"]) if item.get("phone") else None,
                instagram_link=item.get("instagram"),
                youtube_links=item.get("yt"),
                spotify_link=item.get("spotify"),
            )
            session.add(profile)
            session.commit()

    print(f"\n✅ {len(test_data)} perfiles cargados")
    print("\nLinks de edición:")
    for t in edit_tokens:
        print(f"  {t['name']}: http://localhost:8000/edit/{t['token']}")

if __name__ == "__main__":
    asyncio.run(seed())
