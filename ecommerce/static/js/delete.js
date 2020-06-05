function confirmarEliminacion(id){
Swal.fire({
title: 'Estas seguro de querer eliminar la película?',
text: "No podrás volver atrás!",
icon: 'warning',
showCancelButton: true,
confirmButtonColor: '#3085d6',
cancelButtonColor: '#d33',
confirmButtonText: 'Si, Eliminarla!',
cancelButtonText:'Cancelar'
}).then((result) => {
if (result.value) {
	//redirigir a la ruta de eliminar
	window.location.href="/delete/"+id+"/";
}
})
