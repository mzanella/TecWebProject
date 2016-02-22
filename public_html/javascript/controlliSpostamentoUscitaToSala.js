var input = {
	incasso: ["0",/^\d{2,}$/, "incasso del film non inserito o non valido"],
	recensione : ["recensione del film...", /.{25,}/, "recensione non inserita o troppo breve"],
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
	data = document.getElementById("filmSelezionato");
	if(data.value=="")
		return false;
	else
		return true && validazione;
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




