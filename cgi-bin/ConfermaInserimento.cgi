#!/usr/bin/perl -w
use CGI;
use CGI::Session;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib 'perl/modules/';
use PageSkeleton;
print "Content-Type: text/html\n\n";
my $nomePagina = "Conferma inserimento";
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print "<meta http-equiv=\"refresh\" content=\"5; url=Amministrazione.cgi\" />";
my $nomePagina = "Conferma - InstaFilm";
my $description = "Conferma dello spostamento di un film";
my $keyword = "Film, Cinema, InstaFilm";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);

PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> <a href=\"InserisciFilmUscita.cgi\">Inserisci film in uscita</a> <span class=\"breadcrumb\">-&gt;</span> ".$nomePagina;
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
	<h1>Film inserito con successo</h1>
		<p class=\"messaggioConferma\">Il film è stato inserito nella sezione <a href=\"Prossimamente.cgi\">Prossimamente</a>.</p>
		<p class=\"messaggioConferma\">Entro 5 secondi verrai rimandato alla pagina di amministrazione. In alternativa, clicca sul <a href=\"Amministrazione.cgi\">link</a>.</p>
	";
}
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
