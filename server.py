from fastmcp import FastMCP
from fastmcp.server.apps import ToolUI, ResourceUI
 
mcp = FastMCP("My Server")
 
# Register a UI bundle as a resource
@mcp.resource("ui://dashboard/view.html")
def dashboard_html() -> str:
    return Path("./dist/index.html").read_text()
 
# Tool with a UI — clients render an iframe alongside the result
@mcp.tool(ui=ToolUI(resource_uri="ui://dashboard/view.html"))
async def list_users() -> list[dict]:
    return [{"id": "1", "name": "Alice"}]
 
# App-only tool — visible to the UI but hidden from the model
@mcp.tool(ui=ToolUI(
    resource_uri="ui://dashboard/view.html",
    visibility=["app"]
))
async def delete_user(id: str) -> dict:
    return {"deleted": True}
