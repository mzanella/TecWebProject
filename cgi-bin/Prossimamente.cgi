#!/usr/bin/perl -w
use CGI;
use lib './perl/modules/';
use PageSkeleton;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use Template;
use DBFunctions;
print "Content-Type: text/html\n\n";
PageSkeleton::printDocType();
my $nomePagina = "Prossimamente - InstaFilm";
my $description = "Elenco di tutti i film in uscita";
my $keyword = "Film in uscita, Prossimamente al Cinema, Elenco di film, Film, Cinema, InstaFilm";
PageSkeleton::printHead($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb("Prossimamente");
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
print "<h1>Prossimamente</h1>";
my $db_path=DBFunctions::percorsoDBFilms;
my $parser=XML::LibXML->new();
my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
my $root=$doc->getDocumentElement ;
my @films = $root->findnodes("/database/filmsProssimamente/filmProssimamente");
my @fimsDaMostrare;
foreach my $film (@films){

	my $fa = $film->getElementsByTagName("locandina")->pop;
 	$id = $film->getAttribute("id");
 	$locandina = $fa->getAttribute("src");
 	$alt = $fa->getAttribute("alt");
 	$titolo = $film->getElementsByTagName("titolo");
 	$durata = $film->getElementsByTagName("durata");
 	$anno = $film->getElementsByTagName("annoProduzione");
 	$regia = $film->getElementsByTagName("regia");
 	$attori = $film->getElementsByTagName("attori");
 	$genere = $film->getElementsByTagName("genere");
	push(@filmsDaMostrare, {tipologia => "prossimamente",
							id => $id,
							alt => $alt,
							locandina => $locandina,
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
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
