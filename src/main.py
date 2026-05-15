from datetime import date
from mcp.server.fastmcp import FastMCP

# Lista de países del mundo
PAISES = [
    "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda",
    "Arabia Saudita", "Argelia", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaiyán", "Bahamas", "Bangladés", "Barbados", "Baréin", "Bélgica",
    "Belice", "Benín", "Bielorrusia", "Bolivia", "Bosnia y Herzegovina", "Botsuana",
    "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Bután",
    "Cabo Verde", "Camboya", "Camerún", "Canadá", "Catar", "Chad",
    "Chile", "China", "Chipre", "Colombia", "Comoras", "Corea del Norte",
    "Corea del Sur", "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", "Dinamarca",
    "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos Árabes Unidos", "Eritrea",
    "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Etiopía",
    "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia",
    "Georgia", "Ghana", "Granada", "Grecia", "Guatemala", "Guinea",
    "Guinea Ecuatorial", "Guinea-Bisáu", "Guyana", "Haití", "Honduras", "Hungría",
    "India", "Indonesia", "Irak", "Irán", "Irlanda", "Islandia",
    "Islas Marshall", "Islas Salomón", "Israel", "Italia", "Jamaica", "Japón",
    "Jordania", "Kazajistán", "Kenia", "Kirguistán", "Kiribati", "Kuwait",
    "Laos", "Lesoto", "Letonia", "Líbano", "Liberia", "Libia",
    "Liechtenstein", "Lituania", "Luxemburgo", "Madagascar", "Malasia", "Malaui",
    "Maldivas", "Malí", "Malta", "Marruecos", "Mauricio", "Mauritania",
    "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montenegro",
    "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger",
    "Nigeria", "Noruega", "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán",
    "Palaos", "Panamá", "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia",
    "Portugal", "Reino Unido", "República Centroafricana", "República Checa",
    "República del Congo", "República Democrática del Congo", "República Dominicana",
    "Ruanda", "Rumanía", "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino",
    "San Vicente y las Granadinas", "Santa Lucía", "Santo Tomé y Príncipe",
    "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", "Siria",
    "Somalia", "Sri Lanka", "Suazilandia", "Sudáfrica", "Sudán", "Sudán del Sur",
    "Suecia", "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistán",
    "Timor Oriental", "Togo", "Tonga", "Trinidad y Tobago", "Túnez", "Turkmenistán",
    "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay", "Uzbekistán",
    "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue",
]

# Crear el servidor
mcp = FastMCP("Mi servidor jira")


@mcp.tool()
def listar_paises() -> list[str]:
    """Devuelve la lista de todos los países disponibles para seleccionar al crear un usuario."""
    return PAISES


@mcp.tool()
def crear_usuario(nombre: str, telefono: str, dni: str, domicilio: str, pais: str, fecha_nacimiento: str):
    """Crea un usuario con sus datos completos: nombre, teléfono, DNI, domicilio, país y fecha de nacimiento.

    - 'pais' debe ser uno de los países válidos. Usá listar_paises() para ver las opciones.
    - 'fecha_nacimiento' debe estar en formato YYYY-MM-DD.
    - Se admiten usuarios de cualquier edad, incluyendo menores de edad.
    """
    if pais not in PAISES:
        return {
            "error": f"País '{pais}' no válido. Usá listar_paises() para ver los países disponibles.",
            "paises_disponibles": PAISES,
        }

    try:
        nacimiento = date.fromisoformat(fecha_nacimiento)
    except ValueError:
        return {"error": "Formato de fecha inválido. Usá YYYY-MM-DD (ej: 2010-05-15)."}

    hoy = date.today()
    edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))

    if edad < 0 or nacimiento > hoy:
        return {"error": "La fecha de nacimiento no puede ser en el futuro."}

    es_menor = edad < 18

    return {
        "mensaje": f"Usuario {nombre} creado exitosamente",
        "datos": {
            "nombre": nombre,
            "telefono": telefono,
            "dni": dni,
            "domicilio": domicilio,
            "pais": pais,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "es_menor_de_edad": es_menor,
        },
    }


# Exponer como app ASGI para Vercel
app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run()
