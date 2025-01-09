async function sendhoras(action, data) {
    try {
        const response = await fetch('/administracion/gastos/',{
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

document.getElementById('gastos_form').addEventListener('submit', function (e){
    e.preventDefault();
    const data = {
        usuario: this.usuario.value,
        concepto: this.concepto.value,
        monto: this.monto.value,
        fecha_gasto: this.fecha_gasto.value
    }
    console.log(data)
    sendhoras('cargar', data);
});

async function obtenerUsuarios() {
    try {
        const response = await fetch('/administracion/gastos/', {
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
            option.textContent = usuario.user__username;
            selectUsuario.appendChild(option);
        });
    } catch (error) {
        console.error('Error al obtener usuarios:', error);
    }
}

async function obtenerGastos() {
    try {
        const response = await fetch('/administracion/gastos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action: 'obtener_gastos' })
        });

        const gastos = await response.json();

        if (response.ok) {
            const div_contenedor = document.getElementById('gastos_cargados');
            div_contenedor.innerHTML = '';

            gastos.forEach(gasto => {
                const fechaUTC = new Date(gasto.fecha_gasto);
                const fechaLocal = new Date(fechaUTC.getTime() + fechaUTC.getTimezoneOffset() * 60000);

                const diaLocal = fechaLocal.toISOString().split('T')[0];
                let div = document.createElement('div')
                div.innerHTML=`
                    <p><strong>Concepto:</strong> ${gasto.concepto}</p>
                    <p><strong>Fecha:</strong> ${gasto.fecha_gasto}</p>
                    <p><strong>Monto:</strong> ${gasto.monto}</p>
                    <p><strong>Cargado por:</strong> ${gasto.usuario__user__username}</p>
                `;
                div_contenedor.appendChild(div);
            });
        } else {
            console.error('Error al obtener gastos:', gastos.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', obtenerUsuarios);
document.addEventListener('DOMContentLoaded', obtenerGastos);