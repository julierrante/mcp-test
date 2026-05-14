from mcp.server.fastmcp import FastMCP

# Crear el servidor
mcp = FastMCP("Mi servidor jira")

@mcp.tool()
def crear_usuario(nombre: str):
    return f"Usuario {nombre} creado exitosamente"

# Exponer como app ASGI para vErcel
app = mcp.get_asgi_app()

if __name__ == "__main__":
    mcp.run()