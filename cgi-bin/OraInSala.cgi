#!/usr/bin/perl -w
use CGI;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use Template;
use lib './perl/modules/';
use PageSkeleton;
use DBFunctions;
 use HTML::Entities;
print "Content-Type: text/html\n\n";
PageSkeleton::printDocType();
my $nomePagina = "Ora in sala - InstaFilm";
my $description = "Elenco di tutti i film in sala";
my $keyword = "Film in sala, ora al Cinema, Elenco di film, Film, Cinema, InstaFilm";
PageSkeleton::printHead($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb($nomePagina);
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
print "<h1>Ora In Sala</h1>";
my $db_path=DBFunctions::percorsoDBFilms;
my $parser=XML::LibXML->new();
my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
my $root=$doc->getDocumentElement ;
my @films = $root->findnodes("/database/films/film[inSala=\"si\"]");
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
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
