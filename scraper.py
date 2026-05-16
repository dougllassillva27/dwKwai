import yt_dlp
import logging

# Config log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_kwai_info(url: str):
    """
    Extrai metadados do vídeo Kwai usando yt-dlp.
    Retorna dit com title, thumbnail e download_url.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo+bestaudio/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "success": True,
                "title": info.get('title', 'Kwai Video'),
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
