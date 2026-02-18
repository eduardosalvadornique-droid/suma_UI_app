from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.apps import ToolUI
 
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
    Abre la interfaz visual para sumar dos números.
    """,
    ui=ToolUI(resource_uri="ui://sum/index.html"),
)
def abrir_sumadora() -> dict:
    return {}
 
@mcp.tool(
    ui=ToolUI(
        resource_uri="ui://sum/index.html",
        visibility=["app"],
    )
)
def suma(a: float, b: float) -> dict:
    return {"resultado": a + b}
 
 
if __name__ == "__main__":
    mcp.run()
