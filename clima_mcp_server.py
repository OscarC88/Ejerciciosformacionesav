"""
Servidor MCP (Model Context Protocol) para consultar información del clima.

Este servidor proporciona herramientas para:
- Consultar clima actual por nombre de ciudad
- Buscar ciudades disponibles
- Validar configuración de API key
- Manejo robusto de errores

Autor: MiniMax Agent
Fecha: 2025-11-04
Versión: 1.0.0
"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Dependencias externas
import httpx
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_clima_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class WeatherConfig:
    """Configuración del servidor de clima."""
    api_key: str
    base_url: str = "https://api.openweathermap.org/data/2.5"
    timeout: float = 30.0
    max_retries: int = 3


@dataclass 
class LocationData:
    """Estructura para datos de ubicación."""
    name: str
    country: str
    state: Optional[str] = None
    lat: float = 0.0
    lon: float = 0.0
    local_names: Optional[Dict[str, str]] = None


class WeatherResponse(BaseModel):
    """Modelo para respuesta de datos meteorológicos."""
    ciudad: str = Field(description="Nombre de la ciudad")
    pais: str = Field(description="Código de país ISO")
    coordenadas: Dict[str, float] = Field(description="Latitud y longitud")
    temperatura: float = Field(description="Temperatura en Celsius")
    sensacion_termica: float = Field(description="Sensación térmica en Celsius")
    humedad: int = Field(description="Humedad relativa en porcentaje")
    presion: int = Field(description="Presión atmosférica en hPa")
    visibilidad: Optional[float] = Field(default=None, description="Visibilidad en metros")
    condiciones: str = Field(description="Descripción del clima")
    viento: Dict[str, Any] = Field(description="Información del viento")
    nubes: Dict[str, Any] = Field(description="Información de nubes")
    amanecer: str = Field(description="Hora del amanecer")
    atardecer: str = Field(description="Hora del atardecer")
    timezone: int = Field(description="Zona horaria en segundos UTC")
    timestamp: str = Field(description="Timestamp de la consulta")
    unidades: str = Field(default="metric", description="Unidades de medida")


class ClimaMCPServer:
    """
    Servidor MCP para consulta de información meteorológica.
    
    Proporciona herramientas para consultar clima actual, buscar ubicaciones
    y validar configuración, con manejo robusto de errores y logging detallado.
    """
    
    def __init__(self, config: WeatherConfig):
        """
        Inicializar el servidor de clima.
        
        Args:
            config: Configuración del servidor con API key y parámetros
        """
        self.config = config
        self.client = httpx.AsyncClient(timeout=config.timeout)
        self.server = FastMCP(
            "clima-servidor", 
            description="Servidor MCP para consulta de información meteorológica",
            version="1.0.0"
        )
        
        # Registrar herramientas MCP
        self._register_tools()
        
        logger.info("Servidor MCP de clima inicializado correctamente")
    
    def _register_tools(self):
        """Registrar todas las herramientas MCP disponibles."""
        
        @self.server.tool(
            name="consultar_clima_actual",
            description="Consulta el clima actual para una ciudad específica usando OpenWeatherMap API",
            parameters={
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad (ej: 'Madrid', 'New York', 'Paris')",
                        "minLength": 1
                    },
                    "codigo_pais": {
                        "type": "string", 
                        "description": "Código de país ISO de 2 letras (ej: 'ES', 'US', 'FR'). Opcional, mejora la precisión",
                        "pattern": "^[A-Z]{2}$"
                    },
                    "unidades": {
                        "type": "string",
                        "description": "Unidades de medida: 'metric' (Celsius), 'imperial' (Fahrenheit), 'standard' (Kelvin)",
                        "enum": ["metric", "imperial", "standard"],
                        "default": "metric"
                    },
                    "idioma": {
                        "type": "string",
                        "description": "Código de idioma para la respuesta (ej: 'es', 'en', 'fr')",
                        "default": "es"
                    }
                },
                "required": ["ciudad"],
                "additionalProperties": False
            }
        )
        async def consultar_clima_actual(
            ctx: Context,
            ciudad: str,
            codigo_pais: Optional[str] = None,
            unidades: str = "metric",
            idioma: str = "es"
        ) -> str:
            """
            Consulta el clima actual para una ciudad específica.
            
            Args:
                ctx: Contexto MCP para logging y manejo de progreso
                ciudad: Nombre de la ciudad a consultar
                codigo_pais: Código de país ISO de 2 letras (opcional)
                unidades: Unidades de medida ('metric', 'imperial', 'standard')
                idioma: Código de idioma para la respuesta
                
            Returns:
                JSON string con datos meteorológicos o mensaje de error
            """
            try:
                await ctx.info(f"Consultando clima para: {ciudad}")
                await ctx.report_progress(0, 100, "Validando parámetros...")
                
                # Validar parámetros
                if not ciudad or not ciudad.strip():
                    return json.dumps({
                        "error": "Nombre de ciudad requerido",
                        "codigo_error": "PARAMETRO_INVALIDO"
                    })
                
                ciudad = ciudad.strip()
                
                # Validar API key
                if not self.config.api_key or len(self.config.api_key) < 10:
                    await ctx.error("API key no configurada o inválida")
                    return json.dumps({
                        "error": "API key no configurada o inválida",
                        "codigo_error": "API_KEY_INVALIDA"
                    })
                
                await ctx.report_progress(25, 100, "Buscando ubicación...")
                
                # Buscar coordenadas de la ciudad
                coordenadas = await self._obtener_coordenadas(ciudad, codigo_pais, ctx)
                if not coordenadas:
                    await ctx.error(f"Ciudad '{ciudad}' no encontrada")
                    return json.dumps({
                        "error": f"Ciudad '{ciudad}' no encontrada. Verifica el nombre e intenta con código de país.",
                        "codigo_error": "CIUDAD_NO_ENCONTRADA"
                    })
                
                await ctx.report_progress(50, 100, "Consultando datos meteorológicos...")
                
                # Obtener datos del clima
                weather_data = await self._obtener_datos_clima(coordenadas, unidades, idioma, ctx)
                if not weather_data:
                    await ctx.error("Error al obtener datos meteorológicos")
                    return json.dumps({
                        "error": "No se pudieron obtener datos meteorológicos",
                        "codigo_error": "ERROR_API_CLIMA"
                    })
                
                await ctx.report_progress(100, 100, "Consulta completada")
                
                return weather_data
                
            except httpx.TimeoutException:
                await ctx.error("Timeout en la consulta de API")
                logger.warning(f"Timeout consultando clima para {ciudad}")
                return json.dumps({
                    "error": "Timeout: la API tardó demasiado en responder",
                    "codigo_error": "TIMEOUT"
                })
                
            except httpx.HTTPStatusError as e:
                await ctx.error(f"Error HTTP {e.response.status_code} en API")
                logger.error(f"Error HTTP {e.response.status_code}: {e.response.text}")
                
                if e.response.status_code == 401:
                    return json.dumps({
                        "error": "API key inválida o sin permisos",
                        "codigo_error": "API_KEY_INVALIDA"
                    })
                elif e.response.status_code == 404:
                    return json.dumps({
                        "error": "Ubicación no encontrada en la API",
                        "codigo_error": "CIUDAD_NO_ENCONTRADA"
                    })
                elif e.response.status_code == 429:
                    return json.dumps({
                        "error": "Límite de solicitudes API excedido",
                        "codigo_error": "RATE_LIMIT"
                    })
                else:
                    return json.dumps({
                        "error": f"Error del servidor API (HTTP {e.response.status_code})",
                        "codigo_error": "ERROR_API"
                    })
                    
            except Exception as e:
                await ctx.error(f"Error inesperado: {str(e)}")
                logger.error(f"Error inesperado consultando clima: {e}", exc_info=True)
                return json.dumps({
                    "error": f"Error inesperado: {str(e)}",
                    "codigo_error": "ERROR_INTERNO"
                })
        
        @self.server.tool(
            name="buscar_ciudades",
            description="Busca ciudades que coincidan con un término de búsqueda",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Término de búsqueda para ciudades (ej: 'Madrid', 'New York', 'Tor')",
                        "minLength": 2
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Número máximo de resultados a devolver",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        )
        async def buscar_ciudades(
            ctx: Context,
            query: str,
            limit: int = 5
        ) -> str:
            """
            Busca ciudades que coincidan con un término de búsqueda.
            
            Args:
                ctx: Contexto MCP para logging
                query: Término de búsqueda
                limit: Número máximo de resultados
                
            Returns:
                JSON string con lista de ciudades encontradas
            """
            try:
                await ctx.info(f"Buscando ciudades para: {query}")
                
                # Validar API key
                if not self.config.api_key or len(self.config.api_key) < 10:
                    return json.dumps({
                        "error": "API key no configurada o inválida",
                        "codigo_error": "API_KEY_INVALIDA"
                    })
                
                url = f"http://api.openweathermap.org/geo/1.0/direct"
                params = {
                    "q": query.strip(),
                    "limit": limit,
                    "appid": self.config.api_key
                }
                
                response = await self.client.get(url, params=params)
                response.raise_for_status()
                
                ciudades_data = response.json()
                
                if not ciudades_data:
                    return json.dumps({
                        "resultados": [],
                        "mensaje": f"No se encontraron ciudades que coincidan con '{query}'",
                        "total": 0
                    })
                
                ciudades = []
                for ciudad_data in ciudades_data:
                    ciudad = {
                        "nombre": ciudad_data.get("name", ""),
                        "pais": ciudad_data.get("country", ""),
                        "estado": ciudad_data.get("state"),
                        "latitud": ciudad_data.get("lat", 0.0),
                        "longitud": ciudad_data.get("lon", 0.0)
                    }
                    ciudades.append(ciudad)
                
                return json.dumps({
                    "resultados": ciudades,
                    "total": len(ciudades),
                    "query": query,
                    "mensaje": f"Se encontraron {len(ciudades)} ciudades"
                })
                
            except Exception as e:
                await ctx.error(f"Error buscando ciudades: {str(e)}")
                logger.error(f"Error buscando ciudades: {e}", exc_info=True)
                return json.dumps({
                    "error": f"Error al buscar ciudades: {str(e)}",
                    "codigo_error": "ERROR_BUSQUEDA"
                })
        
        @self.server.tool(
            name="validar_configuracion",
            description="Valida la configuración del servidor y API key",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        async def validar_configuracion(ctx: Context) -> str:
            """
            Valida la configuración del servidor y API key.
            
            Returns:
                JSON string con estado de la configuración
            """
            try:
                await ctx.info("Validando configuración del servidor...")
                
                validacion = {
                    "api_key_configurada": bool(self.config.api_key and len(self.config.api_key) >= 10),
                    "timeout_segundos": self.config.timeout,
                    "url_base": self.config.base_url.replace("https://api.openweathermap.org", "OpenWeatherMap API"),
                    "cliente_http": "Configurado",
                    "version_servidor": "1.0.0"
                }
                
                # Probar conectividad con la API
                try:
                    test_url = f"{self.base_url}/weather"
                    test_params = {
                        "q": "London,UK",
                        "appid": self.config.api_key,
                        "units": "metric"
                    }
                    
                    response = await self.client.get(test_url, params=test_params)
                    
                    if response.status_code == 200:
                        validacion["api_funcional"] = True
                        validacion["estado_conexion"] = "Conectado"
                    elif response.status_code == 401:
                        validacion["api_funcional"] = False
                        validacion["estado_conexion"] = "API key inválida"
                    else:
                        validacion["api_funcional"] = False
                        validacion["estado_conexion"] = f"Error HTTP {response.status_code}"
                        
                except Exception as e:
                    validacion["api_funcional"] = False
                    validacion["estado_conexion"] = f"Error de conexión: {str(e)}"
                
                return json.dumps({
                    "configuracion": validacion,
                    "timestamp": datetime.now().isoformat(),
                    "estado_general": "OK" if validacion["api_funcional"] else "REQUIERE_ATENCION"
                })
                
            except Exception as e:
                await ctx.error(f"Error validando configuración: {str(e)}")
                logger.error(f"Error validando configuración: {e}", exc_info=True)
                return json.dumps({
                    "error": f"Error validando configuración: {str(e)}",
                    "codigo_error": "ERROR_VALIDACION"
                })
    
    async def _obtener_coordenadas(self, ciudad: str, codigo_pais: Optional[str], ctx: Context) -> Optional[Dict[str, float]]:
        """
        Obtiene las coordenadas de una ciudad usando la API de geocodificación.
        
        Args:
            ciudad: Nombre de la ciudad
            codigo_pais: Código de país opcional
            ctx: Contexto MCP
            
        Returns:
            Diccionario con lat y lon o None si no se encuentra
        """
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            
            # Construir query
            query = ciudad
            if codigo_pais:
                query = f"{ciudad},{codigo_pais}"
            
            params = {
                "q": query,
                "limit": 1,
                "appid": self.config.api_key
            }
            
            logger.info(f"Buscando coordenadas para: {query}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                # Intentar búsqueda más general si falla con código de país
                if codigo_pais:
                    logger.info(f"Búsqueda específica falló, intentando búsqueda general para {ciudad}")
                    params["q"] = ciudad
                    response = await self.client.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()
            
            if data:
                location = data[0]
                coordenadas = {
                    "lat": location.get("lat", 0.0),
                    "lon": location.get("lon", 0.0)
                }
                await ctx.info(f"Coordenadas encontradas: {coordenadas}")
                return coordenadas
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo coordenadas: {e}")
            return None
    
    async def _obtener_datos_clima(self, coordenadas: Dict[str, float], unidades: str, idioma: str, ctx: Context) -> Optional[str]:
        """
        Obtiene datos meteorológicos usando las coordenadas.
        
        Args:
            coordenadas: Diccionario con lat y lon
            unidades: Unidades de medida
            idioma: Código de idioma
            ctx: Contexto MCP
            
        Returns:
            JSON string con datos meteorológicos o None en caso de error
        """
        try:
            url = f"{self.config.base_url}/weather"
            params = {
                "lat": coordenadas["lat"],
                "lon": coordenadas["lon"],
                "appid": self.config.api_key,
                "units": unidades,
                "lang": idioma
            }
            
            logger.info(f"Consultando datos meteorológicos para lat={coordenadas['lat']}, lon={coordenadas['lon']}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Convertir respuesta API a nuestro modelo
            weather_data = self._procesar_respuesta_clima(data, unidades)
            
            return weather_data.model_dump_json(indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error obteniendo datos del clima: {e}")
            return None
    
    def _procesar_respuesta_clima(self, data: Dict[str, Any], unidades: str) -> WeatherResponse:
        """
        Procesa la respuesta de la API y la convierte a nuestro modelo.
        
        Args:
            data: Respuesta JSON de OpenWeatherMap
            unidades: Unidades de medida utilizadas
            
        Returns:
            Objeto WeatherResponse procesado
        """
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        sys_info = data.get("sys", {})
        wind_info = data.get("wind", {})
        clouds_info = data.get("clouds", {})
        coord_info = data.get("coord", {})
        
        # Mapear unidades de temperatura
        temp_units = {
            "metric": "°C",
            "imperial": "°F", 
            "standard": "K"
        }
        
        return WeatherResponse(
            ciudad=data.get("name", ""),
            pais=sys_info.get("country", ""),
            coordenadas={
                "latitud": coord_info.get("lat", 0.0),
                "longitud": coord_info.get("lon", 0.0)
            },
            temperatura=main.get("temp", 0.0),
            sensacion_termica=main.get("feels_like", 0.0),
            humedad=main.get("humidity", 0),
            presion=main.get("pressure", 0),
            visibilidad=data.get("visibility"),
            condiciones=weather.get("description", ""),
            viento={
                "velocidad": wind_info.get("speed", 0.0),
                "direccion": wind_info.get("deg", 0),
                "gustas": wind_info.get("gust")
            },
            nubes={
                "porcentaje": clouds_info.get("all", 0)
            },
            amanecer=datetime.fromtimestamp(sys_info.get("sunrise", 0)).strftime("%H:%M"),
            atardecer=datetime.fromtimestamp(sys_info.get("sunset", 0)).strftime("%H:%M"),
            timezone=data.get("timezone", 0),
            timestamp=datetime.now().isoformat(),
            unidades=f"{unidades} ({temp_units.get(unidades, 'N/A')})"
        )
    
    async def cleanup(self):
        """Limpiar recursos del servidor."""
        await self.client.aclose()
        logger.info("Cliente HTTP cerrado correctamente")
    
    async def run(self):
        """Ejecutar el servidor MCP."""
        try:
            logger.info("Iniciando servidor MCP...")
            await self.server.run(transport="stdio")
        except KeyboardInterrupt:
            logger.info("Servidor interrumpido por el usuario")
        except Exception as e:
            logger.error(f"Error ejecutando servidor: {e}")
        finally:
            await self.cleanup()


def load_config() -> WeatherConfig:
    """
    Carga la configuración desde variables de entorno.
    
    Returns:
        Objeto WeatherConfig con la configuración cargada
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("Variable de entorno OPENWEATHERMAP_API_KEY no encontrada")
    
    return WeatherConfig(
        api_key=api_key,
        timeout=float(os.getenv("API_TIMEOUT", "30.0")),
        max_retries=int(os.getenv("API_MAX_RETRIES", "3"))
    )


async def main():
    """Función principal para ejecutar el servidor."""
    try:
        config = load_config()
        server = ClimaMCPServer(config)
        await server.run()
    except ValueError as e:
        print(f"Error de configuración: {e}")
        print("Por favor, asegúrate de tener configurada la variable OPENWEATHERMAP_API_KEY")
        exit(1)
    except Exception as e:
        print(f"Error fatal ejecutando servidor: {e}")
        exit(1)


if __name__ == "__main__":
    # Configurar manejo de señales para shutdown graceful
    import signal
    
    async def signal_handler(signum, frame):
        print("\nRecibida señal de terminación...")
        # El cleanup se maneja en el run() del servidor
        exit(0)
    
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f))
    
    # Ejecutar servidor
    asyncio.run(main())
