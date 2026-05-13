from fastapi import FastAPI, Request, Form, Depends, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, func
from app.database import create_db_and_tables, get_session
from app.models.user import User, Profile, Post, Event
from app.utils import (
    get_coordinates,
    calculate_distance,
    extract_youtube_id,
    generate_edit_token,
    generate_whatsapp_link,
    normalize_instagram_link,
    clean_phone_number,
    normalize_text_list,
    validate_url
)
from typing import Optional
import uvicorn
import calendar
import os
import secrets
from datetime import date, datetime
from dotenv import load_dotenv

load_dotenv()

ADMIN_USER     = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_SECRET   = os.getenv("ADMIN_SECRET")

app = FastAPI(title="BANDEO")

def check_admin(admin_token: Optional[str] = Cookie(None)) -> bool:
    return admin_token == ADMIN_SECRET

def require_admin(admin_token: Optional[str] = Cookie(None)):
    if admin_token != ADMIN_SECRET:
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})

# Inicializar DB una sola vez (lazy, compatible con Vercel serverless)
_db_initialized = False

def ensure_db():
    global _db_initialized
    if not _db_initialized:
        create_db_and_tables()
        _db_initialized = True

ensure_db()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
templates.env.cache = {}  # deshabilitar cache para evitar bug con globals
templates.env.globals["extract_youtube_id"] = extract_youtube_id
templates.env.globals["generate_whatsapp_link"] = generate_whatsapp_link
templates.env.globals["normalize_instagram_link"] = normalize_instagram_link

# ── DIRECTORIO ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, session: Session = Depends(get_session)):
    profiles = session.exec(
        select(Profile).join(User).where(User.status == "approved").limit(100)
    ).all()
    return templates.TemplateResponse("landing.html", {"request": request, "profiles": profiles})

# ── CREAR PERFIL ──────────────────────────────────────────────────────────────

