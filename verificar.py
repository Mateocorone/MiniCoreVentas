
from app import app
from models.vendedor import Vendedor
from models.venta import Venta


with app.app_context():
    vendedores = Vendedor.query.all()

    for vendedor in vendedores:
        print(f"\nVendedor: {vendedor.nombre}")

        for venta in vendedor.ventas:
            print(
                f"  Fecha: {venta.fecha} | "
                f"Monto: ${venta.monto}"
            )
