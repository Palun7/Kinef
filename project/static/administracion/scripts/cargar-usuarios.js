async function sendUserData(action, data) {
    try {
        const response = await fetch('/administracion/cargar_usuarios/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action, ...data })
        });

        const result = await response.json();
        if (response.ok) {
            let mensaje = document.getElementById('errores_password');
            mensaje.innerHTML = result.success;
            document.getElementById('register-form').reset();
            setTimeout(() => {
                mensaje.innerHTML = '';
            }, 2000);
        } else {
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

async function sendUserDataFormData(formData) {
    try {
        const response = await fetch('/usuarios/user-management/', {
           method: 'POST',
           headers: {
               'X-CSRFToken': getCsrfToken()
           },
           body: formData
        });

        const result = await response.json();
        if (response.ok) {
            Toastify({
               text: `${result.success}`,
               duration: 2000,
               gravity: 'top',
               position: 'center',
               style: {
                   background: "linear-gradient(to right,rgb(173, 0, 176),rgb(255, 191, 0))",
                 },
            }).showToast();
            document.getElementById('register-form').reset();
            // setTimeout(() => {
            //     window.location.reload();
            // }, 2000);
        } else {
            Toastify({
               text: `${result.error}`,
               duration: 2000,
               gravity: 'top',
               position: 'center',
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

document.getElementById('register-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const password = this.password.value;
    const password2 = this.password2.value;

    if (password !== password2) {
        Toastify({
            text: `Las contraseñas deben ser iguales`,
            duration: 2000,
            gravity: 'top',
            position: 'center',
        }).showToast();
        return;
    }

    const formData = new FormData(this);
    formData.append('action', 'register');

    sendUserDataFormData(formData);
});

let password_tecla = document.getElementById('password');
let password2_tecla = document.getElementById('password2');

password_tecla.addEventListener('blur', ()=>{
    let password = document.getElementById('password').value;
    let div_errores = document.getElementById('errores_password');

    div_errores.innerHTML = '';

    if(password.length < 6){
       let h3 = document.createElement('h3');
       h3.innerHTML = 'La contraseña debe tener mas de 6 caracteres';
       div_errores.appendChild(h3);
    }
})

password2_tecla.addEventListener('blur', ()=>{
    let password = document.getElementById('password').value;
    let password2 = document.getElementById('password2').value;
    let div_errores = document.getElementById('errores_password');

    div_errores.innerHTML = '';

    if(password != password2){
       let h3 = document.createElement('h3');
       h3.innerHTML = 'Las contraseñas deben coincidir';
       div_errores.appendChild(h3);
    }
})