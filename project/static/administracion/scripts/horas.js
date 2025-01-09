async function sendhoras(action, data) {
    try {
        const response = await fetch('/administracion/horas/',{
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

document.getElementById('horas_form').addEventListener('submit', function (e){
    e.preventDefault();
    const data = {
        usuario: this.usuario.value,
        dia: this.dia.value,
        horas: this.horas.value
    }
    console.log(data)
    sendhoras('cargar', data);
});

async function obtenerUsuarios() {
    try {
        const response = await fetch('/administracion/horas/', {
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

document.addEventListener('DOMContentLoaded', obtenerUsuarios);

async function obtenerHoras() {
    try {
        const response = await fetch('/administracion/horas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action: 'obtener_horas' })
        });

        const horas = await response.json();

        if (response.ok) {
            const div_contenedor = document.getElementById('horas_cargadas');
            div_contenedor.innerHTML = '';

            horas.forEach(hora => {
                const fechaUTC = new Date(hora.dia);
                const fechaLocal = new Date(fechaUTC.getTime() + fechaUTC.getTimezoneOffset() * 60000);

                const diaLocal = fechaLocal.toISOString().split('T')[0];
                let div = document.createElement('div');
                div.classList.add('hora-cargada');
                div.innerHTML=`
                    <h3><strong>Usuario:</strong> ${hora.usuario__user__username}</h3>
                    <p><strong>Día:</strong> ${hora.dia}</p>
                    <p><strong>Horas:</strong> ${hora.horas}</p>
                `;
                div_contenedor.appendChild(div);
            });
        } else {
            console.error('Error al obtener horas:', horas.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

const mostrar_horas = document.getElementById('mostrar_horas');
mostrar_horas.addEventListener('click', ()=>{
    const div_contenedor = document.getElementById('horas_cargadas');
    if(div_contenedor.innerHTML == ''){
        obtenerHoras()
        mostrar_horas.innerHTML = 'Ocultar historial de horas';
    }else{
        div_contenedor.innerHTML = '';
        mostrar_horas.innerHTML = 'Mostrar historial de horas';
    }
});

const cargar_horas = document.getElementById('cargar_horas');

cargar_horas.addEventListener('click', () => {
    const form_horas = document.getElementById('horas_form');
    if(form_horas.classList.contains('height-200')){
        form_horas.classList.remove('height-200');
        // form_horas.classList.remove('bottom-5vh');
    }else {
        form_horas.classList.add('height-200');
        // form_horas.classList.add('bottom-5vh');
    }
})

async function sumarHoras() {
    try {
        const response = await fetch('/administracion/horas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action: 'sumar_horas' })
        });

        const horas = await response.json();

        if (response.ok) {
            const div_contenedor = document.getElementById('horas_sumadas');
            div_contenedor.innerHTML = '';

            // Obtener el mes y año actuales
            const fechaActual = new Date();
            const mesActual = fechaActual.getMonth(); // Mes actual (0-11)
            const añoActual = fechaActual.getFullYear(); // Año actual

            // Estructura para acumular las horas por usuario
            const suma_de_horas = {};

            horas.forEach(hora => {
                const fechaUTC = new Date(hora.dia);
                const fechaLocal = new Date(fechaUTC.getTime() + fechaUTC.getTimezoneOffset() * 60000);

                // Filtrar solo las fechas del mes actual
                if (fechaLocal.getMonth() === mesActual && fechaLocal.getFullYear() === añoActual) {
                    const diaLocal = fechaLocal.toISOString().split('T')[0];

                    if (!suma_de_horas[hora.usuario__user__username]) {
                        suma_de_horas[hora.usuario__user__username] = {
                            usuario: hora.usuario__user__username,
                            horas: 0, // Inicializamos las horas en 0
                            dias: []
                        };
                    }

                    // Sumamos las horas y guardamos el día
                    suma_de_horas[hora.usuario__user__username].horas += hora.horas;
                    suma_de_horas[hora.usuario__user__username].dias.push(diaLocal);
                }
            });

            // Renderizamos los datos acumulados
            Object.values(suma_de_horas).forEach(usuario => {
                const div = document.createElement('div');
                div.classList.add('hora-cargada')
                div.innerHTML = `
                    <h3><strong>Usuario:</strong> ${usuario.usuario}</h3>
                    <p><strong>Horas este mes:</strong> ${usuario.horas}</p>
                    <p><strong>Días:</strong> ${usuario.dias.join(', ')}</p>
                `;
                div_contenedor.appendChild(div);
            });
        } else {
            console.error('Error al obtener horas:', horas.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Manejo del botón para mostrar/ocultar
const horas_sumadas = document.getElementById('mostrar_horas_sumadas');
horas_sumadas.addEventListener('click', () => {
    const div_contenedor = document.getElementById('horas_sumadas');
    if (div_contenedor.innerHTML === '') {
        sumarHoras();
        horas_sumadas.innerHTML = 'Ocultar horas este mes';
    } else {
        div_contenedor.innerHTML = '';
        horas_sumadas.innerHTML = 'Ver horas este mes';
    }
});