async function obtenerUsuarios() {
    try {
        const response = await fetch('/administracion/usuarios/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ action: 'obtener_usuarios' })
        });

        const usuarios = await response.json();
        const usuarios_cargados = document.getElementById('usuarios_cargados');

        const buscar_usuario = document.getElementById('buscar_usuario');

        buscar_usuario.addEventListener('keyup', ()=>{
            const div_usuarios = document.getElementById('usuarios_cargados');
            div_usuarios.innerHTML = '';
            let usuario = document.getElementById('buscar_usuario').value;
            let usuarios_buscados = usuarios.filter( i =>
                i.user__username.toLowerCase().includes(usuario.toLowerCase()) ||
                i.nombre.toLowerCase().includes(usuario.toLowerCase()) ||
                i.apellido.toLowerCase().includes(usuario.toLowerCase())
            );
            crearDivUsuario(usuarios_buscados);
        })

        crearDivUsuario(usuarios);

    } catch (error) {
        console.error('Error al obtener usuarios:', error);
    }
}

function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

document.addEventListener('DOMContentLoaded', obtenerUsuarios);

function crearDivUsuario(datos){
    datos.forEach(usuario => {
        const div = document.createElement('div');
        div.classList.add('tarjeta-usuario');

        let foto;
        if(usuario.foto != null){
            foto = `<div class="foto-usuarios-contenedor">
                        <img src="${usuario.foto}" alt="Perfil" class="foto-perfil">
                    </div>`;
        }else{
            foto = '';
        }

        let foto2;
        if(usuario.foto != null){
            foto2 = `<div class="foto-usuarios-contenedor2">
                        <img src="${usuario.foto}" alt="Perfil" class="foto-perfil">
                    </div>`;
        }else{
            foto2 = '';
        }
        if(foto){
            div.innerHTML = `
                    ${foto}
                    <h3>${usuario.user__username}</h3>
                    <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
                    <p><strong>DNI:</strong> ${usuario.dni}</p>
            `;
        }else{
            div.innerHTML = `
                    <img src="../../../static/img/kinef_logo1.png" alt="Logo de Kinef" class='circulo'>
                    <h3>${usuario.user__username}</h3>
                    <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
                    <p><strong>DNI:</strong> ${usuario.dni}</p>
            `;
        }
        div.addEventListener('click',()=>{
            if(div.classList.contains('completo')){
                if(foto){
                    div.innerHTML = `
                            ${foto}
                            <h3>${usuario.user__username}</h3>
                            <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
                            <p><strong>DNI:</strong> ${usuario.dni}</p>
                    `;
                }else{
                    div.innerHTML = `
                            <img src="../../../static/img/kinef_logo1.png" alt="Logo de Kinef" class='circulo'>
                            <h3>${usuario.user__username}</h3>
                            <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
                            <p><strong>DNI:</strong> ${usuario.dni}</p>
                    `;
                }
                div.classList.remove('completo', 'position-relative', 'z-index-100');
            }else {
                if(foto2){
                    div.innerHTML = `
                        ${foto2}
                        <h3>${usuario.user__username}</h3>
                        <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
                        <p><strong>Mail:</strong> ${usuario.mail}</p>
                        <p><strong>DNI:</strong> ${usuario.dni}</p>
                        <p><strong>Fecha de nacimiento:</strong> ${usuario.fecha_nacimiento}</p>
                        <p><strong>Domicilio:</strong> ${usuario.domicilio}</p>
                        <p><strong>Telefono:</strong> ${usuario.telefono}</p>
                        <p><strong>Instagram:</strong> ${usuario.instagram}</p>
                        <p><strong>Cargado el:</strong> ${usuario.cargado}</p>
                    `;
                }else{
                    div.innerHTML = `
                        <img src="../../../static/img/kinef_logo1.png" alt="Logo de Kinef" class='circulo'>
                        <h3>${usuario.user__username}</h3>
                        <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
                        <p><strong>Mail:</strong> ${usuario.mail}</p>
                        <p><strong>DNI:</strong> ${usuario.dni}</p>
                        <p><strong>Fecha de nacimiento:</strong> ${usuario.fecha_nacimiento}</p>
                        <p><strong>Domicilio:</strong> ${usuario.domicilio}</p>
                        <p><strong>Telefono:</strong> ${usuario.telefono}</p>
                        <p><strong>Instagram:</strong> ${usuario.instagram}</p>
                        <p><strong>Cargado el:</strong> ${usuario.cargado}</p>
                    `;
                }
                div.classList.add('completo', 'position-relative', 'z-index-100');
            }
        })
        usuarios_cargados.appendChild(div);
    });
}