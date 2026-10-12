
from extensions import db


class Comision(db.Model):
    __tablename__ = "comisiones"

    id = db.Column(db.Integer, primary_key=True)
    porcentaje = db.Column(db.Numeric(5, 2), nullable=False)
    monto = db.Column(db.Numeric(12, 2), nullable=False)

    venta_id = db.Column(
        db.Integer,
        db.ForeignKey("ventas.id"),
        unique=True,
        nullable=False
    )

    venta = db.relationship(
        "Venta",
        back_populates="comision"
    )
