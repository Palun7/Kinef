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
                let div = document.createElement('div')
                div.innerHTML=`
                    <h3><strong>Usuario:</strong> ${hora.usuario__user__username}</h3>
                    <p><strong>Día:</strong> ${new Date(hora.dia).toLocaleDateString()}</p>
                    <p><strong>Horas:</strong> ${hora.horas}</p>
                `;
                div_contenedor.appendChild(div);
                // const item = document.createElement('div');
                // item.className = 'hora-item';
                // item.innerHTML = `
                //     <p><strong>Usuario:</strong> ${hora.usuario__user__username}</p>
                //     <p><strong>Día:</strong> ${new Date(hora.dia).toLocaleDateString()}</p>
                //     <p><strong>Horas:</strong> ${hora.horas}</p>
                // `;
                // contenedorHoras.appendChild(item);
            });
        } else {
            console.error('Error al obtener horas:', horas.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', obtenerUsuarios);
document.addEventListener('DOMContentLoaded', obtenerHoras);