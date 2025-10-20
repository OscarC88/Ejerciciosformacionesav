import requests

def obtener_info_producto(producto_id: str) -> dict | None:
    """
    Consulta el microservicio de inventario para obtener los datos de un producto.
    Devuelve un diccionario con los datos si el producto existe (HTTP 200).
    Devuelve None si el producto no se encuentra (HTTP 404).
    """
    url = f"https://api.inventario.empresa.com/productos/{producto_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        # En un caso real, manejaríamos otros códigos de error
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        # Log del error en un sistema de monitoreo
        print(f"Error al conectar con la API de inventario: {e}")
        return None