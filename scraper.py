import yt_dlp
import logging
import re
import unicodedata
from functools import lru_cache

# Config log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_url(text: str) -> str:
    """Extrai link do Kwai de um texto usando Regex."""
    pattern = r'(https?://[^\s]+kwai\.com/[^\s]+)'
    match = re.search(pattern, text)
    return match.group(0) if match else text

MAX_FILENAME_LENGTH = 200
CACHE_SIZE = 128

def sanitize_filename(filename: str) -> str:
    """
    Limpa nome do arquivo para garantir compatibilidade com SOs.
    Decompõe acentos, remove caracteres especiais e limita o tamanho.
    """
    if not filename:
        return "kwai_video"
        
    # Normaliza texto (NFKD decompõe caracteres como 'á' em 'a' + '´')
    normalized_text = unicodedata.normalize('NFKD', filename)
    filename = "".join([c for c in normalized_text if not unicodedata.combining(c)])
    
    # Remove caracteres especiais, mantendo letras, números, espaços, hifens e underscores
    filename = re.sub(r'[^a-zA-Z0-9\s\-_]', '', filename)
    
    # Remove espaços extras e substitui por espaço simples
    filename = " ".join(filename.split())
    
    # Limita tamanho para evitar erros de sistema de arquivos
    filename = filename[:MAX_FILENAME_LENGTH]
    
    return filename.strip() or "kwai_video"

@lru_cache(maxsize=CACHE_SIZE)
def get_kwai_info(url_input: str, download_audio_only: bool = False):
    """
    Extrai metadados do vídeo Kwai usando yt-dlp.
    """
    url = extract_url(url_input)
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if download_audio_only else 'bestvideo+bestaudio/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Kwai Video')
            
            return {
                "success": True,
                "title": title,
                "clean_title": sanitize_filename(title),
                "thumbnail": info.get('thumbnail'),
                "video_url": info.get('url'),
                "duration": info.get('duration'),
                "source": url
            }
    except Exception as e:
        logger.error(f"Erro ao extrair {url}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Teste rápido
    test_url = "https://k.kwai.com/p/qzeySRCm"
    print(get_kwai_info(test_url))
