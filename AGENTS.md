# mcp-test

## Stack
- Python 3.13
- FastMCP (MCP server)
- Deployed on Vercel

## Structure
- `src/main.py` — MCP server principal
- `requirements.txt` — dependencias Python

## Commands
- Run server: `python src/main.py`
- Install deps: `uv pip install -r requirements.txt`

## Notes
- El servidor MCP expone tools via HTTP usando `streamable_http_app()`
- El endpoint MCP está disponible en `/mcp`

## Flujo de trabajo para bugs de Jira

Al resolver un bug del proyecto MT, seguir siempre estos pasos en orden:

1. Consultar tickets de tipo Bug en Jira (proyecto MT) con estado != Done
2. Por cada bug:
   a. Descartar todos los cambios locales y hacer checkout a main:
      - `git checkout main`
      - `git reset --hard HEAD`
      - `git clean -fd`
      - `git pull origin main`
   b. Crear branch: `fix/MT-{numero}-{descripcion-corta-en-kebab-case}`
   b. Aplicar el fix en el código
   c. Commit: `fix(MT-{numero}): descripcion del fix` (Conventional Commits)
   d. Push del branch al repositorio remoto
   e. Generar el link para crear el Pull Request hacia `main` con título y descripción pre-cargada usando el formato:
      `https://github.com/julierrante/mcp-test/compare/main...{branch}?expand=1&title={titulo-encoded}&body={descripcion-encoded}`
      Usar `expand=1` (NO `quick_pull=1`) para que el campo `body` se pre-cargue correctamente.
      La descripción debe incluir: qué bug resuelve, qué cambios se hicieron y referencia al ticket (`Closes MT-{numero}`).
   f. **Transicionar el ticket en Jira a "En revisión"** (transition id: 31)
