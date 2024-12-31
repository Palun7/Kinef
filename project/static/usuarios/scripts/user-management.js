async function sendUserData(action, data) {
    try {
        const response = await fetch('/usuarios/user-management/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action, ...data })
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.success);
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

// Registro
document.getElementById('register-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const password = this.password.value;
    const password2 = this.password2.value;

    if (password !== password2) {
        alert('Las contraseñas no coinciden');
        return;
    }

    const data = {
        username: this.username.value,
        password: this.password.value,
        dni: this.dni.value,
        fecha_nacimiento: this.fecha_nacimiento.value,
        telefono: this.telefono.value,
        domicilio: this.domicilio.value,
        instagram: this.instagram.value
    };
    sendUserData('register', data);
});

// Inicio de sesión
document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const data = {
        username: this.username.value,
        password: this.password.value
    };
    sendUserData('login', data);
});

let password_tecla = document.getElementById('password');
let password2_tecla = document.getElementById('password2');

password_tecla.addEventListener('blur', ()=>{
    let password = document.getElementById('password').value;
    let div_errores = document.getElementById('errores_password');

    div_errores.innerHTML = '';

    if(password.length <= 6){
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