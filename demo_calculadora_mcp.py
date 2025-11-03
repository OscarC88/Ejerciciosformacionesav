#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Demostración - Servidor MCP Calculadora
=================================================

Este script demuestra cómo probar el servidor MCP de calculadora
usando solicitudes de ejemplo.

Autor: MiniMax Agent
Versión: 1.0.0
Fecha: 2025-11-04
"""

import json
import subprocess
import sys
import time
import os

def print_banner():
    """Muestra el banner de la demostración."""
    print("=" * 60)
    print("🔢 SERVIDOR MCP CALCULADORA - DEMOSTRACIÓN")
    print("=" * 60)
    print("Este script demuestra el funcionamiento del servidor MCP")
    print("enviando solicitudes de ejemplo y mostrando las respuestas.")
    print()

def print_separator(title=""):
    """Imprime un separador visual."""
    print("-" * 60)
    if title:
        print(f"📋 {title}")
        print("-" * 60)

def demonstrate_mcp_server():
    """Ejecuta una demostración completa del servidor MCP."""
    
    # Verificar que el servidor existe
    server_path = "calculadora_mcp_server.py"
    if not os.path.exists(server_path):
        print(f"❌ ERROR: No se encuentra el archivo {server_path}")
        print("   Asegúrate de ejecutar este script desde el directorio correcto.")
        return False
    
    print("🚀 Iniciando demostración del servidor MCP...")
    print()
    
    try:
        # Iniciar el servidor como proceso
        print("🔄 Iniciando servidor MCP...")
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Esperar un momento para que el servidor se inicie
        time.sleep(1)
        
        if process.poll() is not None:
            stderr_output = process.stderr.read()
            print(f"❌ Error al iniciar servidor:")
            print(stderr_output)
            return False
        
        print("✅ Servidor iniciado exitosamente")
        print()
        
        # Definir casos de prueba
        test_cases = [
            {
                "title": "1. Inicialización del Servidor",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "client_name": "DemoClient",
                        "client_version": "1.0.0"
                    }
                }
            },
            {
                "title": "2. Lista de Herramientas Disponibles",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list"
                }
            },
            {
                "title": "3. Suma: 25 + 17",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "suma",
                        "arguments": {
                            "a": 25,
                            "b": 17
                        }
                    }
                }
            },
            {
                "title": "4. Resta: 100 - 35",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {
                        "name": "resta",
                        "arguments": {
                            "a": 100,
                            "b": 35
                        }
                    }
                }
            },
            {
                "title": "5. Multiplicación: 12 × 8",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "multiplicacion",
                        "arguments": {
                            "a": 12,
                            "b": 8
                        }
                    }
                }
            },
            {
                "title": "6. División: 144 ÷ 12",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "tools/call",
                    "params": {
                        "name": "division",
                        "arguments": {
                            "a": 144,
                            "b": 12
                        }
                    }
                }
            },
            {
                "title": "7. División por Cero (Error Controlado)",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 7,
                    "method": "tools/call",
                    "params": {
                        "name": "division",
                        "arguments": {
                            "a": 10,
                            "b": 0
                        }
                    }
                }
            },
            {
                "title": "8. Verificación de Conectividad (Ping)",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 8,
                    "method": "ping"
                }
            }
        ]
        
        # Ejecutar cada caso de prueba
        for i, test_case in enumerate(test_cases, 1):
            print_separator(test_case["title"])
            
            try:
                # Enviar solicitud
                request_json = json.dumps(test_case["request"]) + "\n"
                process.stdin.write(request_json)
                process.stdin.flush()
                
                # Recibir respuesta
                response_line = process.stdout.readline()
                
                if response_line:
                    response = json.loads(response_line.strip())
                    
                    # Formatear y mostrar respuesta
                    print(f"📤 Solicitud enviada:")
                    print(f"   {json.dumps(test_case['request'], indent=6, ensure_ascii=False)}")
                    print()
                    print(f"📥 Respuesta recibida:")
                    print(f"   {json.dumps(response, indent=6, ensure_ascii=False)}")
                    
                    # Validar respuesta
                    if "error" in response:
                        print("   ⚠️  Respuesta de error detectada")
                    elif response.get("result", {}).get("isError"):
                        print("   ⚠️  Error en la operación detectado")
                    else:
                        print("   ✅ Operación exitosa")
                else:
                    print("   ❌ No se recibió respuesta del servidor")
                
                print()
                
                # Pausa breve entre solicitudes
                if i < len(test_cases):
                    time.sleep(0.5)
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Error al decodificar respuesta JSON: {e}")
            except Exception as e:
                print(f"   ❌ Error inesperado: {e}")
        
        print_separator("RESUMEN DE LA DEMOSTRACIÓN")
        print("🎉 ¡Demostración completada!")
        print("El servidor MCP de calculadora ha procesado todas las solicitudes.")
        print()
        print("Características demostradas:")
        print("   ✅ Inicialización y capacidades del servidor")
        print("   ✅ Descubrimiento de herramientas disponibles")
        print("   ✅ Operaciones matemáticas básicas (suma, resta, multiplicación, división)")
        print("   ✅ Manejo de errores (división por cero)")
        print("   ✅ Verificación de conectividad (ping)")
        print("   ✅ Comunicación JSON-RPC 2.0 sobre stdio")
        print()
        print("Para más información, consulta:")
        print("   📖 docs/ejemplo_calculadora_instructions.md")
        print("   📄 code/ejemplos_mcp/ejemplos_configuracion.md")
        print()
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Demostración interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"❌ Error durante la demostración: {e}")
        return False
    finally:
        # Cerrar el servidor
        if 'process' in locals() and process.poll() is None:
            print("🛑 Cerrando servidor MCP...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Servidor cerrado correctamente")
            except subprocess.TimeoutExpired:
                print("⚠️  Forzando cierre del servidor...")
                process.kill()
                process.wait()

def main():
    """Función principal."""
    print_banner()
    
    # Mostrar información del entorno
    print("🔧 Información del entorno:")
    print(f"   Python: {sys.version}")
    print(f"   Directorio actual: {os.getcwd()}")
    print()
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help", "help"]:
            print("📖 Uso del script de demostración:")
            print("   python demo_calculadora_mcp.py")
            print()
            print("Este script ejecuta una demostración completa del servidor MCP de calculadora,")
            print("enviando solicitudes de ejemplo y mostrando las respuestas.")
            return
        elif sys.argv[1] in ["-v", "--verbose"]:
            print("🔊 Modo verbose activado")
            print()
    
    # Ejecutar demostración
    success = demonstrate_mcp_server()
    
    if success:
        print("✨ Demostración finalizada exitosamente")
        sys.exit(0)
    else:
        print("💥 La demostración falló")
        sys.exit(1)

if __name__ == "__main__":
    main()