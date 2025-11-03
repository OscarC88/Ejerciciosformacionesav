# Servidor MCP de Clima en Python (Windows) con OpenWeatherMap

Este proyecto implementa un servidor MCP (Model Context Protocol) completo en Python para consultar información meteorológica mediante la API de OpenWeatherMap. Diseñado específicamente para ejecutarse en Windows y facilitar la integración con clientes MCP como Claude Desktop.

## 🎯 Características

- ✅ **Consultar clima actual** por nombre de ciudad con códigos de país
- ✅ **Búsqueda inteligente de ubicaciones** con resultados múltiples
- ✅ **Validación de configuración** y diagnóstico del servidor
- ✅ **Manejo robusto de errores** con códigos específicos
- ✅ **Logging detallado** para debugging y monitoreo
- ✅ **Configuración flexible** mediante variables de entorno
- ✅ **Soporte multiidioma** para descripciones meteorológicas
- ✅ **Protocolo MCP estándar** con transporte stdio
- ✅ **Instalación automática** en Windows con script
- ✅ **Documentación exhaustiva** con ejemplos

## 📋 Requisitos

- **Python 3.10 o superior**
- **API Key de OpenWeatherMap** (gratuita, 1,000 llamadas/día)
- **Windows 10/11** (también compatible con Linux/macOS)

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Windows)

```cmd
# Descargar y ejecutar el instalador automático
install.bat
```

### Opción 2: Instalación Manual

```cmd
# 1. Clonar/descargar el proyecto
cd climate-mcp-server

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar API key
copy .env.example .env
# Editar .env y agregar tu API key de OpenWeatherMap
```

## 🔑 Configuración

