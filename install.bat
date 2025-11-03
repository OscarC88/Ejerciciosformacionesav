@echo off
REM Script de instalación automática para Windows
REM Servidor MCP de Clima
REM Autor: MiniMax Agent

echo ========================================
echo  Servidor MCP de Clima - Instalador
echo ========================================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado.
    echo Por favor instala Python 3.10+ desde https://python.org
    echo Durante la instalación, marca "Add Python to PATH"
    pause
    exit /b 1
)
echo Python detectado correctamente.
echo.

REM Crear entorno virtual
echo [2/6] Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo Entorno virtual creado.
echo.

REM Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo Entorno virtual activado.
echo.

REM Actualizar pip
echo [4/6] Actualizando pip...
python -m pip install --upgrade pip
echo Pip actualizado.
echo.

REM Instalar dependencias
echo [5/6] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo Dependencias instaladas correctamente.
echo.

REM Verificar instalación
echo [6/6] Verificando instalación...
python -c "import mcp; import httpx; import pydantic; print('Instalación verificada correctamente')"
if %errorlevel% neq 0 (
    echo ERROR: Verificación de instalación falló
    pause
    exit /b 1
)

REM Crear archivo .env si no existe
if not exist .env (
    echo OPENWEATHERMAP_API_KEY=tu_api_key_aqui > .env
    echo Archivo .env creado. Por favor edítalo y agrega tu API key.
)

echo.
echo ========================================
echo  Instalación completada exitosamente!
echo ========================================
echo.
echo Próximos pasos:
echo 1. Obtén tu API key gratuita en: https://openweathermap.org/api
echo 2. Edita el archivo .env y agrega tu API key
echo 3. Ejecuta: venv\Scripts\activate
echo 4. Ejecuta: python clima_mcp_server.py
echo.
echo Para más información, consulta: docs/ejemplo_clima_instructions.md
echo.
pause
