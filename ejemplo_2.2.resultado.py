# test_inventario_api.py
import unittest
from unittest.mock import patch, Mock

# Asumimos que la función está en un archivo llamado 'servicios.py'
from servicios import obtener_info_producto

class TestInventarioAPI(unittest.TestCase):

    @patch('servicios.requests.get')
    def test_obtener_info_producto_exito(self, mock_get):
        """
        Prueba que la función procesa correctamente una respuesta exitosa (200 OK).
        """
        # 1. Configuración del Mock
        producto_id_existente = "PROD-123"
        datos_producto_mock = {"id": "PROD-123", "nombre": "Teclado Mecánico", "stock": 75}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = datos_producto_mock
        mock_get.return_value = mock_response

        # 2. Ejecución de la función
        resultado = obtener_info_producto(producto_id_existente)

        # 3. Verificación (Assert)
        mock_get.assert_called_once_with(f"https://api.inventario.empresa.com/productos/{producto_id_existente}", timeout=5)
        self.assertEqual(resultado, datos_producto_mock)

    @patch('servicios.requests.get')
    def test_obtener_info_producto_no_encontrado(self, mock_get):
        """
        Prueba que la función devuelve None cuando la API responde con un 404.
        """
        # 1. Configuración del Mock
        producto_id_inexistente = "PROD-999"

        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # 2. Ejecución de la función
        resultado = obtener_info_producto(producto_id_inexistente)

        # 3. Verificación (Assert)
        mock_get.assert_called_once_with(f"https://api.inventario.empresa.com/productos/{producto_id_inexistente}", timeout=5)
        self.assertIsNone(resultado)

if __name__ == '__main__':
    unittest.main()