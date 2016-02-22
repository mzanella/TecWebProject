#!/usr/bin/perl -w
use CGI;
use XML::LibXML;
use XML::LibXSLT;
use lib './perl/modules/';
use PageSkeleton;
use Template;
use DBFunctions;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
print "Content-Type: text/html\n\n";
my $nomePagina = "Tutti i film";
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print "<script type=\"text/javascript\" src=\"../public_html/javascript/ricerca.js\"></script>";

my $nomePagina = "Tutti i film - InstaFilm";
my $description = "Elemnco di tutti i film già recensiti da sito";
my $keyword = "Recensione, Elenco di film, Film, Cinema, InstaFilm";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
print "<body onload=\"ridimensionamentoPagina(); caricamento();\">";
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb("Tutti i film");
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
print qq{
<h1>Tutti i film</h1>
<form id="ricercaForm" method="get" action="TuttiIFilm.cgi" >
	<fieldset>
		<legend>Ricerca film per titolo o genere</legend>
		<label for="ricerca">Cerca:</label>
		<input type="text" id="ricerca" name="ricerca" />
		<input type="submit" value="Cerca" id="btnCerca"/>
	</fieldset>
</form>};
my $session = CGI::Session->load() or die $!;
my $SID = $session->id();
my $query = CGI->new();

my $ric = $query->param("ricerca") || "";

my $db_path=DBFunctions::percorsoDBFilms;
my $parser=XML::LibXML->new();
my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
my $root=$doc->getDocumentElement ;
my @films;
if ($ric eq ""){
	@films = $root->findnodes("/database/films/film");
} else{
	@films = $root->findnodes("/database/films/film[contains(titolo/text(), \"$ric\")]
		| /database/films/film[contains(genere/text(), \"$ric\")]");
} # | /database/films/film[valutazioneSito/text()=\"$ric\"]");
if (!@films){
	print "<p>La tua ricerca non ha prodotto alcun risultato</p>";
} else {
	my @fimsDaMostrare;
	foreach my $film (@films){

		my $fa = $film->getElementsByTagName("locandina")->pop;
	 	$id = $film->getAttribute("id");
		$alt = $fa->getAttribute("alt");
	 	$locandina = $fa->getAttribute("src");
	 	$titolo = $film->getElementsByTagName("titolo");
	 	$durata = $film->getElementsByTagName("durata");
	 	$anno = $film->getElementsByTagName("annoProduzione");
	 	$regia = $film->getElementsByTagName("regia");
	 	$attori = $film->getElementsByTagName("attori");
	 	$genere = $film->getElementsByTagName("genere");
		push(@filmsDaMostrare, {tipologia => "completo",
								id => $id,
								locandina => $locandina,
								alt => $alt,
								titolo => $titolo,
								durata => $durata,
								anno => $anno,
								regia => $regia,
								attori => $attori,
								genere => $genere})
	}

	my %data = (films => \@filmsDaMostrare);
	my $templ = Template->new;
	$templ->process('Templates/templateListaFilm.tt', \%data) || die "Template process failed: ", $templ->error(), "\n";
}
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
