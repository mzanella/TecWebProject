function validaForm() {
	var data = document.getElementById("film");
	if (data == null)
		data = document.getElementById("filmSelezionato");
	if (data == null)
		data = document.getElementById("filmDaRimuovereDaInSala");
	if(data.value=="")
		return false;
	else
		return true;
};