@app.get("/create", response_class=HTMLResponse)
async def get_create_profile_form(request: Request):
    return templates.TemplateResponse("create_profile.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_profile(
    request: Request,
    role: str = Form(...),
    display_name: str = Form(...),
    city: str = Form(...),
    instruments: str = Form(...),
    genres: str = Form(...),
    bio: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    youtube_links: Optional[str] = Form(None),
    spotify_link: Optional[str] = Form(None),
    instagram_link: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    if role not in ["MUSICO", "BANDA"]:
        raise HTTPException(status_code=400, detail="Rol inválido")
    if spotify_link and not validate_url(spotify_link):
        raise HTTPException(status_code=400, detail="URL de Spotify inválida")

    for attempt in range(3):
        try:
            edit_token = generate_edit_token()
            new_user = User(role=role, display_name=display_name.strip(), edit_token=edit_token)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            break
        except Exception:
            if attempt == 2:
                raise HTTPException(status_code=500, detail="Error creando usuario")
            session.rollback()

    lat, lng = await get_coordinates(city)
    new_profile = Profile(
        user_id=new_user.id,
        city=city.strip(), lat=lat, lng=lng,
        instruments=normalize_text_list(instruments),
        genres=normalize_text_list(genres),
        bio=bio.strip() if bio else None,
        phone=clean_phone_number(phone),
        youtube_links=youtube_links.strip() if youtube_links else None,
        spotify_link=spotify_link.strip() if spotify_link else None,
        instagram_link=instagram_link.strip() if instagram_link else None,
    )
    session.add(new_profile)
    session.commit()

    return templates.TemplateResponse("profile_created.html", {
        "request": request, "edit_token": edit_token, "user_id": new_user.id
    })

# ── EDITAR PERFIL ─────────────────────────────────────────────────────────────

@app.get("/edit/{edit_token}", response_class=HTMLResponse)
async def get_edit_profile_form(request: Request, edit_token: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.edit_token == edit_token)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Token inválido")
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    return templates.TemplateResponse("edit_profile.html", {
        "request": request, "user": user, "profile": profile, "edit_token": edit_token
    })

@app.post("/edit/{edit_token}", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    edit_token: str,
    display_name: str = Form(...),
    city: str = Form(...),
    instruments: str = Form(...),
    genres: str = Form(...),
    bio: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    youtube_links: Optional[str] = Form(None),
    spotify_link: Optional[str] = Form(None),
    instagram_link: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.edit_token == edit_token)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Token inválido")
    if spotify_link and not validate_url(spotify_link):
        raise HTTPException(status_code=400, detail="URL de Spotify inválida")

    user.display_name = display_name.strip()
    session.add(user)

    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    if profile:
        lat, lng = await get_coordinates(city)
        profile.city = city.strip()
        profile.lat = lat; profile.lng = lng
        profile.instruments = normalize_text_list(instruments)
        profile.genres = normalize_text_list(genres)
        profile.bio = bio.strip() if bio else None
        profile.phone = clean_phone_number(phone)
        profile.youtube_links = youtube_links.strip() if youtube_links else None
        profile.spotify_link = spotify_link.strip() if spotify_link else None
        profile.instagram_link = instagram_link.strip() if instagram_link else None
        session.add(profile)

    session.commit()
    return templates.TemplateResponse("profile_updated.html", {
        "request": request, "user": user, "edit_token": edit_token
    })

# ── VER PERFIL ────────────────────────────────────────────────────────────────

@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def get_profile_detail(request: Request, user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404)
    profile = session.exec(select(Profile).where(Profile.user_id == user_id)).first()
    if not profile:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("profile_detail.html", {
        "request": request, "user": user, "profile": profile
    })

# ── BANDAS ────────────────────────────────────────────────────────────────────

@app.get("/bandas", response_class=HTMLResponse)
async def bandas_page(request: Request, session: Session = Depends(get_session)):
    posts = session.exec(
        select(Post).where(Post.status == "approved").order_by(Post.created_at.desc()).limit(100)
    ).all()
    return templates.TemplateResponse("bandas.html", {"request": request, "posts": posts})

@app.get("/bandas/nuevo", response_class=HTMLResponse)
async def nuevo_post_form(request: Request, token: Optional[str] = None, session: Session = Depends(get_session)):
    if not token:
        return templates.TemplateResponse("bandas_token.html", {"request": request})
    user = session.exec(select(User).where(User.edit_token == token)).first()
    if not user:
        return templates.TemplateResponse("bandas_token.html", {"request": request, "error": "Token inválido."})
    return templates.TemplateResponse("bandas_nuevo.html", {"request": request, "user": user, "token": token})

@app.post("/bandas/nuevo", response_class=HTMLResponse)
async def crear_post(request: Request, token: str = Form(...), content: str = Form(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.edit_token == token)).first()
    if not user:
        raise HTTPException(status_code=403, detail="Token inválido")
    content = content.strip()
    if not content or len(content) > 500:
        raise HTTPException(status_code=400, detail="Contenido inválido")
    session.add(Post(user_id=user.id, content=content))
    session.commit()
    return templates.TemplateResponse("bandas_post_creado.html", {"request": request, "user": user})

# ── CALENDARIO ────────────────────────────────────────────────────────────────

@app.get("/fechas", response_class=HTMLResponse)
async def fechas_page(
    request: Request,
    year: Optional[int] = None,
    month: Optional[int] = None,
    session: Session = Depends(get_session)
):
    today = date.today()
    year  = year  or today.year
    month = month or today.month

    # Navegar entre meses válidos
    year  = max(2020, min(2030, year))
    month = max(1, min(12, month))

    # Mes anterior / siguiente
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    # Días del mes
    cal = calendar.monthcalendar(year, month)

    # Eventos del mes
    first_day = date(year, month, 1)
    last_day  = date(year, month, calendar.monthrange(year, month)[1])
    events = session.exec(
        select(Event)
        .where(Event.status == "approved")
        .where(Event.date >= first_day)
        .where(Event.date <= last_day)
        .order_by(Event.date, Event.time)
    ).all()

    # Agrupar por día
    events_by_day: dict = {}
    for ev in events:
        events_by_day.setdefault(ev.date.day, []).append(ev)

    month_names = ["", "Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    return templates.TemplateResponse("fechas.html", {
        "request": request,
        "year": year, "month": month,
        "month_name": month_names[month],
        "cal": cal,
        "events_by_day": events_by_day,
        "today": today,
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
    })

@app.get("/fechas/nueva", response_class=HTMLResponse)
async def nueva_fecha_form(request: Request, token: Optional[str] = None, session: Session = Depends(get_session)):
    if not token:
        return templates.TemplateResponse("fechas_token.html", {"request": request})
    user = session.exec(select(User).where(User.edit_token == token)).first()
    if not user:
        return templates.TemplateResponse("fechas_token.html", {"request": request, "error": "Token inválido."})
    return templates.TemplateResponse("fechas_nueva.html", {"request": request, "user": user, "token": token})

