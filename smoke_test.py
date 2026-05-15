"""
Smoke test del servidor MCP desplegado en Vercel.
Usa httpx para llamar directamente al endpoint /mcp via JSON-RPC.
"""

import httpx
import json

BASE_URL = "https://mcp-test-psi-eight.vercel.app/mcp"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def call_tool(client: httpx.Client, tool_name: str, arguments: dict) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    }
    response = client.post(BASE_URL, json=payload, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()


def run_smoke_tests():
    results = []

    with httpx.Client() as client:

        # Test 1: listar_paises devuelve lista no vacía
        print("▶ Test 1: listar_paises devuelve lista no vacía")
        try:
            resp = call_tool(client, "listar_paises", {})
            paises = resp.get("result", {}).get("content", [{}])[0].get("text", "[]")
            lista = json.loads(paises) if isinstance(paises, str) else paises
            assert isinstance(lista, list) and len(lista) > 0, "Lista vacía o inválida"
            print(f"  ✅ PASS — {len(lista)} países devueltos")
            results.append(("listar_paises", True, None))
        except Exception as e:
            print(f"  ❌ FAIL — {e}")
            results.append(("listar_paises", False, str(e)))

        # Test 2: crear_usuario con datos válidos
        print("▶ Test 2: crear_usuario con datos válidos")
        try:
            resp = call_tool(client, "crear_usuario", {
                "nombre": "Juan Pérez",
                "telefono": "1122334455",
                "dni": "12345678",
                "domicilio": "Av. Corrientes 1234",
                "pais": "Argentina",
                "fecha_nacimiento": "1990-05-15",
            })
            content = resp.get("result", {}).get("content", [{}])[0].get("text", "{}")
            data = json.loads(content) if isinstance(content, str) else content
            assert "mensaje" in data and "datos" in data, f"Respuesta inesperada: {data}"
            assert data["datos"]["nombre"] == "Juan Pérez"
            assert data["datos"]["es_menor_de_edad"] is False
            print(f"  ✅ PASS — Usuario creado: {data['mensaje']}")
            results.append(("crear_usuario_valido", True, None))
        except Exception as e:
            print(f"  ❌ FAIL — {e}")
            results.append(("crear_usuario_valido", False, str(e)))

        # Test 3: crear_usuario con menor de edad
        print("▶ Test 3: crear_usuario con menor de edad")
        try:
            resp = call_tool(client, "crear_usuario", {
                "nombre": "Ana García",
                "telefono": "9988776655",
                "dni": "87654321",
                "domicilio": "Calle Falsa 123",
                "pais": "Argentina",
                "fecha_nacimiento": "2015-03-10",
            })
            content = resp.get("result", {}).get("content", [{}])[0].get("text", "{}")
            data = json.loads(content) if isinstance(content, str) else content
            assert data["datos"]["es_menor_de_edad"] is True, "Debería ser menor de edad"
            print(f"  ✅ PASS — Menor de edad detectado correctamente")
            results.append(("crear_usuario_menor", True, None))
        except Exception as e:
            print(f"  ❌ FAIL — {e}")
            results.append(("crear_usuario_menor", False, str(e)))

        # Test 4: crear_usuario con país inválido
        print("▶ Test 4: crear_usuario con país inválido")
        try:
            resp = call_tool(client, "crear_usuario", {
                "nombre": "Test",
                "telefono": "000",
                "dni": "000",
                "domicilio": "Test",
                "pais": "Narnia",
                "fecha_nacimiento": "1990-01-01",
            })
            content = resp.get("result", {}).get("content", [{}])[0].get("text", "{}")
            data = json.loads(content) if isinstance(content, str) else content
            assert "error" in data, f"Debería devolver error, recibió: {data}"
            print(f"  ✅ PASS — Error devuelto correctamente: {data['error'][:60]}")
            results.append(("crear_usuario_pais_invalido", True, None))
        except Exception as e:
            print(f"  ❌ FAIL — {e}")
            results.append(("crear_usuario_pais_invalido", False, str(e)))

        # Test 5: crear_usuario con fecha en el futuro
        print("▶ Test 5: crear_usuario con fecha en el futuro")
        try:
            resp = call_tool(client, "crear_usuario", {
                "nombre": "Test",
                "telefono": "000",
                "dni": "000",
                "domicilio": "Test",
                "pais": "Argentina",
                "fecha_nacimiento": "2099-01-01",
            })
            content = resp.get("result", {}).get("content", [{}])[0].get("text", "{}")
            data = json.loads(content) if isinstance(content, str) else content
            assert "error" in data, f"Debería devolver error, recibió: {data}"
            print(f"  ✅ PASS — Error devuelto correctamente: {data['error'][:60]}")
            results.append(("crear_usuario_fecha_futura", True, None))
        except Exception as e:
            print(f"  ❌ FAIL — {e}")
            results.append(("crear_usuario_fecha_futura", False, str(e)))

    # Resumen
    print("\n" + "=" * 50)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"Resultado: {passed}/{total} tests pasaron")
    if passed == total:
        print("🟢 SMOKE TEST: PASS")
    else:
        print("🔴 SMOKE TEST: FAIL")
        for name, ok, err in results:
            if not ok:
                print(f"  - {name}: {err}")

    return passed == total


if __name__ == "__main__":
    success = run_smoke_tests()
    exit(0 if success else 1)
