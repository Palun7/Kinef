const foto_perfil = document.getElementById('foto_perfil_contenedor');

foto_perfil.addEventListener('click', ()=> {
    if(foto_perfil.classList.contains('trescientos-px')){
        foto_perfil.classList.remove('trescientos-px');
    }else{
        foto_perfil.classList.add('trescientos-px');
    }
})
