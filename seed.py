
from datetime import date
from decimal import Decimal

from app import app
from extensions import db
from models.vendedor import Vendedor
from models.venta import Venta


def insertar_datos():
    with app.app_context():

        # Evitar duplicar datos al ejecutar el script
        if db.session.query(Vendedor.id).first():
            print("Ya existen vendedores en la base de datos.")
            return

        vendedores = [
            Vendedor(
                nombre="Juan Perez",
                correo="juan@example.com"
            ),
            Vendedor(
                nombre="Maria Lopez",
                correo="maria@example.com"
            ),
            Vendedor(
                nombre="Carlos Ruiz",
                correo="carlos@example.com"
            )
        ]

        db.session.add_all(vendedores)
        db.session.flush()

        ventas = [
            Venta(
                vendedor_id=vendedores[0].id,
                monto=Decimal("1200.00"),
                fecha=date(2026, 10, 1)
            ),
            Venta(
                vendedor_id=vendedores[0].id,
                monto=Decimal("800.00"),
                fecha=date(2026, 10, 3)
            ),
            Venta(
                vendedor_id=vendedores[1].id,
                monto=Decimal("2500.00"),
                fecha=date(2026, 10, 4)
            ),
            Venta(
                vendedor_id=vendedores[1].id,
                monto=Decimal("1500.00"),
                fecha=date(2026, 10, 6)
            ),
            Venta(
                vendedor_id=vendedores[2].id,
                monto=Decimal("950.00"),
                fecha=date(2026, 10, 8)
            )
        ]

        db.session.add_all(ventas)
        db.session.commit()

        print("Datos de prueba insertados correctamente.")


if __name__ == "__main__":
    insertar_datos()
