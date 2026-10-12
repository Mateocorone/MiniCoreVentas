
const formulario = document.getElementById("form-comisiones");
const tabla = document.getElementById("tabla-resultados");
const mensaje = document.getElementById("mensaje");
const totalElemento = document.getElementById("total-comisiones");
const boton = document.getElementById("btn-consultar");

const formatoMoneda = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
});

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const fechaInicio = document.getElementById("fecha-inicio").value;
    const fechaFin = document.getElementById("fecha-fin").value;

    if (fechaInicio > fechaFin) {
        mensaje.textContent = "La fecha inicial no puede superar la final.";
        return;
    }

    boton.disabled = true;
    mensaje.textContent = "Consultando comisiones...";
    tabla.replaceChildren();
    totalElemento.textContent = formatoMoneda.format(0);

    try {
        const parametros = new URLSearchParams({
            fecha_inicio: fechaInicio,
            fecha_fin: fechaFin
        });

        const respuesta = await fetch(`/api/comisiones?${parametros}`);
        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.error || "Error al consultar.");
        }

        let totalComisiones = 0;

        for (const resultado of datos.resultados) {
            const fila = document.createElement("tr");

            const valores = [
                resultado.vendedor,
                resultado.cantidad_ventas,
                formatoMoneda.format(resultado.total_ventas),
                formatoMoneda.format(resultado.comision)
            ];

            for (const valor of valores) {
                const celda = document.createElement("td");
                celda.textContent = valor;
                fila.appendChild(celda);
            }

            tabla.appendChild(fila);
            totalComisiones += resultado.comision;
        }

        totalElemento.textContent =
            formatoMoneda.format(totalComisiones);

        mensaje.textContent = datos.resultados.length
            ? `${datos.resultados.length} vendedores encontrados.`
            : "No hay ventas en este rango de fechas.";

    } catch (error) {
        mensaje.textContent = error.message;
    } finally {
        boton.disabled = false;
    }
});
