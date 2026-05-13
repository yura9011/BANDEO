import httpx
import math
import secrets
import re
from typing import Optional, Tuple

async def get_coordinates(city_name: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Obtiene latitud y longitud desde OpenStreetMap Nominatim.
    Incluye timeout y manejo de errores para evitar bloqueos.
    """
    if not city_name or not city_name.strip():
        return None, None
        
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    headers = {"User-Agent": "BandeoApp/0.2.1 (contact: bandeo@example.com)"}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception as e:
            print(f"Error geocoding {city_name}: {e}")
            
    # Si falla, devolvemos None para que el perfil se cree sin coordenadas
    return None, None

def calculate_distance(lat1: Optional[float], lon1: Optional[float], 
                       lat2: Optional[float], lon2: Optional[float]) -> Optional[float]:
    """
    Calcula la distancia en KM usando fórmula de Haversine.
    Retorna None si alguna coordenada es None.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None
    
    R = 6371  # Radio de la Tierra en km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def extract_youtube_id(url: str) -> Optional[str]:
    """
    Extrae el ID del video de YouTube para el iframe.
    Soporta formatos: youtube.com/watch?v=ID y youtu.be/ID
    """
    if not url:
        return None
        
    url = url.strip()
    
    # youtu.be/ID
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
        return video_id if len(video_id) == 11 else None
    
    # youtube.com/watch?v=ID
    elif "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
        return video_id if len(video_id) == 11 else None
    
    return None

def generate_edit_token() -> str:
    """Genera un token único y seguro para editar perfiles."""
    return secrets.token_urlsafe(32)  # 32 bytes = ~43 caracteres

def clean_phone_number(phone: str) -> Optional[str]:
    """
    Limpia un número de teléfono preservando el código de país.
    Ejemplos:
      "+54 11 5566-7788" -> "541155667788"
      "11 5566 7788" -> "1155667788"
      "+1 555-1234" -> "15551234"
    """
    if not phone:
        return None
    
    # Eliminar todo excepto dígitos y el + inicial
    cleaned = phone.strip()
    if cleaned.startswith('+'):
        cleaned = '+' + ''.join(filter(str.isdigit, cleaned[1:]))
    else:
        cleaned = ''.join(filter(str.isdigit, cleaned))
    
    # Remover el + para almacenar solo dígitos
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    
    return cleaned if cleaned else None

def generate_whatsapp_link(phone: str, message: str = "") -> str:
    """
    Genera un link de WhatsApp con el número en formato internacional.
    Asume que el número ya tiene código de país.
    Si no empieza con código conocido, asume Argentina (+54).
    """
    if not phone:
        return "#"
    
    clean_phone = "".join(filter(str.isdigit, phone))
    
    # Si no empieza con código de país común, asumir Argentina
    # Códigos comunes: 1 (USA/Canada), 54 (Argentina), 55 (Brasil), 52 (México), etc.
    if not (clean_phone.startswith('1') or 
            clean_phone.startswith('54') or 
            clean_phone.startswith('55') or
            clean_phone.startswith('52')):
        # Asumir Argentina si no tiene código
        clean_phone = "54" + clean_phone
    
    encoded_message = message.replace(" ", "%20")
    return f"https://wa.me/{clean_phone}?text={encoded_message}"

def normalize_instagram_link(username_or_url: str) -> str:
    """
    Normaliza un username o URL de Instagram a formato completo.
    """
    if not username_or_url:
        return ""
    
    username_or_url = username_or_url.strip()
    
    if username_or_url.startswith("http"):
        return username_or_url
    
    username = username_or_url.replace("@", "")
    return f"https://instagram.com/{username}"

def normalize_text_list(text: str) -> str:
    """
    Normaliza una lista de items separados por comas.
    Convierte a lowercase y elimina espacios extra.
    Ejemplo: "Bajo, Guitarra, BATERÍA" -> "bajo, guitarra, batería"
    """
    if not text:
        return ""
    
    items = [item.strip().lower() for item in text.split(',') if item.strip()]
    return ', '.join(items)

def validate_youtube_url(url: str) -> bool:
    """Valida que una URL de YouTube sea válida."""
    if not url:
        return True  # URLs vacías son válidas (opcional)
    
    return extract_youtube_id(url) is not None

def validate_url(url: str) -> bool:
    """Valida que una URL tenga formato básico correcto."""
    if not url:
        return True  # URLs vacías son válidas (opcional)
    
    url_pattern = re.compile(
        r'^https?://'  # http:// o https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # dominio
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # o IP
        r'(?::\d+)?'  # puerto opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None
