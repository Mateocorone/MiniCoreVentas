"""Controlador para calcular las comisiones de vendedores."""
from datetime import datetime
from decimal import Decimal

from flask import Blueprint, jsonify, request
from sqlalchemy import func, select

from extensions import db
from models.vendedor import Vendedor
from models.venta import Venta

comision_bp = Blueprint("comisiones", __name__)


@comision_bp.route("/api/comisiones", methods=["GET"])
def calcular_comisiones():

    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    if not fecha_inicio or not fecha_fin:
        return jsonify({
            "error": "Debe indicar fecha_inicio y fecha_fin"
        }), 400

    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "error": "El formato de las fechas debe ser YYYY-MM-DD"
        }), 400

    if inicio > fin:
        return jsonify({
            "error": "La fecha inicial no puede ser posterior a la final"
        }), 400

    # Comisión fija del 10% para nuestro ejercicio
    porcentaje = Decimal("0.10")

    resultados = (
        db.session.query(
            Vendedor.id,
            Vendedor.nombre,
            func.sum(Venta.monto).label("total_ventas"),
            func.count(Venta.id).label("cantidad_ventas")  # pylint: disable=not-callable
        )
        .join(Venta, Venta.vendedor_id == Vendedor.id)
        .filter(Venta.fecha.between(inicio, fin))
        .group_by(Vendedor.id, Vendedor.nombre)
        .order_by(Vendedor.nombre)
        .all()
    )

    comisiones = []

    for resultado in resultados:
        total = Decimal(str(resultado.total_ventas))
        monto_comision = (
            total * porcentaje
        ).quantize(Decimal("0.01"))

        comisiones.append({
            "vendedor_id": resultado.id,
            "vendedor": resultado.nombre,
            "cantidad_ventas": resultado.cantidad_ventas,
            "total_ventas": float(total),
            "porcentaje_comision": 10,
            "comision": float(monto_comision)
        })

    return jsonify({
        "fecha_inicio": inicio.isoformat(),
        "fecha_fin": fin.isoformat(),
        "resultados": comisiones
    })
