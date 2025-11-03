#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor MCP (Model Context Protocol) - Calculadora Básica
==========================================================

Este servidor implementa una calculadora básica siguiendo el protocolo MCP estándar.
Proporciona operaciones matemáticas fundamentales a través de herramientas (tools)
que pueden ser invocadas por clientes compatibles con MCP.

Características:
- Implementación del protocolo MCP con transporte stdio
- Herramientas para suma, resta, multiplicación y división
- Manejo robusto de errores y validación de entrada
- Documentación automática de herramientas
- Compatible con Windows

Autor: MiniMax Agent
Versión: 1.0.0
Fecha: 2025-11-04
"""

import json
import sys
import traceback
from typing import Any, Dict, List, Union
from dataclasses import dataclass


@dataclass
class MCPRequest:
    """Representa una solicitud MCP estándar."""
    jsonrpc: str
    id: Union[str, int]
    method: str
    params: Dict[str, Any] = None


@dataclass
class MCPResponse:
    """Representa una respuesta MCP estándar."""
    jsonrpc: str = "2.0"
    id: Union[str, int]
    result: Dict[str, Any] = None
    error: Dict[str, Any] = None


class CalculadoraMCP:
    """
    Servidor MCP de calculadora básica.
    
    Esta clase implementa las operaciones matemáticas fundamentales
    siguiendo el protocolo MCP estándar.
    """
    
    def __init__(self):
        """Inicializa el servidor de calculadora."""
        self.operations = {
            "suma": self.suma,
            "resta": self.resta,
            "multiplicacion": self.multiplicacion,
            "division": self.division
        }
    
    def suma(self, a: float, b: float) -> Dict[str, Any]:
        """
        Realiza la suma de dos números.
        
        Args:
            a (float): Primer número
            b (float): Segundo número
            
        Returns:
            Dict: Resultado de la operación
        """
        try:
            resultado = a + b
            return {
                "success": True,
                "operacion": "suma",
                "operandos": [a, b],
                "resultado": resultado,
                "descripcion": f"{a} + {b} = {resultado}"
            }
        except Exception as e:
            return self._error_response("suma", str(e))
    
    def resta(self, a: float, b: float) -> Dict[str, Any]:
        """
        Realiza la resta de dos números.
        
        Args:
            a (float): Primer número (minuendo)
            b (float): Segundo número (sustraendo)
            
        Returns:
            Dict: Resultado de la operación
        """
        try:
            resultado = a - b
            return {
                "success": True,
                "operacion": "resta",
                "operandos": [a, b],
                "resultado": resultado,
                "descripcion": f"{a} - {b} = {resultado}"
            }
        except Exception as e:
            return self._error_response("resta", str(e))
    
    def multiplicacion(self, a: float, b: float) -> Dict[str, Any]:
        """
        Realiza la multiplicación de dos números.
        
        Args:
            a (float): Primer número
            b (float): Segundo número
            
        Returns:
            Dict: Resultado de la operación
        """
        try:
            resultado = a * b
            return {
                "success": True,
                "operacion": "multiplicacion",
                "operandos": [a, b],
                "resultado": resultado,
                "descripcion": f"{a} × {b} = {resultado}"
            }
        except Exception as e:
            return self._error_response("multiplicacion", str(e))
    
    def division(self, a: float, b: float) -> Dict[str, Any]:
        """
        Realiza la división de dos números.
        
        Args:
            a (float): Dividendo
            b (float): Divisor
            
        Returns:
            Dict: Resultado de la operación
            
        Raises:
            ValueError: Si el divisor es cero
        """
        try:
            if b == 0:
                raise ValueError("No se puede dividir por cero")
            
            resultado = a / b
            return {
                "success": True,
                "operacion": "division",
                "operandos": [a, b],
                "resultado": resultado,
                "descripcion": f"{a} ÷ {b} = {resultado}"
            }
        except Exception as e:
            return self._error_response("division", str(e))
    
    def _error_response(self, operacion: str, mensaje_error: str) -> Dict[str, Any]:
        """
        Genera una respuesta de error estándar.
        
        Args:
            operacion (str): Nombre de la operación que falló
            mensaje_error (str): Mensaje descriptivo del error
            
        Returns:
            Dict: Respuesta de error formateada
        """
        return {
            "success": False,
            "operacion": operacion,
            "error": mensaje_error,
            "error_type": "calculation_error"
        }
    
    def validate_operands(self, a: Any, b: Any) -> Dict[str, Any]:
        """
        Valida que los operandos sean números válidos.
        
        Args:
            a: Primer operando
            b: Segundo operando
            
        Returns:
            Dict: Resultado de la validación
        """
        try:
            # Convertir a float para validar
            num_a = float(a)
            num_b = float(b)
            
            # Verificar que no sean NaN o infinito
            if not (num_a == num_a and num_b == num_b):  # Verificar NaN
                return {
                    "valid": False,
                    "error": "Los operandos no pueden ser NaN"
                }
            
            if float('inf') in [num_a, num_b] or float('-inf') in [num_a, num_b]:
                return {
                    "valid": False,
                    "error": "Los operandos no pueden ser infinito"
                }
            
            return {
                "valid": True,
                "num_a": num_a,
                "num_b": num_b
            }
            
        except (ValueError, TypeError) as e:
            return {
                "valid": False,
                "error": f"Operandos inválidos: {str(e)}"
            }


class MCPServer:
    """
    Servidor MCP que maneja la comunicación con clientes MCP.
    
    Esta clase implementa el protocolo MCP estándar, procesando
    solicitudes y devolviendo respuestas apropiadas.
    """
    
    def __init__(self):
        """Inicializa el servidor MCP."""
        self.calculadora = CalculadoraMCP()
        self.server_info = {
            "name": "Calculadora MCP Server",
            "version": "1.0.0",
            "description": "Servidor MCP para operaciones matemáticas básicas"
        }
    
    def get_server_capabilities(self) -> Dict[str, Any]:
        """
        Retorna las capacidades del servidor según el protocolo MCP.
        
        Returns:
            Dict: Capacidades del servidor
        """
        return {
            "tools": {
                "suma": {
                    "name": "suma",
                    "description": "Suma dos números",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Primer número"},
                            "b": {"type": "number", "description": "Segundo número"}
                        },
                        "required": ["a", "b"],
                        "additionalProperties": False
                    }
                },
                "resta": {
                    "name": "resta",
                    "description": "Resta dos números",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Primer número (minuendo)"},
                            "b": {"type": "number", "description": "Segundo número (sustraendo)"}
                        },
                        "required": ["a", "b"],
                        "additionalProperties": False
                    }
                },
                "multiplicacion": {
                    "name": "multiplicacion",
                    "description": "Multiplica dos números",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Primer número"},
                            "b": {"type": "number", "description": "Segundo número"}
                        },
                        "required": ["a", "b"],
                        "additionalProperties": False
                    }
                },
                "division": {
                    "name": "division",
                    "description": "Divide dos números",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Dividendo"},
                            "b": {"type": "number", "description": "Divisor (no puede ser cero)"}
                        },
                        "required": ["a", "b"],
                        "additionalProperties": False
                    }
                }
            }
        }
    
    def process_request(self, request_data: str) -> str:
        """
        Procesa una solicitud MCP y retorna la respuesta correspondiente.
        
        Args:
            request_data (str): Datos JSON de la solicitud
            
        Returns:
            str: Respuesta JSON formateada
        """
        try:
            # Parsear la solicitud
            request = json.loads(request_data)
            request_id = request.get("id", "unknown")
            method = request.get("method", "")
            params = request.get("params", {})
            
            # Manejar diferentes métodos MCP
            if method == "initialize":
                return self._handle_initialize(request_id)
            
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            
            elif method == "tools/call":
                return self._handle_tools_call(request_id, params)
            
            elif method == "ping":
                return self._handle_ping(request_id)
            
            else:
                # Método no soportado
                error_response = MCPResponse(
                    id=request_id,
                    error={
                        "code": -32601,
                        "message": f"Método no soportado: {method}",
                        "data": "Este servidor MCP solo soporta initialize, tools/list, tools/call y ping"
                    }
                )
                return json.dumps(error_response.__dict__, ensure_ascii=False)
        
        except json.JSONDecodeError:
            error_response = MCPResponse(
                id="unknown",
                error={
                    "code": -32700,
                    "message": "JSON inválido en la solicitud",
                    "data": "Los datos recibidos no son un JSON válido"
                }
            )
            return json.dumps(error_response.__dict__, ensure_ascii=False)
        
        except Exception as e:
            error_response = MCPResponse(
                id="unknown",
                error={
                    "code": -32603,
                    "message": "Error interno del servidor",
                    "data": f"Error: {str(e)}\n{traceback.format_exc()}"
                }
                )
            return json.dumps(error_response.__dict__, ensure_ascii=False)
    
    def _handle_initialize(self, request_id: Union[str, int]) -> str:
        """
        Maneja la inicialización del cliente MCP.
        
        Args:
            request_id: ID de la solicitud
            
        Returns:
            str: Respuesta de inicialización
        """
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": self.get_server_capabilities(),
                "serverInfo": self.server_info
            }
        }
        return json.dumps(response, ensure_ascii=False)
    
    def _handle_tools_list(self, request_id: Union[str, int]) -> str:
        """
        Maneja la solicitud de lista de herramientas disponibles.
        
        Args:
            request_id: ID de la solicitud
            
        Returns:
            str: Lista de herramientas en formato JSON
        """
        capabilities = self.get_server_capabilities()
        tools_list = []
        
        for tool_name, tool_config in capabilities["tools"].items():
            tools_list.append({
                "name": tool_name,
                "description": tool_config["description"],
                "inputSchema": tool_config["inputSchema"]
            })
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools_list
            }
        }
        return json.dumps(response, ensure_ascii=False)
    
    def _handle_tools_call(self, request_id: Union[str, int], params: Dict[str, Any]) -> str:
        """
        Maneja la invocación de herramientas.
        
        Args:
            request_id: ID de la solicitud
            params: Parámetros de la herramienta
            
        Returns:
            str: Resultado de la herramienta invocada
        """
        try:
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            
            # Verificar que la herramienta existe
            if tool_name not in self.calculadora.operations:
                error_response = MCPResponse(
                    id=request_id,
                    error={
                        "code": -32601,
                        "message": f"Herramienta no encontrada: {tool_name}",
                        "data": f"Las herramientas disponibles son: {list(self.calculadora.operations.keys())}"
                    }
                )
                return json.dumps(error_response.__dict__, ensure_ascii=False)
            
            # Validar argumentos
            a = arguments.get("a")
            b = arguments.get("b")
            
            validation_result = self.calculadora.validate_operands(a, b)
            if not validation_result["valid"]:
                error_response = MCPResponse(
                    id=request_id,
                    error={
                        "code": -32602,
                        "message": "Argumentos inválidos",
                        "data": validation_result["error"]
                    }
                )
                return json.dumps(error_response.__dict__, ensure_ascii=False)
            
            # Ejecutar la operación
            num_a = validation_result["num_a"]
            num_b = validation_result["num_b"]
            
            operation_func = self.calculadora.operations[tool_name]
            result = operation_func(num_a, num_b)
            
            # Formatear respuesta según estándar MCP
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ],
                    "isError": not result["success"]
                }
            }
            
            return json.dumps(response, ensure_ascii=False)
            
        except KeyError as e:
            error_response = MCPResponse(
                id=request_id,
                error={
                    "code": -32602,
                    "message": "Argumentos faltantes",
                    "data": f"Argumento requerido faltante: {str(e)}"
                }
            )
            return json.dumps(error_response.__dict__, ensure_ascii=False)
        
        except Exception as e:
            error_response = MCPResponse(
                id=request_id,
                error={
                    "code": -32603,
                    "message": "Error al ejecutar la herramienta",
                    "data": f"Error: {str(e)}\n{traceback.format_exc()}"
                }
            )
            return json.dumps(error_response.__dict__, ensure_ascii=False)
    
    def _handle_ping(self, request_id: Union[str, int]) -> str:
        """
        Maneja las solicitudes de ping para verificar conectividad.
        
        Args:
            request_id: ID de la solicitud
            
        Returns:
            str: Respuesta de ping
        """
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "message": "Pong - Calculadora MCP Server funcionando correctamente"
            }
        }
        return json.dumps(response, ensure_ascii=False)
    
    def run(self):
        """
        Ejecuta el servidor MCP procesando entrada desde stdin.
        """
        print("Iniciando Calculadora MCP Server...", file=sys.stderr)
        print("Servidor listo para recibir solicitudes...", file=sys.stderr)
        
        try:
            while True:
                # Leer línea de entrada desde stdin
                line = sys.stdin.readline()
                
                if not line:
                    # EOF detectado, terminar el servidor
                    break
                
                line = line.strip()
                if not line:
                    # Línea vacía, continuar
                    continue
                
                # Procesar la solicitud
                response = self.process_request(line)
                
                # Enviar respuesta a stdout
                print(response)
                sys.stdout.flush()
                
        except KeyboardInterrupt:
            print("\nServidor interrumpido por el usuario.", file=sys.stderr)
        except Exception as e:
            print(f"Error crítico del servidor: {e}", file=sys.stderr)
            traceback.print_exc()
        finally:
            print("Calculadora MCP Server finalizado.", file=sys.stderr)


def main():
    """
    Función principal para ejecutar el servidor MCP.
    """
    # Crear y ejecutar el servidor
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()