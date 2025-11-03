# Calculadora MCP Server - Ejemplos de Uso y Configuración

Este archivo contiene ejemplos prácticos de cómo usar el servidor MCP de calculadora, configuraciones de ejemplo y casos de uso reales.

## 1. Ejemplos de Solicitudes MCP

### 1.1 Solicitud de Inicialización

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "client_name": "MiClienteMCP",
    "client_version": "1.0.0"
  }
}
```

**Respuesta esperada:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {
        "suma": {...},
        "resta": {...},
        "multiplicacion": {...},
        "division": {...}
      }
    },
    "serverInfo": {
      "name": "Calculadora MCP Server",
      "version": "1.0.0",
      "description": "Servidor MCP para operaciones matemáticas básicas"
    }
  }
}
```

### 1.2 Solicitud de Lista de Herramientas

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Respuesta esperada:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "suma",
        "description": "Suma dos números",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {"type": "number", "description": "Primer número"},
            "b": {"type": "number", "description": "Segundo número"}
          },
          "required": ["a", "b"],
          "additionalProperties": false
        }
      }
      // ... otras herramientas
    ]
  }
}
```

### 1.3 Operaciones Matemáticas

#### Suma de números enteros
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "suma",
    "arguments": {
      "a": 15,
      "b": 27
    }
  }
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"success\": true, \"operacion\": \"suma\", \"operandos\": [15, 27], \"resultado\": 42, \"descripcion\": \"15 + 27 = 42\"}"
      }
    ],
    "isError": false
  }
}
```

#### División con números decimales
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "division",
    "arguments": {
      "a": 22.5,
      "b": 3.0
    }
  }
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"success\": true, \"operacion\": \"division\", \"operandos\": [22.5, 3.0], \"resultado\": 7.5, \"descripcion\": \"22.5 ÷ 3.0 = 7.5\"}"
      }
    ],
    "isError": false
  }
}
```

#### Manejo de error - División por cero
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "division",
    "arguments": {
      "a": 10,
      "b": 0
    }
  }
}
```

**Respuesta de error:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"success\": false, \"operacion\": \"division\", \"error\": \"No se puede dividir por cero\", \"error_type\": \"calculation_error\"}"
      }
    ],
    "isError": true
  }
}
```

### 1.4 Solicitud de Ping

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "ping"
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "message": "Pong - Calculadora MCP Server funcionando correctamente"
  }
}
```

## 2. Ejemplos de Archivos de Pruebas

### 2.1 Archivo JSON para pruebas automáticas (`test_requests.json`)

```json
[
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "client_name": "Tester",
      "client_version": "1.0.0"
    }
  },
  {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
  },
  {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "suma",
      "arguments": {
        "a": 5,
        "b": 3
      }
    }
  },
  {
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "division",
      "arguments": {
        "a": 10,
        "b": 2
      }
    }
  },
  {
    "jsonrpc": "2.0",
    "id": 5,
    "method": "ping"
  }
]
```

### 2.2 Script de prueba automatizada (`test_client.py`)

