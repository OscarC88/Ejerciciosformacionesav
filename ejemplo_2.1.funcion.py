import pytest 
def calcular_descuento_final(precio_base: float, tipo_cliente: str) -> float:
 """ 
 Calcula el precio final aplicando un descuento según el tipo de cliente.
 - Clientes 'VIP' tienen un 20% de descuento.
 - Clientes 'REGULAR' tienen un 10% de descuento si la compra supera los 100.
 - Lanza un ValueError si el precio es negativo.
 """ 
 if precio_base < 0:
    raise ValueError("El precio base no puede ser negativo.")
descuento = 0.0
if tipo_cliente == 'VIP':
    descuento = 0.20 
elif tipo_cliente == 'REGULAR' and precio_base > 100:
    descuento = 0.10
precio_final = precio_base * (1 - descuento)
return round(precio_final, 2)
