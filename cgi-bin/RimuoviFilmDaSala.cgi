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
my $nomePagina = "Rimuovi film dalla sala - InstaFilm";
PageSkeleton::printHeadStart();
print
"	<script type=\"text/javascript\" src=\"../public_html/javascript/selezionaFilm.js\"></script>";
my $nomePagina = "Rimozione film- Amministrazione - InstaFilm";
my $description = "Rimuovi un film";
my $keyword = "Film, Cinema, InstaFilm, Film in sala";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> "."Rimuovi film dalla sala";
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
	my $errselezione = $session->param("errSelezione");
	print
	"<h1>Rimuovi film dalla sala $errselezione</h1>
	<form id=\"frmFilm\" action=\"perl/rimozioneDaSala.cgi\" method=\"post\" onsubmit=\"return validaForm();\">
		<fieldset>
			<legend>Film da rimuovere dalla sala</legend>";
			my $db_path=DBFunctions::percorsoDBFilms;
			my $parser=XML::LibXML->new();
			my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
			my $root=$doc->getDocumentElement ;
			my @films = $root->findnodes("/database/films/film[inSala=\"si\"]");
			print"<label for=\"filmDaRimuovereDaInSala\">Seleziona film:</label>
				  <select id=\"filmDaRimuovereDaInSala\" name=\"filmDaRimuovereDaInSala\">";
			print"<option class=\"placeholder\" selected disabled hidden value=\'\'>--Seleziona un film--</option>";
			foreach my $film (@films){
				$filmID = $film->getAttribute("id");
				$filmTitolo = $film->getElementsByTagName("titolo");
				print "<option value=\"$filmID\" > $filmTitolo </option>";
			}
			print "</select>";
			if(defined($errselezione)){
				print "<span id=\"errselezione\">$errselezione</span>";
			}
			print "
			<input type=\"submit\" value=\"Rimuovi film dalla sala\" />
		</fieldset>
	</form>";
}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
