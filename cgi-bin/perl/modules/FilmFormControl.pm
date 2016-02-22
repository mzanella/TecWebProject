#!/usr/bin/perl
#modulo per il controllo delle form dei film
package FilmFormControl;
use strict;
use File::Basename;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use HTML::Entities ();
use Fcntl ':flock';
use lib 'modules/';
use DBFunctions;

#queste funzioni servono per stampare a video il campo dati con eventuali errori
sub titolo{
	my $s=$_[0];
	my $titolo=$_[1];
	print "<div>
		<label for=\"titolo\">Titolo (<abbr title=\"minimo\">min.</abbr> 1 carattere):<span class=\"obbligatorio\">*</span></label>
		<input type=\"text\" name=\"titolo\" id=\"titolo\" value=\"$titolo\"/>";
	if(defined $s){
		print "<span id=\"errtitolo\">$s</span>";
	}
	print "</div>"
}

sub paeseDiProduzione{
	my $s=$_[0];
	my $paese=HTML::Entities::decode($_[1]);
	print "<div>
		<label for=\"paeseDiProduzione\">Paese di produzione (<abbr title=\"minimo\">min.</abbr> 2 caratteri):<span class=\"obbligatorio\">*</span></label>
		<input type=\"text\" name=\"paeseDiProduzione\" id=\"paeseDiProduzione\" value=\"$paese\"/>";
	if(defined $s){
		print "<span id=\"errpaeseDiProduzione\">$s</span>";
	}
	print "</div>"
}

sub durata {
	my $s=$_[0];
	my $durata=$_[1];
	print "<div>
		<label for=\"durata\">Durata (in minuti, <abbr title=\"minimo\">min.</abbr> 2 caratteri):<span class=\"obbligatorio\">*</span></label>
		<input type=\"text\" name=\"durata\" id=\"durata\" value=\"$durata\"/>";
	if(defined $s){
		print "<span id=\"errdurata\">$s</span>";
	}
	print "</div>"
}

sub incasso {
	my $s=$_[0];
	my $incasso=$_[1];
	print "<div>
		<label for=\"incasso\">Incasso (in Milioni di euro, <abbr title=\"minimo\">min.</abbr> 1 carattere):<span class=\"obbligatorio\">*</span></label>
		<input type=\"text\" name=\"incasso\" id=\"incasso\" value=\"$incasso\"/>";
	if(defined $s){
		print "<span id=\"errincasso\">$s</span>";
	}
	print "</div>"
}

sub regia {
	my $s=$_[0];
	my $regia=$_[1];
	print "<div>
		<label for=\"regia\">Regia (<abbr title=\"minimo\">min.</abbr> 2 caratteri):<span class=\"obbligatorio\">*</span></label>
		<input type=\"text\" name=\"regia\" id=\"regia\" value=\"$regia\"/>";
	if(defined $s){
		print "<span id=\"errregia\">$s</span>";
	}
	print "</div>"
}

sub attori {
	my $s=$_[0];
	my $attori=$_[1];
	print "<div>
		<label for=\"attori\">Attori (<abbr title=\"minimo\">min.</abbr> 2 caratteri):<span class=\"obbligatorio\">*</span></label>
		<textarea name=\"attori\" id=\"attori\" rows=\"5\" cols=\"150\">$attori</textarea>";
	if(defined $s){
		print "<span id=\"errattori\">$s</span>";
	}
	print "</div>"
}

sub trama {
	my $s=$_[0];
	my $trama=$_[1];
	print "<div>
		<label for=\"trama\">Trama: (<abbr title=\"minimo\">min.</abbr> 25 caratteri):<span class=\"obbligatorio\">*</span></label>
		<textarea name=\"trama\" id=\"trama\" rows=\"5\" cols=\"150\">$trama</textarea>";
	if(defined $s){
		print "<span id=\"errtrama\">$s</span>";
	}
	print "</div>"
}