@app.post("/fechas/nueva", response_class=HTMLResponse)
async def crear_fecha(
    request: Request,
    token: str = Form(...),
    band_name: Optional[str] = Form(None),
    event_date: str = Form(...),
    time: Optional[str] = Form(None),
    venue: str = Form(...),
    address: Optional[str] = Form(None),
    city: str = Form(...),
    price: Optional[str] = Form(None),
    details: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.edit_token == token)).first()
    if not user:
        raise HTTPException(status_code=403, detail="Token inválido")

    try:
        parsed_date = date.fromisoformat(event_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Fecha inválida")

    event = Event(
        user_id=user.id,
        band_name=band_name.strip() if band_name else user.display_name,
        date=parsed_date,
        time=time.strip() if time else None,
        venue=venue.strip(),
        address=address.strip() if address else None,
        city=city.strip(),
        price=price.strip() if price else None,
        details=details.strip() if details else None,
    )
    session.add(event)
    session.commit()

    return templates.TemplateResponse("fechas_creada.html", {
        "request": request, "user": user, "event": event
    })

@app.get("/debug-env")
async def debug_env():
    """Temporal — verificar variables de entorno en Vercel. Borrar después."""
    db_url = os.environ.get("DATABASE_URL", "NO ENCONTRADA")
    # Ocultar la contraseña
    if "@" in db_url:
        db_url = db_url.split("@")[0].rsplit(":", 1)[0] + ":***@" + db_url.split("@")[1]
    return {"DATABASE_URL": db_url, "has_db": bool(os.environ.get("DATABASE_URL"))}

@app.get("/admin/fix-band-names")
async def fix_band_names(
    admin_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
):
    """Actualiza band_name en los eventos existentes cargados por el admin."""
    if admin_token != ADMIN_SECRET:
        return RedirectResponse(url="/admin/login", status_code=303)

    from datetime import date as d
    fixes = {
        (d(2026,5,3),  "Uniclub"):                     "Bane + Stick To Your Guns",
        (d(2026,5,9),  "Mamadera Bar"):                 "Expulsados, Mal Pasar, Quebraditos",
        (d(2026,5,14), "Buenos Aires"):                 "The Chameleons",
        (d(2026,5,21), "Movistar Arena"):               "Mon Laferte",
        (d(2026,5,4),  "Buenos Aires"):                 "Six Feet Under + Swallow The Sun",
        (d(2026,5,10), "Marquee Session"):              "Vader",
        (d(2026,5,10), "Parque Sarmiento"):             "Korn",
        (d(2026,5,15), "Groove"):                       "Groove Metal Fest Vol. 3",
        (d(2026,5,17), "Teatro Flores"):                "Draconian",
        (d(2026,5,17), "Uniclub"):                      "Cult of Fire",
        (d(2026,5,22), "Uniclub"):                      "The Amity Affliction",
        (d(2026,5,26), "Teatro Vorterix"):              "Drowning Pool",
        (d(2026,5,29), "Arkham Multiespacio"):          "Buenos Aires Nu Metal Fest",
        (d(2026,5,2),  "Buenos Aires"):                 "Gauchito Club",
        (d(2026,5,14), "C Art Media"):                  "Portugal. The Man",
        (d(2026,5,19), "Teatro Vorterix"):              "POGOFEST",
        (d(2026,5,25), "C Art Media"):                  "Wolf Alice",
        (d(2026,5,26), "Niceto Club"):                  "Horsegirl",
        (d(2026,5,9),  "Museum Live"):                  "Smile Trap Sessions",
        (d(2026,5,10), "Estadio Malvinas Argentinas"):  "Modo Diablo",
        (d(2026,5,14), "Movistar Arena"):               "Ca7riel & Paco Amoroso",
        (d(2026,6,6),  "Mole Club"):                    "Buenos Aires Nu Metal Fest MdP",
        (d(2026,6,2),  "Uniclub"):                      "Tygers of Pan Tang",
        (d(2026,6,19), "Marquee Session Live"):         "Masacre",
        (d(2026,6,26), "Teatro Vorterix"):              "Drowning Pool",
        (d(2026,6,12), "Movistar Arena"):               "Pulp",
        (d(2026,6,17), "Niceto Club"):                  "Shame",
        (d(2026,6,3),  "Movistar Arena"):               "Andres Calamaro",
        (d(2026,6,4),  "Movistar Arena"):               "Soda Stereo",
        (d(2026,6,6),  "Estadio Atenas"):               "Guasones",
        (d(2026,6,12), "Club Aleman"):                  "WOS",
        (d(2026,6,14), "Estadio Centro"):               "Las Pastillas del Abuelo",
        (d(2026,6,20), "Garage Club"):                  "La Vela Puerca",
        (d(2026,6,20), "Arena Sur"):                    "Nonpalidece",
        (d(2026,6,25), "Movistar Arena"):               "Babasónicos",
        (d(2026,6,24), "Uniclub"):                      "Redd Kross",
    }

    events = session.exec(select(Event)).all()
    count = 0
    for ev in events:
        name = fixes.get((ev.date, ev.venue))
        if name and not ev.band_name:
            ev.band_name = name
            session.add(ev)
            count += 1

    session.commit()
    return {"ok": True, "updated": count}

@app.get("/admin/debug-events")
async def debug_events(
    admin_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
):
    if admin_token != ADMIN_SECRET:
        return RedirectResponse(url="/admin/login", status_code=303)
    events = session.exec(select(Event).limit(5)).all()
    return {
        "total": len(events),
        "sample": [{"id": e.id, "date": str(e.date), "venue": e.venue, "band_name": e.band_name, "status": e.status} for e in events]
    }

@app.get("/admin/migrate")
async def migrate(
    admin_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
):
    if admin_token != ADMIN_SECRET:
        return RedirectResponse(url="/admin/login", status_code=303)
    from sqlalchemy import text
    from app.database import engine as db_engine
    with db_engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE event ADD COLUMN band_name VARCHAR"))
            conn.commit()
            return {"ok": True, "msg": "columna band_name agregada"}
        except Exception as e:
            conn.rollback()
            if "already exists" in str(e):
                return {"ok": True, "msg": "columna ya existia"}
            return {"ok": False, "error": str(e)}

@app.get("/legal", response_class=HTMLResponse)
async def legal_page(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})

