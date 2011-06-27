function Classify() {

    bodyContent = $.ajax({
          url: "/admin/textClassification/materia/classify/",
          global: false,
          type: "POST",
          data: ({texto : $("#id_corpo").val(), titulo : $("#id_titulo").val(), subtitulo : $("#id_subtitulo").val(),}),
          dataType: "html",
          async:false,
          success: function(msg){
             $("#id_tags").val(msg);
          }
       }
    ).responseText;

}