sub dataUscita {
	my $s=$_[0];
	my $giornoUscita=$_[1];
	my $meseUscita=$_[2];
	my $annoUscita=$_[3];
	my $annoVecchio=$_[4];

	print "<div>";
	print "<label for=\"dataUscita\">Data uscita nelle sale:<span class=\"obbligatorio\">*</span></label>
		<fieldset id=\"dataUscita\">
		<label for=\"giornoUscita\" class=\"labelUscita\">Giorno:</label>
		<select name=\"giornoUscita\" id=\"giornoUscita\">";
		for(my $index = 1; $index <= 31; $index++){
			if ($index==$giornoUscita){
				print "<option selected=\"selected\" value=\"$index\">$index</option>";
			} else {
				print "<option value=\"$index\">$index</option>";
			}
		}
	print	"</select>
		<label for=\"meseUscita\" class=\"labelUscita\">Mese:</label>
		<select name=\"meseUscita\" id=\"meseUscita\">";
		for(my $index = 1; $index <= 12; $index++){
			if ($index==$meseUscita){
				print "<option selected=\"selected\" value=\"$index\">$index</option>";
			} else{
				print "<option value=\"$index\">$index</option>";
			}
		}
	print	"</select>
			<label for=\"annoUscita\" class=\"labelUscita\">Anno:</label>
			<select name=\"annoUscita\" id=\"annoUscita\">";
			(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst)=localtime(time);
				if (defined $annoVecchio){
					for(my $index = -36; $index <= 5; $index++){
							my $value = $year + 1900 + $index;
							if ($value==$annoUscita){
								print "<option selected=\"selected\" value=\"$value\">$value</option>";
							} else {
								print "<option value=\"$value\">$value</option>";
							}
					}
				}
				else{
					for(my $index = 0; $index <= 5; $index++){
							my $value = $year + 1900 + $index;
							if ($value==$annoUscita){
								print "<option selected=\"selected\" value=\"$value\">$value</option>";
							} else {
								print "<option value=\"$value\">$value</option>";
							}
					}
				}
	print "</select>
		   </fieldset>";

	if(defined $s){
		print "<span id=\"errdataUscita\">$s</span>";
	}

	print "</div>";
}

sub annoDiProduzione {
	my $annoProduzione=$_[0];
	my $annoVecchio=$_[1];
	print "<label for=\"annoProduzione\">Anno produzione:<span class=\"obbligatorio\">*</span></label>
			<select name=\"annoProduzione\" id=\"annoProduzione\">";
	(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst)=localtime(time);
	if (defined $annoVecchio){
		for(my $index = -36; $index <= 5; $index++){
				my $value = $year + 1900 + $index;
				if ($value==$annoProduzione){
					print "<option selected=\"selected\" value=\"$value\">$value</option>";
				} else {
					print "<option value=\"$value\">$value</option>";
				}
		}
	}
	else{
		for(my $index = 0; $index <= 5; $index++){
				my $value = $year + 1900 + $index;
				if ($value==$annoProduzione){
					print "<option selected=\"selected\" value=\"$value\">$value</option>";
				} else {
					print "<option value=\"$value\">$value</option>";
				}
		}
	}
	print "</select>";
}

sub genere {
	my $gen=$_[0];
	my $db_path='../data/database/generi.xml';
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my @generi = $root->getElementsByTagName("genere");
	print"<label for=\"genere\">Genere<span class=\"obbligatorio\">*</span></label>
		  <select id=\"genere\" name=\"genere\">";

	foreach my $genere (@generi){
		$genere = $genere->firstChild->data;
		my $s = "";
		if ($gen eq $genere){
			$s = "selected=\"selected\"";
		}

		print "<option value=\"$genere\" $s>".ucfirst($genere)."</option>";
	}
	print "</select>";
}

sub recensione {
	my $s=$_[0];
	my $recensione=$_[1];
	print "<div>
		<label for=\"recensione\">Recensione (<abbr title=\"minimo\">min.</abbr> 25 caratteri):<span class=\"obbligatorio\">*</span></label>
		<textarea name=\"recensione\" id=\"recensione\" rows=\"5\" cols=\"150\" >$recensione</textarea>";
	if(defined $s){
		print "<span id=\"errrecensione\">$s</span>";
	}
	print "</div>"
}

sub descrizione {
	my $s=$_[0];
	my $descrizione=$_[1];
	print "<div>
		<label for=\"locDescr\">Fornisci una descrizione per la locandina (<abbr title=\"minimo\">min.</abbr> 15 caratteri):<span class=\"obbligatorio\">*</span></label>
		<input type=\"text\" name=\"locDescr\" id=\"locDescr\" value=\"$descrizione\" />";
		if(defined $s){
			print "<span id=\"errrecensione\">$s</span>";
		}
	print "</div>"
}