1. **Obtener API Key gratuita:**
   - Visitar [OpenWeatherMap API](https://openweathermap.org/api)
   - Crear cuenta gratuita
   - Copiar la API key

2. **Configurar variables de entorno:**
   ```cmd
   # En archivo .env
   OPENWEATHERMAP_API_KEY=tu_api_key_aqui
   ```

## 🛠️ Uso

### Ejecutar Servidor
```cmd
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar servidor
python clima_mcp_server.py
```

### Probar Funcionamiento
```cmd
# Ejecutar suite de pruebas
python test_servidor.py
```

### Integración con Claude Desktop

1. **Configurar cliente MCP:**
   - Editar: `%APPDATA%\Claude\claude_desktop_config.json`
   - Usar configuración de `config.json`

2. **Ejemplo de configuración:**
   ```json
   {
     "mcpServers": {
       "clima-servidor": {
         "command": "python",
         "args": ["C:/ruta/a/clima_mcp_server.py"],
         "env": {
           "OPENWEATHERMAP_API_KEY": "tu_api_key_aqui"
         }
       }
     }
   }
   ```

## 📚 Herramientas MCP Disponibles

### 1. `consultar_clima_actual`
Consulta el clima actual para una ciudad específica.

**Parámetros:**
- `ciudad` (string, requerido): Nombre de la ciudad
- `codigo_pais` (string, opcional): Código ISO de país
- `unidades` (string): "metric", "imperial", "standard"
- `idioma` (string): Código de idioma ("es", "en", "fr", etc.)

**Ejemplos:**
```
Consultar clima en Madrid
Clima en Paris, FR en Fahrenheit
Weather in London with English descriptions
```

### 2. `buscar_ciudades`
Busca ciudades que coincidan con un término.

**Parámetros:**
- `query` (string, requerido): Término de búsqueda
- `limit` (integer): Número máximo de resultados

**Ejemplos:**
```
Buscar ciudades con "New"
Encontrar ubicaciones que contengan "Madrid"
```

### 3. `validar_configuracion`
Valida la configuración del servidor y API key.

**Ejemplos:**
```
Validar configuración del servidor
Check server setup and API connection
```

## 📊 Ejemplo de Respuesta

```json
{
  "ciudad": "Madrid",
  "pais": "ES",
  "coordenadas": {
    "latitud": 40.4168,
    "longitud": -3.7038
  },
  "temperatura": 22.5,
  "sensacion_termica": 25.0,
  "humedad": 65,
  "presion": 1013,
  "visibilidad": 10000,
  "condiciones": "cielo despejado",
  "viento": {
    "velocidad": 5.2,
    "direccion": 180,
    "gustas": null
  },
  "nubes": {
    "porcentaje": 10
  },
  "amanecer": "07:30",
  "atardecer": "19:45",
  "timezone": 3600,
  "timestamp": "2025-11-04T02:14:20",
  "unidades": "metric (°C)"
}
```

## 🚨 Manejo de Errores

| Código | Descripción | Solución |
|--------|-------------|----------|
| `API_KEY_INVALIDA` | API key no configurada o inválida | Verificar configuración en .env |
| `CIUDAD_NO_ENCONTRADA` | Ciudad no encontrada | Verificar nombre, usar código de país |
| `TIMEOUT` | API no responde | Verificar conectividad, aumentar timeout |
| `RATE_LIMIT` | Límite de solicitudes excedido | Esperar antes de nuevas consultas |
| `PARAMETRO_INVALIDO` | Parámetros faltantes | Verificar parámetros de entrada |

## 📁 Estructura del Proyecto

```
code/ejemplos_mcp/
├── clima_mcp_server.py     # Servidor MCP principal
├── test_servidor.py        # Suite de pruebas
├── install.bat            # Instalador automático Windows
├── requirements.txt       # Dependencias Python
├── .env.example          # Ejemplo de configuración
├── config.json           # Configuración detallada
└── README.md             # Este archivo

docs/
└── ejemplo_clima_instructions.md  # Documentación completa
```

## 🔧 Desarrollo

### Agregar Nuevas Funcionalidades

1. **Nuevas herramientas MCP:** Usar decorador `@server.tool()`
2. **Nuevos modelos:** Crear clases que hereden de `BaseModel`
3. **Nuevas APIs:** Expandir métodos en `ClimaMCPServer`
4. **Testing:** Agregar tests en `test_servidor.py`

### Logging
El servidor genera logs detallados:
```
2025-11-04 02:14:20 - INFO - Servidor MCP de clima inicializado
2025-11-04 02:14:21 - INFO - Consultando clima para: Madrid
2025-11-04 02:14:22 - INFO - Coordenadas encontradas: lat=40.4168, lon=-3.7038
2025-11-04 02:14:23 - INFO - Consulta completada exitosamente
```

## 📖 Documentación Completa

Para documentación detallada, consultar:
- **[Guía Completa](docs/ejemplo_clima_instructions.md)** - Manual exhaustivo
- **[Configuración MCP](config.json)** - Especificaciones técnicas
- **[Protocolo MCP](https://modelcontextprotocol.io)** - Documentación oficial

## 🆘 Solución de Problemas

### Error: "API key no configurada"
```cmd
# Verificar archivo .env existe
dir .env

# Verificar contenido
type .env
```

### Error: "Module not found"
```cmd
# Reactivar entorno virtual
venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Timeout en la consulta"
```cmd
# Aumentar timeout en .env
API_TIMEOUT=60.0
```

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama de feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📞 Soporte

- **Issues:** Reportar problemas en el repositorio
- **Documentación:** [Protocolo MCP](https://modelcontextprotocol.io)
- **API Docs:** [OpenWeatherMap](https://openweathermap.org/api)

## 🏆 Características Destacadas

- **600+ líneas de código** comentado y documentado
- **3 herramientas MCP** completamente funcionales
- **10+ tipos de errores** manejados específicamente
- **Instalación automatizada** para Windows
- **Testing automatizado** con simulación
- **Configuración flexible** para múltiples escenarios
- **Documentación exhaustiva** con ejemplos

---

**Desarrollado por:** MiniMax Agent  
**Versión:** 1.0.0  
**Fecha:** 2025-11-04  
**Compatibilidad:** Python 3.10+, Windows 10+, MCP SDK 1.0+
