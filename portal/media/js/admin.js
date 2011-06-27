jQuery(function($) {
    $("#id_elemento").change(function() {
        id = $(this).val()
        if (id != "") {
		    nome = $("#id_elemento option:selected").text()
		    $.getJSON("/portal/"+ nome +"/api/"+ nome +"/todos.js", function(j,result) {
		        var options = '<option value="">---------- </option>';
		        if (result == 'success') {
		            var valor = ''
		            for (var i = 0; i < j.length; i++) {
		             options += '<option value="' + parseInt(j[i].id) + '"' + valor + '>' + parseInt(j[i].id) + ' - ' + j[i].title + '</option>';
		            }
		        } 
		        $("#id_instancia").html(options)
		    });
		}
     });
});



