var input = {
	ricerca: ["cerca per titolo o per genere", /\.{1,}/, ""],
};

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
			var padre = this.parentNode;
			controlData(this, padre);
		}, true);

		if(data.value == input[key][0]){
			data.className = "placeholder";
		}

	}
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
		addPlaceholder(el);
		return false
	} else return true;
}
