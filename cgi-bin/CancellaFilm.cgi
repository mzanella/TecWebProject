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
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print
"	<script type=\"text/javascript\" src=\"../public_html/javascript/selezionaFilm.js\"></script>";
my $nomePagina = "Cancella un film - InstaFilm";
my $description = "Cancellazione di un film";
my $keyword = "Film, Cinema, InstaFilm";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> "."Cancella un film";
PageSkeleton::printBreadCrumb($nomeBC);
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
my $errselezione = $session->param("errSelezione");
print
	"<h1>Cancella film</h1>
	<form id=\"frmFilm\" action=\"perl/rimozione.cgi\" method=\"post\" onsubmit=\"return validaForm();\">
		<fieldset>
			<legend>Film da cancellare</legend>";
			my $db_path=DBFunctions::percorsoDBFilms;
			my $parser=XML::LibXML->new();
			my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
			my $root=$doc->getDocumentElement;
			my @films = $root->findnodes("/database/films/film");
			print"<label for=\"filmSelezionato\">Seleziona film:</label>
				  <select id=\"filmSelezionato\" name=\"filmSelezionato\">";
			print"<option class=\"placeholder\" value=\'\'>--Seleziona un film--</option>";
			foreach my $film (@films){
				$filmID = $film->getAttribute("id");
				$filmTitolo = $film->getElementsByTagName("titolo");
				print "<option value=\"$filmID\" > $filmTitolo </option>\n";
			}
			print "</select>";
			if(defined($errselezione)){
				print "<span id=\"errselezione\">$errselezione</span>";
			}
			print "<input type=\"submit\" value=\"Cancella film\" />
		</fieldset>
	</form>";
}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
