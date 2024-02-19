 
var $ = jQuery.noConflict();


function abrir_modal(url) {
    $('#modal').load(url, function(){
        $(this).modal('show');
    });
} 

function cerrar_modal() {
    $('#modal').modal('hide');
} 

