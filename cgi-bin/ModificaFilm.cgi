#!/usr/bin/perl -w
use CGI;
use CGI::Session();
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib 'perl/modules/';
use PageSkeleton;
use FilmFormControl;
use DBFunctions;
use Template;

print "Content-Type: text/html\n\n";

PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print
"	<script type=\"text/javascript\" src=\"../public_html/javascript/controlliInserimentoFilmInSala.js\"></script>";
my $nomePagina = "Modifica film - Amministrazione - InstaFilm";
my $description = "Pagina per la modifica di un film già recensito";
my $keyword = "Film, Cinema, InstaFilm, Modifica film";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
print "<body onload=\" ridimensionamentoPagina(); caricamento();\">";
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
#creazione breadcrumb
$nomeBC="<a href=\"Amministrazione.cgi\">Amministrazione</a> <span class=\"breadcrumb\">-&gt;</span> <a href=\"SelezionaFilmDaModificare.cgi\">Seleziona film da modificare</a> <span class=\"breadcrumb\">-&gt;</span> "."Modifica film";
PageSkeleton::printBreadCrumb($nomeBC);
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
my $cgi = new CGI;
my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
my $session = load CGI::Session();
if (DBFunctions::controlAdmin($session->param("utenteEmail")) == 0){
	print "<h1>Accesso negato</h1>
		   <p>Sezione riservata solamente agli amministratori del sito web.</p>
		   <p>Se sei un amministratore devi eseguire il <a href=\"Login.cgi\">login</a> prima di poter accere.</p>";
} else  {
	#recupero parametri per controllo degli errori e per risettare i campi come messo dall'utente
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();

	my $query = CGI->new();
	my %input;
	$input{'film'}=$query->param('film');
	if (!defined($session->param("id")) && !defined($input{"film"})) {
		print "<h1>Errore</h1><p>Devi prima <a href=\"SelezionaFilmDaModificare.cgi\">selezionare un film</a>
		 per poterlo poi modificare</p>";
	} else {
		my $db_path=DBFunctions::percorsoDBFilms;
		my $parser=XML::LibXML->new();
		my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
		my $root=$doc->getDocumentElement ;
		my $id;
		if (defined($input{"film"})){
			$id = $input{"film"};
		} else {
			$id = $session->param("id");
		}

		$query='/database/films/film[@id='.$id."]";
		my $film=$root->find($query) || die "film non trovato";
		my $f = $film->pop();
		my $fa = $f->getElementsByTagName("locandina")->pop;

		if (!defined($session->param("id"))){
			$session->param("id", $input{"film"});
		}

		my $nomePagina="Modifica film";
		my $errtitolo = $session->param("errTitolo");
		my $errpaese = $session->param("errPaese");
		my $errdurata = $session->param("errDurata");
		my $errregia = $session->param("errRegia");
		my $errattori = $session->param("errAttori");
		my $errtrama = $session->param("errTrama");
		my $errdatauscita = $session->param("errDataUscita");
		my $errrecensione = $session->param("errRecensione");
		my $errval = $session->param("errValutazione");
		my $errincasso = $session->param("errIncasso");
		my $errDescrLoc = $session->param("errDescrLoc");
		my $src = $session->param("src") || $fa->getAttribute("src");
		my $titolo = $session->param("titolo") || $f->getElementsByTagName("titolo");
		(my $giornoUscita, my $meseUscita, my $annoUscita) = ($session->param("giornoUscita"),$session->param("meseUscita"),
		$session->param("annoUscita")) || split('-',$f->getElementsByTagName("dataUscita"));
		my $paese = $session->param("paeseDiProduzione") || $f->getElementsByTagName("paese");
		my $durata = $session->param("durata" )	|| $f->getElementsByTagName("durata");
		my $incasso = $session->param("incasso" ) || $f->getElementsByTagName("incasso");
		my $tempval = $f->getElementsByTagName("valutazioneSito");
		my $val = $session->param("ValutazioneFilm") || $tempval;
		my $recensione = $session->param("recensione" ) || $f->getElementsByTagName("recensione");
		my $trama = $session->param("trama" ) || $f->getElementsByTagName("trama");
		my $gen = $session->param("genere" ) || $f->getElementsByTagName("genere");
		my $annoProduzionetemp = $f->getElementsByTagName("annoProduzione");
		my $annoProduzione = $session->param("annoProduzione") || $annoProduzionetemp;
		my $insala = $session->param("inSala") || $f->getElementsByTagName("inSala");
		my $attori = $session->param("attori" ) || $f->getElementsByTagName("attori");
		my $regia = $session->param("regia") || $f->getElementsByTagName("regia");
		my $incasso = $session->param("incasso") || $f->getElementsByTagName("incasso");
		my $locdescr = $session->param("locDescr") || $fa->getAttribute("alt");

		print
		"<h1>Modifica film</h1>
		<form id=\"frmInsFilm\" action=\"perl/controlliModificaFilm.cgi\" method=\"post\"
		onsubmit=\"return validaForm();\">
			<fieldset>
				<legend>Film da modificare</legend>";
				FilmFormControl::titolo($errtitolo, $titolo);
				print "
				<input type=\"hidden\" name=\"id\" value=\"$id\" />";
				print "
				<label for=\"locandina\">Inserisci il percorso o l'url della locandina:</label>
				<input type=\"text\" name=\"locandina\" id=\"locandina\" value=\"$src\" />";
				FilmFormControl::descrizione($errDescrLoc, $locdescr);
				FilmFormControl::paeseDiProduzione($errpaese, $paese);
				FilmFormControl::durata($errdurata, $durata);
				FilmFormControl::annoDiProduzione($annoProduzione);
				FilmFormControl::dataUscita($errdatauscita, $giornoUscita, $meseUscita, $annoUscita);
				FilmFormControl::incasso($errincasso, $incasso);
				FilmFormControl::regia($errregia, $regia);
				FilmFormControl::attori($errattori, $attori);
				FilmFormControl::genere($gen);
				FilmFormControl::trama($errtrama, $trama);
				FilmFormControl::recensione($errrecensione, $recensione);
				FilmFormControl::valutazione($errval, $val);
				print "
				<input type=\"submit\" value=\"Modifica film\" />
			</fieldset>
		</form>";
	}
}

#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();


#print $session->header(-location=>"../ModificaFilm.cgi");
