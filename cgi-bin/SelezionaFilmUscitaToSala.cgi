#!/usr/bin/perl -w
use CGI;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib './perl/modules/';
use PageSkeleton;
use DBFunctions;
use FilmFormControl;
print "Content-Type: text/html\n\n";

;
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print "<script type=\"text/javascript\" src=\"../public_html/javascript/controlliSpostamentoUscitaToSala.js\"></script>";
my $nomePagina = "Seleziona film da spostare in sala - Amministrazione - InstaFilm";
my $description = "Pagina per selezionare un film da mettere in sala";
my $keyword = "Film, Cinema, InstaFilm, Film in sala";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
print "<body onload=\" ridimensionamentoPagina(); caricamento();\">";
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> <a href=\"InserisciNuovoFilmSala.cgi\">Inserisci film in sala</a> <span class=\"breadcrumb\">-&gt;</span> "."Seleziona film da spostare in sala";
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
	my $errincasso = $session->param("errIncasso");
	my $errrecensione = $session->param("errRecensione");
	my $errval = $session->param("errValutazione");
	my $errselezione = $session->param("errSelezione");
	my $recensione = $session->param("recensione") || undef;
	my $val = $session->param("ValutazioneFilm") || undef;
	my $incasso = $session->param("incasso") || undef;
	print
	"<h1>Sposta film in sala</h1>
	<form id=\"formSelez\" action=\"perl/SpostaDaInUscitaAInSala.cgi\" method=\"post\" onsubmit=\" return validaForm();\">
		<fieldset>
			<legend>Seleziona film da spostare (i campi contrassegnati con <span class=\"obbligatorio\">*</span> sono obbligatori)</legend>";
			my $db_path=DBFunctions::percorsoDBFilms;
			my $parser=XML::LibXML->new();
			my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
			my $root=$doc->getDocumentElement;
			my @films = $root->findnodes("/database/filmsProssimamente/filmProssimamente");
			print"<label for=\"filmSelezionato\">Seleziona film:<span class=\"obbligatorio\">*</span></label>
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
			print "</fieldset>
				<fieldset>
				<legend>Inserisci i dati mancanti:</legend>";
				FilmFormControl::incasso($errincasso, $incasso);
				FilmFormControl::recensione($errrecensione, $recensione);
				FilmFormControl::valutazione($errval, $val);
			print "<input type=\"submit\" value=\"Invio\" id=\"invioSelez\" />
		</fieldset>
	</form>";
}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
