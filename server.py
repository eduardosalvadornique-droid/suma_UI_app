from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.apps import ToolUI

# Crea el servidor
mcp = FastMCP("Suma Server")

# Registra la UI como recurso MCP
@mcp.resource("ui://sum/view.html")
def suma_ui() -> str:
    return Path("./ui/index.html").read_text()

# Tool con UI asociada
@mcp.tool(ui=ToolUI(resource_uri="ui://sum/view.html"))
def suma(a: float, b: float) -> dict:
    return {"resultado": a + b}

if __name__ == "__main__":
    mcp.run()
