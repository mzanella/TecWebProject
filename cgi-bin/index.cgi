#!/usr/bin/perl -w
use CGI;
use lib './perl/modules/';
use PageSkeleton;
use utf8;
use Encode;
use XML::LibXSLT;
binmode(STDOUT, ":utf8");
print "Content-Type: text/html\n\n";
my $nomePagina = "Home - InstaFilm";
my $description = "Prima pagina del sito InstaFilm.  Contiene gli ultimi 2 film inseriti,
gli ultimi due film inseriti con valutazione massima e gli ultimi due film inseriti in uscita.";
my $keyword = "Film, Cinema, Ultime uscite, InstaFilm, Prossimamente al cinema";
PageSkeleton::printDocType();
PageSkeleton::printHead($nomePagina, $description, $keyword);
PageSkeleton::printBodyStart();
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb($nomePagina);
PageSkeleton::printLoginBar();
PageSkeleton::printContentStart();
#qui va il contenuto
my $parser = XML::LibXML->new();
my $xslt = XML::LibXSLT->new();
my $source = $parser->parse_file(DBFunctions::percorsoDBFilms);
my $style_doc = $parser->parse_file(DBFunctions::percorsoTrasformataUltimiFilm);
my $stylesheet = $xslt->parse_stylesheet($style_doc);
my $results = $stylesheet->transform($source);
my $s = $results->toString;
$s =~ s/\<\?xml version=\"1.0\"\?\>//;
print $s;
#fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();
