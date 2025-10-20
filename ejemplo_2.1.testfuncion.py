#test_calculadora_descuentos.py
##Se asume que la función calcular_descuento_final está definida en 'logica_negocio.py'


from logica_negocio import calcular_descuento_final
import pytest

def test_descuento_cliente_vip(): 
    """Valida el 20% de descuento para clientes VIP."""
    assert calcular_descuento_final(200.0, 'VIP') == 160.00
def test_descuento_cliente_regular_compra_alta() 
    """Comprueba el 10% de descuento para clientes REGULAR con compras superiores a 100."""
    assert calcular_descuento_final(150.0, 'REGULAR') == 135.00
def test_sin_descuento_cliente_regular_compra_baja():
    """Verifica que clientes REGULAR con compra menor o igual a 100 no reciben descuento."""
    assert calcular_descuento_final(90.0, 'REGULAR') == 90.00
def test_precio_base_cero():
    """Evalúa el comportamiento cuando el precio base es cero."""
    assert calcular_descuento_final(0.0, 'VIP') == 0.0
def test_precio_negativo_lanza_excepcion():
    """Confirma que un precio negativo genera un ValueError."""
    with pytest.raises(ValueError, match="El precio base no puede ser negativo."):
         calcular_descuento_final(-50.0, 'REGULAR')
def test_tipo_cliente_invalido():
    """Verifica que un tipo de cliente no reconocido no recibe descuento."""
    assert calcular_descuento_final(100.0, 'NUEVO') == 100.00
