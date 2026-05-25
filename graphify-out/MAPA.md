# MAPA.md - Visão Arquitetural kwaiDownloader

**Gerado em:** 2026-05-24
**Commit base:** `1fe4b79e`
**ID de Observação:** [OBS-20260524-01]

---

## 🏗️ Stack Tecnológica

| Camada | Tecnologia | Versão | Responsabilidade |
|--------|-----------|--------|-----------------|
| **Framework** | FastAPI | >=0.110.0 | API REST assíncrona |
| **Servidor** | uvicorn | >=0.31.1 | ASGI server para produção |
| **Extração** | yt-dlp | >=2024.3.10 | Download e metadados de vídeo |
| **HTTP Client** | httpx | >=0.27.1 | Pooling de conexões assíncronas |
| **Templates** | Jinja2 | >=3.1.6 | Renderização de HTML |
| **Forms** | python-multipart | >=0.0.9 | Parsing de multipart/form-data |
| **Infra** | FFmpeg | system | Conversão áudio (MP3) via post-processor |

---

## 🗂️ Estrutura de Diretórios

```
kwaiDownloader/
├── main.py                 # Entry point: FastAPI app, rotas, lifespan management
├── scraper.py              # Lógica de extração: get_kwai_info(), sanitize_filename()
├── requirements.txt        # Dependências Python
├── templates/
│   └── index.html          # Frontend: formulário + UX de download
├── assets/                 # Static files (CSS, JS, favicon)
├── temp/                   # Diretório temporário para conversão MP3
├── graphify-out/
│   ├── GRAPH_REPORT.md     # Grafo de dependências (34 nodes, 42 edges)
│   ├── TREE_RAW.txt        # Árvore de arquivos filtrada
│   └── MAPA.md             # Este arquivo
├── .git/                   # Versionamento
└── README.md               # Documentação do projeto
```

---

## 🔗 Pontos de Entrada e Fluxos Críticos

### 1. Entry Point: `main.py`
- **`lifespan()`**: Gerencia ciclo de vida do httpx.AsyncClient (pooling global)
- **`/`**: Renderiza `index.html` via Jinja2Templates
- **`/api/info` [POST]**: Extrai metadados do vídeo Kwai
- **`/api/download/mp4` [GET]**: Streaming proxy com nome personalizado
- **`/api/download/mp3` [GET]**: Conversão assíncrona via yt-dlp + FFmpeg

### 2. Módulo Core: `scraper.py`
- **`get_kwai_info(url, audio_only=False)`**:
  - Extrai URL via regex (suporta links em textos livres)
  - Consulta yt-dlp para metadados (título, thumbnail, URLs)
  - Retorna dict padronizado: `{success, title, clean_title, video_url, thumbnail, source}`
- **`sanitize_filename(filename)`**:
  - Remove caracteres inválidos para SOs (Windows/Linux/macOS)
  - Preserva acentos via NFD normalization + decomposição

### 3. Fluxo MP4 (Streaming)
```
GET /api/download/mp4?url=...&filename=...
  ↓
get_kwai_info(url) → extrai video_url
  ↓
sanitize_filename(filename) ou clean_title
  ↓
httpx.AsyncClient.stream(GET video_url)
  ↓
StreamingResponse(chunk_size=64KB) → cliente
```

### 4. Fluxo MP3 (Conversão Assíncrona)
```
GET /api/download/mp3?url=...&filename=...
  ↓
get_kwai_info(url, audio_only=True) → source URL
  ↓
yt-dlp com post-processor FFmpegExtractAudio
  ↓
Arquivo temporário em temp/{uuid}.mp3
  ↓
BackgroundTasks.add_task(cleanup_file) → remoção pós-envio
  ↓
FileResponse → cliente
```

---

## 🧩 Padrões de Arquitetura Identificados

| Padrão | Implementação | Benefício |
|--------|--------------|-----------|
| **Async/Await** | FastAPI + httpx + run_in_threadpool | Não-bloqueante para I/O pesado |
| **Dependency Injection** | `AppState` com lifespan | Gerenciamento seguro de recursos |
| **Proxy Pattern** | `/api/download/*` redireciona para Kwai | Controle de headers, nomes, logging |
| **Background Tasks** | `cleanup_file` via BackgroundTasks | Liberação imediata da resposta |
| **Sanitization Layer** | `sanitize_filename()` centralizado | Segurança contra path traversal |
| **Error Boundary** | Try/except com logging + HTTPException | Respostas consistentes ao cliente |

---

## ⚠️ Risk Register (Baseado em GRAPH_REPORT.md)

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| **18 nós isolados** no grafo | Média | Documentar funções auxiliares em scraper.py |
| **7 conexões INFERRED** não validadas | Alta | Revisar chamadas entre `download_mp3()` → `sanitize_filename()` |
| **Dependência de FFmpeg system** | Alta | Validar presença em Dockerfile + fallback error message |
| **Temp files sem cleanup garantido** | Média | BackgroundTasks já implementado; monitorar falhas de disco |
| **Regex de extração frágil** | Baixa | Testes com URLs reais do Kwai + fallback para yt-dlp direto |

---

## 📊 Métricas do Codebase

- **Arquivos Python**: 2 (`main.py`, `scraper.py`)
- **Linhas de código**: ~250 (excluindo imports/comentários)
- **Endpoints API**: 3 (`/`, `/api/info`, `/api/download/*`)
- **God Nodes** (GRAPH_REPORT.md):
  1. `get_kwai_info()` — 9 edges
  2. `download_mp3()` — 8 edges
  3. `download_mp4()` — 7 edges
  4. `sanitize_filename()` — 7 edges
  5. `extract_url()` — 6 edges

---

## 🔄 Próximos Passos Sugeridos

1. **Validar conexões INFERRED**: Confirmar se `download_mp3()` realmente chama `sanitize_filename()` e `extract_url()` no código fonte
2. **Adicionar testes unitários**: Para `sanitize_filename()` (edge cases: emojis, paths, unicode)
3. **Health check endpoint**: `/api/health` para monitorar FFmpeg e conexão com Kwai
4. **Rate limiting**: Proteger endpoints contra abuso (FastAPI + SlowAPI ou similar)
5. **Logging estruturado**: Migrar `logger.error` para JSON para agregação externa

---

*Este mapa será atualizado a cada mudança arquitetural significativa. Consulte `resumo-de-trabalho.md` para histórico de decisões.*