```python
#!/usr/bin/env python3
"""
Cliente de prueba para el servidor MCP de calculadora.
Ejecuta una serie de solicitudes predefinidas y valida las respuestas.
"""

import json
import subprocess
import sys
import time

class MCPTestClient:
    def __init__(self, server_path="calculadora_mcp_server.py"):
        self.server_path = server_path
        self.process = None
        self.test_results = []
    
    def start_server(self):
        """Inicia el servidor MCP en un proceso separado."""
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            print(f"✅ Servidor iniciado con PID: {self.process.pid}")
            time.sleep(1)  # Esperar a que el servidor se inicialice
            return True
        except Exception as e:
            print(f"❌ Error al iniciar servidor: {e}")
            return False
    
    def send_request(self, request):
        """Envía una solicitud al servidor y recibe la respuesta."""
        try:
            request_json = json.dumps(request) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            response_line = self.process.stdout.readline()
            if response_line:
                response = json.loads(response_line.strip())
                return response
            else:
                return None
        except Exception as e:
            print(f"❌ Error al enviar solicitud: {e}")
            return None
    
    def test_sequence(self):
        """Ejecuta una secuencia de pruebas."""
        test_cases = [
            {
                "name": "Inicialización",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {"client_name": "TestClient"}
                },
                "validate": lambda r: r and "result" in r and "serverInfo" in r.get("result", {})
            },
            {
                "name": "Lista de herramientas",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list"
                },
                "validate": lambda r: r and "result" in r and "tools" in r.get("result", {})
            },
            {
                "name": "Suma de números",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "suma",
                        "arguments": {"a": 10, "b": 5}
                    }
                },
                "validate": lambda r: r and not r.get("result", {}).get("isError", False)
            },
            {
                "name": "División por cero (debe fallar)",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {
                        "name": "division",
                        "arguments": {"a": 10, "b": 0}
                    }
                },
                "validate": lambda r: r and r.get("result", {}).get("isError", False)
            }
        ]
        
        print("\n🔄 Ejecutando pruebas...")
        for i, test in enumerate(test_cases, 1):
            print(f"\n📋 Prueba {i}: {test['name']}")
            
            response = self.send_request(test["request"])
            if response:
                is_valid = test["validate"](response)
                if is_valid:
                    print("   ✅ PASADA")
                    self.test_results.append(True)
                else:
                    print("   ❌ FALLIDA")
                    print(f"   📝 Respuesta: {json.dumps(response, indent=2)}")
                    self.test_results.append(False)
            else:
                print("   ❌ No se recibió respuesta")
                self.test_results.append(False)
    
    def stop_server(self):
        """Detiene el servidor."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("\n🛑 Servidor detenido")
    
    def run_tests(self):
        """Ejecuta la suite completa de pruebas."""
        print("🚀 Iniciando cliente de prueba MCP")
        
        if not self.start_server():
            return False
        
        try:
            self.test_sequence()
            
            # Resumen final
            passed = sum(self.test_results)
            total = len(self.test_results)
            print(f"\n📊 Resumen: {passed}/{total} pruebas pasadas")
            
            if passed == total:
                print("🎉 ¡Todas las pruebas pasaron!")
                return True
            else:
                print("⚠️  Algunas pruebas fallaron")
                return False
                
        finally:
            self.stop_server()

if __name__ == "__main__":
    client = MCPTestClient()
    success = client.run_tests()
    sys.exit(0 if success else 1)
```

### 2.3 Script batch para Windows (`run_tests.bat`)

```batch
@echo off
echo Iniciando pruebas del servidor MCP de calculadora...
echo.

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Ejecutar las pruebas
echo Ejecutando pruebas automatizadas...
python test_client.py

echo.
echo Pruebas completadas. Presiona cualquier tecla para continuar...
pause >nul
```

## 3. Configuraciones Avanzadas

### 3.1 Configuración como Servicio de Windows

Para ejecutar el servidor MCP como un servicio de Windows, se puede usar `nssm` (Non-Sucking Service Manager) o `sc`:

#### Usando nssm (recomendado)
```batch
nssm install CalculadoraMCP "C:\Python\python.exe" "C:\path\to\calculadora_mcp_server.py"
nssm set CalculadoraMCP AppDirectory "C:\path\to"
nssm set CalculadoraMCP AppStdout "C:\logs\calculadora_stdout.log"
nssm set CalculadoraMCP AppStderr "C:\logs\calculadora_stderr.log"
nssm start CalculadoraMCP
```

#### Usando sc (Windows Service Control Manager)
```batch
sc create CalculadoraMCP binPath= "C:\Python\python.exe C:\path\to\calculadora_mcp_server.py" type= own
sc start CalculadoraMCP
```

### 3.2 Configuración con Nginx (Proxy reverso)

Para usar el servidor MCP detrás de Nginx:

