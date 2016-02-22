#!/usr/bin/perl -w
use CGI;
#use utf8;
#binmode STDIN, ":encoding(utf8)";
#binmode STDOUT, ":encoding(utf8)";
#use Encode;
use lib './perl/modules/';
use PageSkeleton;
use DBFunctions;
print "Content-Type: text/html\n\n";

my $cgi = new CGI;
my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
my $session = load CGI::Session();
my $erremail = $session->param("errEmail");
my $errpass = $session->param("errPassword");
my $errpassc = $session->param("errPasswordConferma");
my $errnome = $session->param("errNome");
my $errcognome = $session->param("errCognome");
my $errddn = $session->param("errDataDiNascita");
my $email = $session->param("email") || undef;
my $pass = $session->param("password") || undef;
my $passc = $session->param("passwordConferma") || undef;
my $nome = $session->param("nome") || undef;
my $cognome = $session->param("cognome") || undef;
my $giorno = $session->param("giorno") || undef;
my $mese = $session->param("mese") || undef;
my $anno = $session->param("anno") || undef;
my $nomePagina = "Registrati";
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print
"	<script type=\"text/javascript\" src=\"../public_html/javascript/button.js\"></script>
	<script type=\"text/javascript\" src=\"../public_html/javascript/controlliRegistrati.js\"></script>";
my $nomePagina = "Registrati - InstaFilm";
my $description = "Pagina per la registrazione a InstaFilm";
my $keyword = "Film, Cinema, InstaFilm, Registrati";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
print "<body onload=\" ridimensionamentoPagina(); caricamento();\">";
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb("Registrati");
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
#Qui va inserito il contenuto
if ($session->param("utenteEmail") eq undef){
	print
	"
		<h2>Registrazione</h2>
			<form id=\"registrazione\" action=\"perl/controlliRegistrazione.cgi\" method=\"post\"
			onsubmit=\"return validaForm()\" accept-charset=\"UTF-8\">
			<fieldset>
				<fieldset>
					<legend >Dati per il login</legend>";
						&email($erremail);
						&password($errpass);
						&cPassword($errpassc);
	print "
				</fieldset>
				<fieldset>
					<legend>Dati personali</legend>";
						&nome($errnome);
						&cognome($errcognome);
						&dataDiNascita($errddn);
	print "
				</fieldset>";
				&categorie();
	print "
					<input type=\"submit\" value=\"Registrati\" />
			</fieldset>
			</form>";
} else {
	my $nome = $session->param("utenteNome");
	print
	"<h2 id=\"h2Login\">Errore</h2>
	<p id=\"erroreLogin\">Sei già loggato come $nome.
		Se non sei tu procedi al <a href=\"Logout.cgi\">logout</a> e rieffettua il login con il tuo account.</p>";
}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();

sub email(){
	my $s=$_[0];
	print "<div><label for=\"email\">Email:</label><input type=\"text\" name=\"email\" id=\"email\" value=\"$email\" />";
	if(defined $s){
		print "$s";
	}
	print "</div>"
}

sub password(){
	my $s=$_[0];
	print"<div>
	<label for=\"password\">Password (la password deve esssere di almeno 8 caretteri):</label>
	<input type=\"password\" name=\"password\" id=\"password\" />";
	if(defined $s){
		print "$s";
	}
	print "</div>"
}

sub cPassword(){
	my $s=$_[0];
	print "<div>
	<label for=\"passwordConferma\">Password di conferma:</label>
	<input type=\"password\" name=\"passwordConferma\" id=\"passwordConferma\" />";
	if(defined $s){
		print "$s";
	}
	print "</div>"
}

sub nome(){
	my $s=$_[0];
	print "<div>
	<label for=\"nome\">Nome:</label>
	<input type=\"text\" name=\"nome\" id=\"nome\" value=\"$nome\" />";
	if(defined $s){
		print "$s";
	}
	print "</div>"
}

sub cognome(){
	my $s=$_[0];
	print "<div>
	<label for=\"cognome\">Cognome:</label>
	<input type=\"text\" name=\"cognome\" id=\"cognome\" value=\"$cognome\" />";
	if(defined $s){
		print "$s";
	}
	print "</div>"
}

sub dataDiNascita(){
	my $s=$_[0];

	print "<div>";
	print "<label for=\"dataDiNascita\">Data di nascita:</label>
		<fieldset id=\"dataDiNascita\">
		<label for=\"giorno\" class=\"labelUscita\">Giorno:</label>
		<select name=\"giorno\" id=\"giorno\">";
		for(my $index = 1; $index <= 31; $index++){
			if ($index==$giorno){
				print "<option selected=\"selected\" value=\"$index\">$index</option>";
			} else {
				print "<option value=\"$index\">$index</option>";
			}
		}
		print	"</select>
		<label for=\"mese\" class=\"labelUscita\">Mese:</label>
		<select name=\"mese\" id=\"mese\">";
		for(my $index = 1; $index <= 12; $index++){
			if ($index==$mese){
				print "<option selected=\"selected\" value=\"$index\">$index</option>";
			} else{
				print "<option value=\"$index\">$index</option>";
			}
		}

	print	"</select>
			<label for=\"anno\" class=\"labelUscita\">Anno:</label>
			<select name=\"anno\" id=\"anno\">";

			($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time);
				for(my $index = 94; $index >= 0; $index--){
						my $value = $year + 1800 + $index;
						if ($value==$anno){
							print "<option selected=\"selected\" value=\"$value\">$value</option>";
						} else {
							print "<option value=\"$value\">$value</option>";
						}
				}
	print "</select>
		</fieldset>";

	if(defined $s){
		print "$s";
	}

	print "</div>";
}


sub categorie() {
	my $db_path=DBFunctions::percorsoGeneriFilm;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my @generi = $root->getElementsByTagName("genere");
	print"<fieldset id=\"categorie\">
		<legend>Categorie di film</legend>";

	foreach my $genere (@generi){
		$genere = $genere->firstChild->data;
		my $isSet = $session->param($genere) || undef;
		$genere =~ s/^\s+|\s+$//g;
		my $s = "";
		if (defined($isSet)){
			$s = "checked=\"checked\"";
		}
		print "<input type=\"checkbox\" name=\"$genere\" id=\"$genere\" $s />
				<label for=\"$genere\" >".ucfirst($genere)."</label>";
	}
	print "</fieldset>";
}