sub valutazione {
	my $err=$_[0];
	my $val=$_[1];
	print"<div>
		  <label for=\"ValutazioneFilmVoti\">Valutazione del film: <span class=\"obbligatorio\">*</span></label>
		  <fieldset id=\"ValutazioneFilmVoti\">";
	for (my $i = 1; $i <= 5; $i++){
		my $s="";
		if ($val eq $i){
			$s = "checked='checked'";
		}
		print "<input type=\"radio\" name=\"ValutazioneFilm\" value=\"$i\" id=\"ValutazioneFilm$i\" $s />
			<label for=\"ValutazioneFilm$i\">$i</label>";
	}
	print "</fieldset>
			<span id=\"errValutazioneFilm\">$err</span>
		   </div>";
}

#queste funzioni servono per fare il controllo che il relatico campo dati sia corretto. se non
#lo è ritornano la stringa di errore e 1 per indicare che c'è un errore
sub controlloTitolo {
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'titolo'})==0){
		$errorstring="Errore: titolo non inserito";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloPaese{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'paeseDiProduzione'})==0){
		$errorstring="Errore: paese di produzione non inserito";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloDurata{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'durata'})==0){
		$errorstring="Errore: durata non inserita";
		$error=1;
	} elsif (!($input->{'durata'}=~/^\d{1,}$/)){
		$errorstring="Errore: durata non valida";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloIncasso{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'incasso'})==0){
		$errorstring="Errore: incasso non inserito";
		$error=1;
	} elsif (!($input->{'incasso'}=~m/^\d{1,}$/)){
		$errorstring="Errore: incasso non valido";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloRegia{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'regia'})==0){
		$errorstring="Errore: regia non inserita";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloAttori{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'attori'})==0){
		$errorstring="Errore: attori non inseriti";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloTrama{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'trama'})<25){
		$errorstring="Errore: trama non inserita o troppo breve";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloData{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst)=localtime(time);
	if ($input->{'giornoUscita'}>30 and ($input->{'meseUscita'}==11 || $input->{'meseUscita'}==4 || $input->{'meseUscita'}==6 || $input->{'meseUscita'}==9)){
		$errorstring="Errore: data non valida";
		$error=1;
	} elsif ($input->{'giornoUscita'}>28 and $input->{'meseUscita'}==2 and $input->{'annoUscita'}%4!=0){
		$errorstring="Errore: data non valida";
		$error=1;
	} elsif ($input->{'giornoUscita'}>29 and $input->{'meseUscita'}==2 and $input->{'annoUscita'}%4==0){
		$errorstring="Errore: data non valida";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloRecensione{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'recensione'})<25){
		$errorstring="Errore: recensione non inserita o troppo breve";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloValutazione{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;

	if (! defined($input->{'ValutazioneFilm'})){
		$errorstring="Errore: valutazione non inserita";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloSelezione{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;

	if ($input->{'selezione'} eq ""){
		$errorstring="Errore: nessun film selezionato";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

sub controlloDescrizioneLoc{
	my $input = $_[0];
	my $errorstring=undef;
	my $error;
	if (length($input->{'locDescr'})<15){
		$errorstring="Errore: descrizione della locandina non inserita o troppo breve";
		$error=1;
	}
	my @return;
	push @return, $errorstring;
	push @return, $error;
	return @return;
}

#svuota la sessione rigenerandola con solamente i dati dell'utente che servono per continuare la navigazione
sub rigeneraSessione{
	my $session=$_[0]; #prende la sessione passata e legge i paramentri
	my $e = $session->param("utenteEmail");
	my $n = $session->param("utenteNome");
	my $a = $session->param("utenteAdmin");

	$session->close(); #chiude e pulisce
	$session->delete();
	$session->flush();

	$session = CGI::Session->new(); #genera una nuova sessione
	$session->expires(0);
	$session->param("utenteEmail", $e);
	$session->param("utenteNome", $n);
	$session->param("utenteAdmin", $a);
	return $session;
}

#salva l'immagine in un percorso predefinito e restituisce il percorso da salvare nel database
sub saveImage{
	my $input = $_[0];
	my $query = $_[1];
	my $path = "../data/database/locandine/locandina_non_disponibile.jpg";
	if ($query->param("locandina") ne ""){
		$path=$query->param("locandina");
	}
	return $path;
}


1;