# ── ADMIN ─────────────────────────────────────────────────────────────────────

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie("admin_token", ADMIN_SECRET, httponly=True, max_age=60*60*8)
        return response
    return RedirectResponse(url="/admin/login?error=1", status_code=303)

@app.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_token")
    return response

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    admin_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
):
    if admin_token != ADMIN_SECRET:
        return RedirectResponse(url="/admin/login", status_code=303)

    # Estadísticas
    total_users    = session.exec(select(func.count(User.id))).one()
    pending_users  = session.exec(select(func.count(User.id)).where(User.status == "pending")).one()
    approved_users = session.exec(select(func.count(User.id)).where(User.status == "approved")).one()

    total_posts    = session.exec(select(func.count(Post.id))).one()
    pending_posts  = session.exec(select(func.count(Post.id)).where(Post.status == "pending")).one()

    total_events   = session.exec(select(func.count(Event.id))).one()
    pending_events = session.exec(select(func.count(Event.id)).where(Event.status == "pending")).one()

    # Pendientes
    pending_user_list  = session.exec(select(User).where(User.status == "pending").order_by(User.created_at.desc())).all()
    pending_post_list  = session.exec(select(Post).where(Post.status == "pending").order_by(Post.created_at.desc())).all()
    pending_event_list = session.exec(select(Event).where(Event.status == "pending").order_by(Event.created_at.desc())).all()

    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "stats": {
            "total_users": total_users, "pending_users": pending_users, "approved_users": approved_users,
            "total_posts": total_posts, "pending_posts": pending_posts,
            "total_events": total_events, "pending_events": pending_events,
        },
        "pending_users": pending_user_list,
        "pending_posts": pending_post_list,
        "pending_events": pending_event_list,
    })

@app.post("/admin/approve/{entity}/{id}", response_class=HTMLResponse)
async def admin_approve(
    entity: str, id: int,
    admin_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
):
    if admin_token != ADMIN_SECRET:
        return RedirectResponse(url="/admin/login", status_code=303)

    if entity == "user":
        obj = session.get(User, id)
    elif entity == "post":
        obj = session.get(Post, id)
    elif entity == "event":
        obj = session.get(Event, id)
    else:
        raise HTTPException(status_code=400)

    if obj:
        obj.status = "approved"
        session.add(obj)
        session.commit()

    return RedirectResponse(url="/admin", status_code=303)

@app.post("/admin/reject/{entity}/{id}", response_class=HTMLResponse)
async def admin_reject(
    entity: str, id: int,
    admin_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_session)
):
    if admin_token != ADMIN_SECRET:
        return RedirectResponse(url="/admin/login", status_code=303)

    if entity == "user":
        obj = session.get(User, id)
    elif entity == "post":
        obj = session.get(Post, id)
    elif entity == "event":
        obj = session.get(Event, id)
    else:
        raise HTTPException(status_code=400)

    if obj:
        obj.status = "rejected"
        session.add(obj)
        session.commit()

    return RedirectResponse(url="/admin", status_code=303)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
