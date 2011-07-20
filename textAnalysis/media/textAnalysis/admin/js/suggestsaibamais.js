function SuggestSaibaMais() {
	corpo = CKEDITOR.instances.id_corpo.getSnapshot();
	titulo = $("#id_titulo").val()
	subtitulo = $("#id_subtitulo").val()
	permalink = $('#id_permalink').val()
    bodyContent = $.ajax({
         url: "/classify/",
         global: false,
         type: "POST",
         data: ({'texto' : corpo, 
                 'titulo' : titulo, 
                 'subtitulo' : subtitulo,
                 'permalink' : permalink, }),
         dataType: "html",
         async:false,
         success: function(msg){
        }
    }).responseText;
    return bodyContent;
}