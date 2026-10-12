
from extensions import db
from datetime import date


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    monto = db.Column(db.Numeric(12, 2), nullable=False)

    vendedor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendedores.id"),
        nullable=False
    )

    vendedor = db.relationship(
        "Vendedor",
        back_populates="ventas"
    )

    comision = db.relationship(
        "Comision",
        back_populates="venta",
        uselist=False
    )
