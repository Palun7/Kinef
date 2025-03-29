async function sendhoras(action, data) {
    try {
        const response = await fetch('/administracion/pagos/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({action, ...data})
        });

        const result = await response.json();
        if (response.ok) {
            Toastify({
                text: `${result.success}`,
                duration: 1000,
                gravity: 'top',
                position: 'center',
                style: {
                   background: "linear-gradient(to right,rgb(228, 10, 232),rgb(255, 191, 0))",
                   color: "rgb(0,0,0)"
                 },
                }).showToast();
                setTimeout(()=> {
                    location.reload();
                }, 1000);
        }else {
            Toastify({
                text: `${result.error}`,
                duration: 2000,
                gravity: 'top',
                position: 'center',
                style: {
                    background: "linear-gradient(to right,rgb(255, 0, 0),rgb(251, 66, 66))",
                    color: "rgb(221,221,221)",
                  },
            }).showToast();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

document.getElementById('pagos_form').addEventListener('submit', function (e){
    e.preventDefault();
    const data = {
        usuario: this.usuario.value,
        monto: this.monto.value,
        modo_pago: this.modo_pago.value,
        actividad: this.actividad.value,
        pase: this.pase.value,
        fecha: this.fecha.value
    }
    console.log(data)
    sendhoras('cargar', data);
});

async function obtenerUsuarios() {
    try {
        const response = await fetch('/administracion/pagos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action: 'obtener_usuarios' })
        });

        const usuarios = await response.json();
        const selectUsuario = document.getElementById('usuario');

        usuarios.forEach(usuario => {
            const option = document.createElement('option');
            option.value = usuario.id;
            option.textContent = `${usuario.user__username} ${usuario.dni}`;
            selectUsuario.appendChild(option);
        });
    } catch (error) {
        console.error('Error al obtener usuarios:', error);
    }
}

async function obtenerPagos() {
    try {
        const response = await fetch('/administracion/pagos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action: 'obtener_pagos' })
        });

        let pagos = await response.json(); 

        if (response.ok) {
            // Filtrar solo el pago más reciente de cada usuario
            const pagosRecientes = {};
            pagos.forEach(pago => {
                const usuario = pago.usuario__user__username;
                const fechaPago = new Date(pago.fecha.split('/').reverse().join('-'));

                if (!pagosRecientes[usuario] || fechaPago > new Date(pagosRecientes[usuario].fecha.split('/').reverse().join('-'))) {
                    pagosRecientes[usuario] = pago;
                }
            });

            let pagosFiltrados = Object.values(pagosRecientes);

            const pagosActivos = [];
            const pagosVencidos = [];

            pagosFiltrados.forEach(pago => {
                if (esPagoVencido(pago.fecha)) {
                    pagosVencidos.push(pago);
                } else {
                    pagosActivos.push(pago);
                }
            });

            // Renderizar ambos tipos de pagos
            crearDivPago(pagosActivos);
            crearDivPagoVencido(pagosVencidos);

            // 📌 Agregar el buscador dentro del async
            const buscador = document.getElementById('buscar_pago');
            buscador.addEventListener('keyup', () => {
                const busqueda = buscador.value.toLowerCase();

                let pagosFiltrados = Object.values(pagosRecientes).filter(i => 
                    i.usuario__user__username.toLowerCase().includes(busqueda) ||
                    i.monto.toString().includes(busqueda) ||
                    i.modo_pago.toLowerCase().includes(busqueda) ||
                    i.actividad.toLowerCase().includes(busqueda) ||
                    i.pase.toLowerCase().includes(busqueda) ||
                    i.fecha.toLowerCase().includes(busqueda)
                );

                const pagosActivos = [];
                const pagosVencidos = [];

                pagosFiltrados.forEach(pago => {
                    if (esPagoVencido(pago.fecha)) {
                        pagosVencidos.push(pago);
                    } else {
                        pagosActivos.push(pago);
                    }
                });

                crearDivPago(pagosActivos);
                crearDivPagoVencido(pagosVencidos);
            });

        } else {
            console.error('Error al obtener pagos:', pagos.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', obtenerUsuarios);

const ver_pagos = document.getElementById('ver_pagos');

document.addEventListener('DOMContentLoaded', obtenerPagos);

const cargar_pagos = document.getElementById('cargar_pagos');

cargar_pagos.addEventListener('click', () => {
    const form_pagos = document.getElementById('pagos_form');
    if(form_pagos.classList.contains('height-260')){
        form_pagos.classList.remove('height-260');
    }else {
        form_pagos.classList.add('height-260');
    }
})

function crearDivPago(dato){
    const div_contenedor = document.getElementById('pagos_cargados-activos');
    div_contenedor.innerHTML = '';

    dato.forEach(pago => {
        let div = document.createElement('div');
        div.classList.add('activo');
        div.classList.add('gasto');
        div.innerHTML=`
            <h3><strong>Usuario:</strong> ${pago.usuario__user__username}</h3>
            <p><strong>Monto abonado:</strong> $${pago.monto}</p>
            <p><strong>Modo de pago:</strong> ${pago.modo_pago}</p>
            <p><strong>Actividad:</strong> ${pago.actividad}</p>
            <p><strong>Pase:</strong> ${pago.pase}</p>
            <p><strong>Fecha:</strong> ${pago.fecha}</p>
            <p>Estado: <strong>Activo</strong></p>
        `;
        div_contenedor.appendChild(div);
    });
}

function crearDivPagoVencido(dato){
    const div_contenedor = document.getElementById('pagos_cargados');
    div_contenedor.innerHTML = '';

    dato.forEach(pago => {
        let div = document.createElement('div');
        div.classList.add('vencido');
        div.classList.add('gasto');
        div.innerHTML=`
            <h3><strong>Usuario:</strong> ${pago.usuario__user__username}</h3>
            <p><strong>Monto abonado:</strong> $${pago.monto}</p>
            <p><strong>Modo de pago:</strong> ${pago.modo_pago}</p>
            <p><strong>Actividad:</strong> ${pago.actividad}</p>
            <p><strong>Pase:</strong> ${pago.pase}</p>
            <p><strong>Fecha:</strong> ${pago.fecha}</p>
            <p>Estado: <strong>Vencido</strong></p>
        `;
        div_contenedor.appendChild(div);
    });
}

function mostrarPagos(pagos) {
    const pagosVencidos = pagos.filter(pago => esPagoVencido(pago.fecha));
    const pagosActivos = pagos.filter(pago => !esPagoVencido(pago.fecha));

    crearDivPago(pagosActivos);
    crearDivPagoVencido(pagosVencidos);
}

function esPagoVencido(fechaPago) {
    const [dia, mes, anio] = fechaPago.split('/').map(num => parseInt(num, 10));
    const fechaPagoDate = new Date(anio, mes - 1, dia);
    const fechaActual = new Date();

    const diferenciaTiempo = fechaActual - fechaPagoDate;
    const diferenciaDias = diferenciaTiempo / (1000 * 60 * 60 * 24);

    return diferenciaDias >= 30;
}

function filtrarUltimoPago(pagos) {
    const pagosPorUsuario = {};

    pagos.forEach(pago => {
        const username = pago.usuario__user__username;

        if (!pagosPorUsuario[username] || new Date(pago.fecha) > new Date(pagosPorUsuario[username].fecha)) {
            pagosPorUsuario[username] = pago;
        }
    });

    return Object.values(pagosPorUsuario);
}