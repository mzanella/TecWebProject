#!/usr/bin/perl -w
use CGI;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use CGI::Session;
use lib 'perl/modules/';
use PageSkeleton;
print "Content-Type: text/html\n\n";
my $nomePagina = "Conferma - InstaFilm";
my $description = "Conferma della rimozione da in sala di un film";
my $keyword = "Film, Cinema, InstaFilm";
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print "<meta http-equiv=\"refresh\" content=\"5; url=Amministrazione.cgi\">";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> <a href=\"RimuoviFilmDaSala.cgi\">Rimuovi film dalla sala</a> <span class=\"breadcrumb\">-&gt;</span> ".$nomePagina;
PageSkeleton::printBreadCrumb($nomeBC);
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
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
	"
	<h1>Rimozione avvenuta con successo</h1>
		<p class=\"messaggioConferma\">Il film è stato rimosso dalla sezione <a href=\"OraInSala.cgi\">Ora in sala</a></p>
		<p class=\"messaggioConferma\">Entro 5 secondi verrai rimandato alla pagina di amministrazione. In alternativa, clicca sul <a href=\"Amministrazione.cgi\">link</a>.</p>
	";
}
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
