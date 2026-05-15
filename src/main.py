from mcp.server.fastmcp import FastMCP

# Crear el servidor
mcp = FastMCP("Mi servidor jira")

@mcp.tool()
def crear_usuario(nombre: str, telefono: str, dni: str, domicilio: str):
    """Crea un usuario con sus datos completos: nombre, teléfono, DNI y domicilio."""
    return {
        "mensaje": f"Usuario {nombre} creado exitosamente",
        "datos": {
            "nombre": nombre,
            "telefono": telefono,
            "dni": dni,
            "domicilio": domicilio,
        },
    }

# Exponer como app ASGI para vErcel
app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run()