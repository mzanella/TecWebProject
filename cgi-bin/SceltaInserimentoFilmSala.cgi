#!/usr/bin/perl -w
use CGI;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib './perl/modules/';
use PageSkeleton;
print "Content-Type: text/html\n\n";
PageSkeleton::printDocType();
my $nomePagina = "Inserisci film in sala - InstaFilm";
my $description = "Pagina per selezionare un film da mettere in sala";
my $keyword = "Film, Cinema, InstaFilm, Film in sala";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
PageSkeleton::printHead($nomePagina);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> "."Inserisci film in sala";
PageSkeleton::printBreadCrumb($nomeBC);
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
#Qui va inserito il contenuto
my $cgi = new CGI;
my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
my $session = load CGI::Session();
if (DBFunctions::controlAdmin($session->param("utenteEmail")) == 0){
	print "<h1>Accesso negato</h1>
		   <p>Sezione riservata solamente agli amministratori del sito web.</p>
		   <p>Se sei un amministratore devi eseguire il <a href=\"Login.cgi\">login</a> prima di poter accere.</p>";
} else {
	print
	"<h1>Nuovo film in sala</h1>
	<ul class=\"adminList\">
		<li><a href=\"SelezionaFilmUscitaToSala.cgi\">Sposta film dai film in uscita</a></li>
		<li><a href=\"InserisciNuovoFilmSala.cgi\">Inserisci nuovo film in sala</a></li>
	</ul>";
}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
