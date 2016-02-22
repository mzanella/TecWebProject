#!/usr/bin/perl -w
use CGI;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib './perl/modules/';
use PageSkeleton;
use DBFunctions;
print "Content-Type: text/html\n\n";
my $nomePagina = "Amministrazione";
PageSkeleton::printDocType();
my $nomePagina = "Amministrazione - InstaFilm";
my $description = "Pagina di amministrazione del sito InstaFilm";
my $keyword = "Film, Cinema, InstaFilm";
PageSkeleton::printHead($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb("Amministrazione");
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
#Qui va inserito il contenuto
#controllo sel'utente è registrato come amministratore
my $cgi = new CGI;
my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
my $session = load CGI::Session();
if (DBFunctions::controlAdmin($session->param("utenteEmail")) == 0){
	print "<h1>Accesso negato</h1>
		   <p>Sezione riservata solamente agli amministratori del sito web.</p>
		   <p>Se sei un amministratore devi eseguire il <a href=\"Login.cgi\">login</a> prima di poter accere.</p>";
} else {
print
" <h1> Amministrazione </h1>
<h2>Gestisci film in uscita</h2>
<ul class=\"adminList\">
	<li><a href=\"InserisciFilmUscita.cgi\">Inserisci film in uscita</a></li>1

</ul>
<h2>Gestisci film in sala</h2>
<ul class=\"adminList\">
	<li><a href=\"SceltaInserimentoFilmSala.cgi\">Inserisci film in sala</a></li>
	<li><a href=\"RimuoviFilmDaSala.cgi\">Rimuovi film dalla sala</a></li>
</ul>
<h2>Inserisci</h2>
<ul class=\"adminList\">
	<li><a href=\"RecensisciNuovoFilm.cgi\">Recensisci un nuovo film</a></li>
</ul>
<h2>Modifica</h2>
<ul class=\"adminList\">
	<li><a href=\"SelezionaFilmDaModificare.cgi\">Modifica un film già recensito</a></li>
	<li><a href=\"SelezionaFilmDaModificareProssimamente.cgi\">Modifica un film in uscita</a></li>
</ul>
<h2>Cancella</h2>
<ul class=\"adminList\">
	<li><a href=\"CancellaFilm.cgi\">Cancella film</a></li>
</ul>
";

}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
