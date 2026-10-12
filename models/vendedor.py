
from extensions import db


class Vendedor(db.Model):
    __tablename__ = "vendedores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)

    ventas = db.relationship(
        "Venta",
        back_populates="vendedor"
    )
