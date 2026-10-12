
import os

from flask import Flask, render_template
from extensions import db


def create_app():
    """Configura e inicializa la aplicación Flask."""

    app = Flask(__name__)

    # Configuración de SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, "ventas.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + database_path.replace("\\", "/")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Registrar los modelos de la base de datos
    from models.vendedor import Vendedor
    from models.venta import Venta
    from models.comision import Comision

    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()

    # Registrar el controlador
    from controllers.comision_controller import comision_bp
    app.register_blueprint(comision_bp)

    # Ruta principal
    @app.route("/")
    def inicio():
        """Muestra la interfaz de MiniCore Ventas."""
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
