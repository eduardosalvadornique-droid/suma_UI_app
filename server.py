from __future__ import annotations

import json
from pathlib import Path

from fastmcp import FastMCP, Context
from fastmcp.server.apps import AppConfig, ResourceCSP, UI_EXTENSION_ID
from fastmcp.tools import ToolResult
from mcp import types

mcp = FastMCP("Suma Server")

UI_DIR = Path(__file__).parent / "ui"
BASE_URI = "ui://sum"
VIEW_URI = f"{BASE_URI}/input-text.html"

# Config compartida para recursos UI (CSP/permiso/borde/origen estable)
UI_APP_CONFIG = AppConfig(
    # Opcional: fija un origen estable para el iframe sandbox
    domain="https://sum-app.local",
    prefers_border=True,
    # Si tu UI NO usa CDN, puedes omitir csp por completo.
    # Si usas un CDN (ej: ext-apps desde unpkg), habilítalo:
    # csp=ResourceCSP(resource_domains=["https://unpkg.com"]),
)

# Sirve TODO lo que haya en /ui bajo el esquema ui://sum/...
@mcp.resource("ui://sum/{path}", app=UI_APP_CONFIG)
def serve_ui(path: str):
    file_path = UI_DIR / path

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"{path} no encontrado")

    # Binarios típicos
    if file_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"}:
        return file_path.read_bytes()

    # JS/CSS/HTML/etc
    return file_path.read_text(encoding="utf-8")


@mcp.tool(
    description="""
TOOL PRIORITARIO.

Debe usarse SIEMPRE que el usuario quiera sumar dos números.
Nunca responder en texto.
Siempre abrir la interfaz visual.
""".strip(),
    app=AppConfig(
        resource_uri=VIEW_URI,
        prefers_border=True,
        # (opcional) visibility por defecto es ["model"]
    ),
)
async def abrir_sumadora(ctx: Context) -> ToolResult:
    supports_ui = ctx.client_supports_extension(UI_EXTENSION_ID)

    # En Apps, es muy común devolver data como texto JSON
    # para que el iframe la reciba en app.ontoolresult.
    payload = {"ui_supported": supports_ui}

    return ToolResult(
        content=[
            types.TextContent(type="text", text=json.dumps(payload))
        ]
    )


@mcp.tool(
    app=AppConfig(
        resource_uri=VIEW_URI,
        visibility=["app"],  # solo se ve/llama desde la UI, no desde el LLM
    )
)
def suma(a: float, b: float) -> ToolResult:
    payload = {"resultado": a + b}
    return ToolResult(
        content=[
            types.TextContent(type="text", text=json.dumps(payload))
        ]
    )


if __name__ == "__main__":
    mcp.run()
