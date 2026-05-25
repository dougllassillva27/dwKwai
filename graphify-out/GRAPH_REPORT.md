# Graph Report - kwaiDownloader  (2026-05-24)

## Corpus Check
- 3 files · ~4,211 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 34 nodes · 42 edges · 7 communities (5 shown, 2 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1fe4b79e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `get_kwai_info()` - 9 edges
2. `download_mp3()` - 8 edges
3. `download_mp4()` - 7 edges
4. `sanitize_filename()` - 7 edges
5. `extract_url()` - 6 edges
6. `cleanup_file()` - 5 edges
7. `info()` - 2 edges
8. `gerarHash()` - 2 edges
9. `processarUrl()` - 2 edges
10. `AppState` - 1 edges

## Surprising Connections (you probably didn't know these)
- `info()` --calls--> `get_kwai_info()`  [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `sanitize_filename()`  [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `extract_url()`  [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `get_kwai_info()`  [INFERRED]
  main.py → scraper.py
- `download_mp3()` --calls--> `sanitize_filename()`  [INFERRED]
  main.py → scraper.py

## Communities (7 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (7): extract_url(), get_kwai_info(), Extrai link do Kwai de um texto usando Regex., Extrai link do Kwai de um texto usando Regex., Extrai metadados do vídeo Kwai usando yt-dlp., Extrai metadados do vídeo Kwai usando yt-dlp., Extrai metadados do vídeo Kwai usando yt-dlp.

### Community 3 - "Community 3"
Cohesion: 0.5
Nodes (4): cleanup_file(), Remove arquivo temporário., Remove arquivo temporário., Remove arquivo temporário.

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (4): download_mp4(), Proxy para download do MP4 com nome personalizado., Proxy para download do MP4 com nome personalizado., Proxy para download do MP4 com nome personalizado.

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (4): download_mp3(), Gera MP3 via FFmpeg e envia., Gera MP3 via yt-dlp post-processors e envia., Gera MP3 via yt-dlp post-processors e envia.

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (4): Limpa nome do arquivo: letras, números e espaços (Opção 1)., Limpa nome do arquivo: letras, números e espaços (Opção 1)., Limpa nome do arquivo para garantir compatibilidade com SOs.     Decompõe acent, sanitize_filename()

## Knowledge Gaps
- **18 isolated node(s):** `AppState`, `Remove arquivo temporário.`, `Proxy para download do MP4 com nome personalizado.`, `Gera MP3 via yt-dlp post-processors e envia.`, `Extrai link do Kwai de um texto usando Regex.` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `download_mp3()` connect `Community 5` to `Community 0`, `Community 1`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.284) - this node is a cross-community bridge._
- **Why does `get_kwai_info()` connect `Community 0` to `Community 1`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Why does `download_mp4()` connect `Community 4` to `Community 0`, `Community 1`, `Community 6`?**
  _High betweenness centrality (0.193) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `get_kwai_info()` (e.g. with `info()` and `download_mp4()`) actually correct?**
  _`get_kwai_info()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `download_mp3()` (e.g. with `sanitize_filename()` and `extract_url()`) actually correct?**
  _`download_mp3()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `download_mp4()` (e.g. with `sanitize_filename()` and `extract_url()`) actually correct?**
  _`download_mp4()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `sanitize_filename()` (e.g. with `download_mp4()` and `download_mp3()`) actually correct?**
  _`sanitize_filename()` has 2 INFERRED edges - model-reasoned connections that need verification._