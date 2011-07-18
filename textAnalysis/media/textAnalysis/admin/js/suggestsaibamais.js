function SuggestSaibaMais(id,configs) {
    this.config = configs || {};
	this.id = id;
	this.local = $('#' + this.id);
	this.classify();
	this.configura();
}
SuggestSaibaMais.prototype = {

	configura:function() {
		var self = this;
		this.local.find('input').click(function(i){
		    self.classify();
		});
	},

	classify:function() {
		var self = this;
		corpo = CKEDITOR.instances.id_corpo.getData();
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
                $("#saibamais ul").html(msg);
	        }
	    }).responseText;
	    
        // $(".items").draggable({helper: 'clone'});
        //         $(".droparea").droppable({
        //             accept: ".items",
        //             hoverClass: 'dropareahover',
        //             tolerance: 'pointer',
        //             drop: function(ev, ui) {
        //                 var dropElem = ui.draggable.html();                
        //                 $(this).append(dropElem);
        //             }
        //         });
        // });
    	
                
    	$( ".items" ).draggable();
        // $( ".droparea" ).droppable({
        //  drop: function( event, ui ) {
        //      $(this).append( "Dropped!" );
        //  }
        // });
	
                
	},		

}