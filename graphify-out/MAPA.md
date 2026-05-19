# MAPA ARQUITETURAL - KwaiDownloader [OBS-20260519-01]

## 🛠️ Stack Tecnológica
- **Backend:** FastAPI (Python 3.10+)
- **Scraper/Core:** yt-dlp (Extração de metadados e áudio)
- **Streaming/Proxy:** httpx (Chunks de vídeo sem persistência em disco)
- **Frontend:** HTML/JS Vanilla (Bootstrap/Tailwind via CDN)
- **Processamento:** FFmpeg (Conversão MP3)

## 🏗️ Visão Arquitetural
1. **Extração (`scraper.py`):** Encapsula `yt-dlp` para sanitizar URLs e extrair metadados. Usa cache para otimizar performance em requisições repetidas.
2. **Servidor (`main.py`):**
   - `/api/info`: Retorna dados do vídeo.
   - `/api/download/mp4`: Stream de vídeo via proxy `httpx`. Transparência para o cliente, baixo consumo de RAM/Disco no servidor.
   - `/api/download/mp3`: Download, conversão via post-processor do `yt-dlp` e limpeza automática de arquivos temporários.
3. **Frontend (`templates/index.html`):** SPA minimalista que consome a API e gerencia os blobs de download.

## 📁 Estrutura de Pastas (Principais)
- `main.py`: Entrypoint e rotas API.
- `scraper.py`: Core logic de extração.
- `temp/`: Pasta para processamento de áudio (MP3).
- `assets/`: Recursos estáticos (imagens/ícones).
- `templates/`: Interface web.

## 🚀 Pontos de Entrada
- **API:** `http://localhost:8000/api`
- **Web:** `http://localhost:8000/`