```nginx
server {
    listen 8080;
    server_name localhost;
    
    location /mcp/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 3.3 Configuración de Variables de Entorno

```batch
REM Configuración básica
set MCP_SERVER_PORT=8000
set MCP_LOG_LEVEL=INFO
set MCP_LOG_FILE=C:\logs\calculadora.log

REM Configuración avanzada
set MCP_MAX_CONNECTIONS=100
set MCP_TIMEOUT=30
set MCP_ENABLE_METRICS=true
```

## 4. Casos de Uso Reales

### 4.1 Integración con Claude Desktop

Para usar el servidor con Claude Desktop, añadir a `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "calculadora": {
      "command": "python",
      "args": ["C:/path/to/calculadora_mcp_server.py"],
      "env": {
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 4.2 Aplicación Web con Flask

```python
from flask import Flask, jsonify, request
import subprocess
import json
import threading

app = Flask(__name__)

def run_mcp_calculation(operation, a, b):
    """Ejecuta una operación MCP y retorna el resultado."""
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": operation,
            "arguments": {"a": a, "b": b}
        }
    }
    
    # Aquí ejecutarías el servidor MCP real
    # Por simplicidad, simulamos la respuesta
    if operation == "suma":
        return {"success": True, "resultado": a + b}
    elif operation == "division" and b == 0:
        return {"success": False, "error": "División por cero"}
    # ... más operaciones

@app.route('/calculadora/<operation>', methods=['POST'])
def calculate(operation):
    """Endpoint REST para operaciones de calculadora."""
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')
    
    if a is None or b is None:
        return jsonify({"error": "Parámetros 'a' y 'b' requeridos"}), 400
    
    result = run_mcp_calculation(operation, a, b)
    
    if result["success"]:
        return jsonify(result)
    else:
        return jsonify(result), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 4.3 Calculadora en Tiempo Real con WebSockets

```python
import asyncio
import websockets
import json

class MCPWebSocketServer:
    def __init__(self):
        self.clients = set()
    
    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"Cliente conectado: {websocket.remote_address}")
    
    async def unregister(self, websocket):
        self.clients.remove(websocket)
        print(f"Cliente desconectado: {websocket.remote_address}")
    
    async def handle_client(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                try:
                    request = json.loads(message)
                    response = await self.process_request(request)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"error": "JSON inválido"}))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def process_request(self, request):
        """Procesa una solicitud MCP y retorna respuesta."""
        # Aquí implementarías la lógica del servidor MCP
        method = request.get("method")
        if method == "ping":
            return {"jsonrpc": "2.0", "id": request["id"], "result": {"pong": True}}
        
        return {"jsonrpc": "2.0", "id": request["id"], "error": {"message": "Método no implementado"}}
    
    async def start_server(self, host="localhost", port=8765):
        print(f"🚀 Iniciando servidor WebSocket MCP en ws://{host}:{port}")
        await websockets.serve(self.handle_client, host, port)
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    server = MCPWebSocketServer()
    asyncio.run(server.start_server())
```

## 5. Optimizaciones y Mejores Prácticas

### 5.1 Performance
- Usar `asyncio` para manejar múltiples clientes concurrentemente
- Implementar pool de conexiones para bases de datos si es necesario
- Cachear resultados de operaciones comunes

### 5.2 Seguridad
- Validar todas las entradas JSON antes del procesamiento
- Limitar el tamaño de las solicitudes para prevenir ataques DoS
- Implementar autenticación y autorización según sea necesario

### 5.3 Monitoreo
- Implementar métricas de rendimiento (tiempo de respuesta, throughput)
- Logging estructurado con niveles (DEBUG, INFO, WARNING, ERROR)
- Health checks automáticos

### 5.4 Escalabilidad
- Diseñar para ser stateless cuando sea posible
- Usar load balancing para múltiples instancias
- Considerar microservicios para aplicaciones grandes

---

Este archivo complementa la documentación principal del servidor MCP de calculadora con ejemplos prácticos, configuraciones avanzadas y casos de uso reales que puedes implementar en tus propios proyectos.