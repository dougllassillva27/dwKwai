# MAPA.md - Visão Arquitetural kwaiDownloader

**Gerado em:** 2026-05-25
**Commit base:** `0e829ec`
**ID de Observação:** [OBS-20260525-01]

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
| **Quality** | Ruff, mypy, pytest | dev | Linting, type checking, testes |
| **Versionamento** | versionador.js | custom | Script JS para controle de versão |

---

## 🗂️ Estrutura de Diretórios

```
kwaiDownloader/
├── main.py                 # Entry point: FastAPI app, rotas, lifespan management
├── scraper.py              # Lógica de extração: get_kwai_info(), sanitize_filename()
├── requirements.txt        # Dependências Python (dev: ruff, mypy, pytest)
├── Dockerfile              # Containerização da aplicação
├── templates/
│   └── index.html          # Frontend: formulário + UX de download
├── assets/img/             # Static files (banner, favicon, logo .webp/.ico)
├── tests/
│   └── test_git_hooks.py   # Testes automatizados para hooks de git
├── versionamento/
│   └── versionador.js      # Script de versionamento customizado
├── docs/
│   ├── DESIGN.md           # Documentação de design
│   ├── GSD_FLOW.md         # Guia do fluxo GSD
│   ├── RTK_GUIDE.md        # Guia do proxy RTK
│   └── skills/             # JSON de skills para agentes IA
├── _contexto-ia/
│   └── Geral.md            # Contexto extenso para workflow IA
├── .githooks/              # Hooks pre-commit e commit-msg (Python + Shell)
├── .agents/rules/          # Regras específicas para agentes (antigravity-rtk)
├── graphify-out/
│   ├── GRAPH_REPORT.md     # Grafo de dependências (34 nodes, 42 edges)
│   ├── TREE.md             # Árvore de arquivos filtrada
│   ├── graph.json          # Grafo estruturado em JSON
│   ├── graph.html          # Visualização interativa do grafo
│   └── MAPA.md             # Este arquivo
├── AGENT.md / CLAUDE.md / GEMINI.md  # Diretrizes para agentes IA
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
|--------|--------------|----------|
| **Async/Await** | FastAPI + httpx + run_in_threadpool | Não-bloqueante para I/O pesado |
| **Dependency Injection** | `AppState` com lifespan | Gerenciamento seguro de recursos |
| **Proxy Pattern** | `/api/download/*` redireciona para Kwai | Controle de headers, nomes, logging |
| **Background Tasks** | `cleanup_file` via BackgroundTasks | Liberação imediata da resposta |
| **Sanitization Layer** | `sanitize_filename()` centralizado | Segurança contra path traversal |
| **Error Boundary** | Try/except com logging + HTTPException | Respostas consistentes ao cliente |
| **Git Hooks** | pre-commit + commit-msg (.githooks/) | Qualidade e padronização pré-commit |

---

## ⚠️ Risk Register (Baseado em GRAPH_REPORT.md)

| Risco | Severidade | Mitigação |
|-------|-----------|----------|
| **18 nós isolados** no grafo | Média | Documentar funções auxiliares em scraper.py |
| **7 conexões INFERRED** não validadas | Alta | Revisar chamadas entre `download_mp3()` → `sanitize_filename()` |
| **Dependência de FFmpeg system** | Alta | Validar presença em Dockerfile + fallback error message |
| **Temp files sem cleanup garantido** | Média | BackgroundTasks já implementado; monitorar falhas de disco |
| **Regex de extração frágil** | Baixa | Testes com URLs reais do Kwai + fallback para yt-dlp direto |
| **requirements.txt incompleto** | Alta | Adicionar deps de runtime (fastapi, uvicorn, yt-dlp, httpx, jinja2) |

---

## 📊 Métricas do Codebase

- **Arquivos Python**: 2 core (`main.py`, `scraper.py`) + 1 teste + 2 hooks
- **Arquivos JS**: 1 (`versionador.js`)
- **Endpoints API**: 3 (`/`, `/api/info`, `/api/download/*`)
- **God Nodes** (GRAPH_REPORT.md):
  1. `get_kwai_info()` — 9 edges
  2. `download_mp3()` — 8 edges
  3. `download_mp4()` — 7 edges
  4. `sanitize_filename()` — 7 edges
  5. `extract_url()` — 6 edges

---

## 🔄 Delta vs OBS-20260524-01

| Aspecto | Anterior (24/05) | Atual (25/05) |
|---------|-----------------|---------------|
| Commit base | `1fe4b79e` | `0e829ec` |
| Novos commits | - | 2 (auto-focus UI) |
| Estrutura | Baseline | + `_contexto-ia/`, `docs/skills/`, `.agents/rules/` |
| Tests | Ausente | `test_git_hooks.py` |
| Versionamento | Não mapeado | `versionador.js` identificado |
| Deps runtime | Listadas | **FALTANDO em requirements.txt** |

---

## 🎯 Próximos Passos Prioritários

1. **[CRÍTICO] Corrigir requirements.txt**: Adicionar fastapi, uvicorn, yt-dlp, httpx, jinja2, python-multipart
2. **Validar conexões INFERRED**: Confirmar chamadas cruzadas main.py → scraper.py
3. **Expandir testes**: Cobrir `sanitize_filename()` e `get_kwai_info()`
4. **Health check endpoint**: `/api/health` para monitorar FFmpeg e conexão
5. **Rate limiting**: Proteger endpoints contra abuso

---

*Este mapa será atualizado a cada mudança arquitetural significativa. Consulte `resumo-de-trabalho.md` para histórico de decisões.*
