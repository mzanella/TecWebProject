var input = {
	email : ["email@dominio.com", /^([\w\-\+\.]+)@([\w\-\+\.]+).([\w\-\+\.]+)$/, "email non valida o non inserita"],
	password : ["password", /.{8,}/, "la password deve essere di almeno otto caratteri"],
	passwordConferma : ["password", /.{8,}/, "password e password di conferma differenti"],
	nome : ["Nome", /\w{1,}/, "nome non inserito"],
	cognome : ["Cognome", /\w{1,}/, "cognome non inserito"],
	giorno : ["gg", /^\d{1,2}$/, "giorno non inserito o non valido"],
	mese : ["mm", /^\d{1,2}$/, "messe non inserito o non valido"],
	anno : ["AAAA", /^(19|20)\d{1,2}$/, "anno non inserito o non valido"]
};

function validaForm() {
	var validazione = true;
	var data;
	var padre;
	var errore;
	for (var key in input){
		data = document.getElementById(key);
		padre = data.parentNode;
		var x = controlData(data, padre);
		validazione = validazione && x;
	}
	return validazione;
};

function remove(el) {
	el.parentNode.removeChild(el);
}

function caricamento() {
	for(var key in input){
		var data = document.getElementById(key);
		addPlaceholder(data);
		
		data.addEventListener("focus", function(){
			if(this.value == input[this.id][0]){
				this.value = "";
				this.className = "text";
			}
		}, true);

		data.addEventListener("blur", function(){
			errorid = "err"+this.id
			var padre = this.parentNode;
			var errore = document.getElementById("err"+this.id);
			if (errore != undefined){
				remove(errore);
			}
			controlData(this, padre, errore);
		}, true);

		if(data.value == input[key][0]){
			data.className = "placeholder";
		}
	}

	var g = document.getElementById("giorno");
	var m = document.getElementById("mese");
	var a = document.getElementById("anno");
	m.addEventListener("change", function() {
		var selected = g.value;
		var s = "";
    	if(m.value == 11 || m.value == 4 || m.value == 6 || m.value == 9) {
			for (var i = 1; i <= 30; i++){
				if (i == selected)
					s = s+'<option selected="selected" value="'+i+'">'+i+'</option>';
				else
					s = s+'<option value="'+i+'">'+i+'</option>';
			}
		} else if (m.value == 2 && a.value % 4 != 0){
			for (var i = 1; i <= 28; i++){
				if (i == selected)
					s = s+'<option selected="selected" value="'+i+'">'+i+'</option>';
				else
					s = s+'<option value="'+i+'">'+i+'</option>';
			}
		} else if (m.value == 2 && a.value % 4 == 0){
			for (var i = 1; i <= 29; i++){
				if (i == selected)
					s = s+'<option selected="selected" value="'+i+'">'+i+'</option>';
				else
					s = s+'<option value="'+i+'">'+i+'</option>';
			}
		} else {
			for (var i = 1; i <= 31; i++){
				if (i == selected)
					s = s+'<option selected="selected" value="'+i+'">'+i+'</option>';
				else
					s = s+'<option value="'+i+'">'+i+'</option>';
			}
		}
		g.innerHTML=s;
	});
	a.addEventListener("change", function() {
		if ((m.value == 2 && a.value % 4 != 0)||(m.value == 2 && a.value % 4 == 0)){
			var selected = g.value;
			var s = "";
	    	if (m.value == 2 && a.value % 4 != 0){
				for (var i = 1; i <= 28; i++){
					if (i == selected)
						s = s+'<option selected="selected" value="'+i+'">'+i+'</option>';
					else
						s = s+'<option value="'+i+'">'+i+'</option>';
				}
			} else if (m.value == 2 && a.value % 4 == 0){
				for (var i = 1; i <= 29; i++){
					if (i == selected)
						s = s+'<option selected="selected" value="'+i+'">'+i+'</option>';
					else
						s = s+'<option value="'+i+'">'+i+'</option>';
				}
			} 
			g.innerHTML=s;
		}
    });	
}

function addPlaceholder(el){
	if (el.value == "") {
		el.value = input[el.id][0];
		el.className = "placeholder";
	}
}

function controlData(el, padre) {
	var text = el.value;
	var regexp = input[el.id][1];
	var errorid = "err"+el.id;
	if (text.search(regexp) != 0 ) {
		var errore = document.getElementById(errorid);
		if (errore == null){
			errore = document.createElement("span");
			errore.id = (errorid);
		}
		errore.innerHTML=input[el.id][2];
		padre.appendChild(errore);
		errore.className = "errore";
		addPlaceholder(el);
		return false
	} else return true;
}


