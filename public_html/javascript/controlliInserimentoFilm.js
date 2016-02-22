var input = {
	titolo: ["titolo del film", /.{1,}/, "titolo del film non inserito"],
	//locandina : ["", /.{0,}/, "locandina non inserita"],
	locDescr : ["descrizione della locandina", /.{15,}/, "descrizione della locandina non inserita o troppo breve"],
	paeseDiProduzione: ["nome paese", /.{2,}/, "paese di produzione non inserito"],
	durata: ["180", /^\d{2,}$/, "durata del film non inserita"],
	//anno : ["2016", /^(19|20)\d{1,2}$/, "anno non inserito o non valido"],
	//dataUscita : ["gg", /^\d{1,2}$/, "giorno non inserito o non valido"],
	regia: ["regia", /.{2,}/, "regia del film non inserita"],
	attori: ["attori", /.{2,}/, "attori non inseriti"],
	trama: ["trama del film...", /.{25,}/, "trama non inserita o troppo breve"],
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
	for (var key in input) {
		var data = document.getElementById(key);
		addPlaceholder(data);

		data.addEventListener("focus", function() {
			if (this.value == input[this.id][0]) {
				this.value = "";
				this.className = "text";
			}
		}, true);

		data.addEventListener("blur", function() {
			errorid = "err" + this.id
			var padre = this.parentNode;
			var errore = document.getElementById("err" + this.id);
			if (errore != undefined) {
				remove(errore);
			}
			controlData(this, padre, errore);
		}, true);

		if(data.value == input[key][0]){
			data.className = "placeholder";
		}

	}

	var g = document.getElementById("giornoUscita");
	var m = document.getElementById("meseUscita");
	var a = document.getElementById("annoUscita");
	m.addEventListener("change", function() {
		var selected = g.value;
		var s = "";
		if (m.value == 11 || m.value == 4 || m.value == 6 || m.value == 9) {
			for (var i = 1; i <= 30; i++) {
				if (i == selected)
					s = s + '<option selected="selected" value="' + i + '">' + i + '</option>';
				else
					s = s + '<option value="' + i + '">' + i + '</option>';
			}
		} else if (m.value == 2 && a.value % 4 != 0) {
			for (var i = 1; i <= 28; i++) {
				if (i == selected)
					s = s + '<option selected="selected" value="' + i + '">' + i + '</option>';
				else
					s = s + '<option value="' + i + '">' + i + '</option>';
			}
		} else if (m.value == 2 && a.value % 4 == 0) {
			for (var i = 1; i <= 29; i++) {
				if (i == selected)
					s = s + '<option selected="selected" value="' + i + '">' + i + '</option>';
				else
					s = s + '<option value="' + i + '">' + i + '</option>';
			}
		} else {
			for (var i = 1; i <= 31; i++) {
				if (i == selected)
					s = s + '<option selected="selected" value="' + i + '">' + i + '</option>';
				else
					s = s + '<option value="' + i + '">' + i + '</option>';
			}
		}
		g.innerHTML = s;
	});

	a.addEventListener("change", function() {
		var selected = g.value;
		var s = "";
		if (m.value == 2 && a.value % 4 != 0) {
			for (var i = 1; i <= 28; i++) {
				if (i == selected)
					s = s + '<option selected="selected" value="' + i + '">' + i + '</option>';
				else
					s = s + '<option value="' + i + '">' + i + '</option>';
			}
			g.innerHTML = s;
		} else if (m.value == 2 && a.value % 4 == 0) {
			for (var i = 1; i <= 29; i++) {
				if (i == selected)
					s = s + '<option selected="selected" value="' + i + '">' + i + '</option>';
				else
					s = s + '<option value="' + i + '">' + i + '</option>';
			}
			g.innerHTML = s;
		}
	});

}

function addPlaceholder(el) {
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
