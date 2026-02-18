from pathlib import Path
from fastmcp import FastMCP, Context
from fastmcp.server.apps import ToolUI, UI_EXTENSION_ID
 
mcp = FastMCP("Suma Server")
 
UI_DIR = Path(__file__).parent / "ui"
 
@mcp.resource("ui://sum/{path}")
def serve_ui(path: str):
    file_path = UI_DIR / path
 
    if not file_path.exists():
        raise FileNotFoundError(f"{path} no encontrado")
 
    if file_path.suffix in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
        return file_path.read_bytes()
 
    return file_path.read_text(encoding="utf-8")
 
@mcp.tool(
    description="""
    TOOL PRIORITARIO.
 
    Debe usarse SIEMPRE que el usuario quiera sumar dos números.
    Nunca responder en texto.
    Siempre abrir la interfaz visual.
    """,
    ui=ToolUI(resource_uri="ui://sum/input-text.html"),
)
async def abrir_sumadora(ctx: Context) -> dict:
    supports_ui = ctx.client_supports_extension(UI_EXTENSION_ID)
 
    print("Client supports UI extension:", supports_ui)
 
    return {
        "ui_supported": supports_ui
    }
 
@mcp.tool(
    ui=ToolUI(
        resource_uri="ui://sum/input-text.html",
        visibility=["app"],
    )
)
def suma(a: float, b: float) -> dict:
    return {"resultado": a + b}
 
 
if __name__ == "__main__":
    mcp.run()
 
 
