#!/usr/bin/perl -w
use CGI;
use CGI::Session;
use XML::LibXML;
use XML::LibXSLT;
use lib './perl/modules/';
use PageSkeleton;
use DBFunctions;
use Template;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;

my $session = CGI::Session->load() or die $!;
my $SID = $session->id();
my $query = CGI->new();
my %input;
my @names = $query->param();
foreach $name (@names) {
	$input{$name}=$query->param($name);
}
if(defined($input{"id"})){
	print "Content-Type: text/html\n\n";
	my $db_path=DBFunctions::percorsoDBFilms;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my @films = $root->findnodes("/database/films/film[\@id=\"$input{\"id\"}\"]");
	my $film = @films[0];
	my $fa = $film->getElementsByTagName("locandina")->pop;
	#recupero info da passare al template
	$id = $film->getAttribute("id");
	$locandina = $fa->getAttribute("src");
	$alt = $fa->getAttribute("alt");
	$titolo = $film->getElementsByTagName("titolo");
	$dataUscita = $film->getElementsByTagName("dataUscita");
	$paese = $film->getElementsByTagName("paese");
	$durata = $film->getElementsByTagName("durata");
	$anno = $film->getElementsByTagName("annoProduzione");
	$regia = $film->getElementsByTagName("regia");
	$attori = $film->getElementsByTagName("attori");
	$genere = $film->getElementsByTagName("genere");
	$trama = $film->getElementsByTagName("trama");
	$incasso = $film->getElementsByTagName("incasso");
	$valutazioneSito = $film->getElementsByTagName("valutazioneSito");
	$recensione = $film->getElementsByTagName("recensione");

	my $nomePagina = $titolo."- film - InstaFilm";
	my $description = "Pagina del film: $titolo";
	my $keyword = "$titolo, Film, Cinema, InstaFilm, $genere ";
	PageSkeleton::printDocType();
	PageSkeleton::printHead($nomePagina, $description, $keyword);
	PageSkeleton::printBodyStart();
	PageSkeleton::printHeader();
	PageSkeleton::printNav($nomePagina);
	PageSkeleton::printBreadCrumb("<a href=\"TuttiIFilm.cgi\">Tutti i Film</a> -> $titolo");
	PageSkeleton::printLoginBar($id);
	PageSkeleton::printContentStart();

	my $cgi = new CGI;
	my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
	my $session = CGI::Session->load();
	my $SID = $session->id();

	my $errCommento = $session->param("errCommento");
	my $commento = $session->param("commento");
	my $loggato=$session->param("utenteEmail");
	#controllo Login per poter commentare
	if(!defined($loggato)){
		$loggato=0;
	}
	else{
		$loggato=1;
	}

	#salvataggio info in %data
	my %data = (id => $id,
				locandina => $locandina,
				alt => $alt,
				titolo => $titolo,
				dataUscita => $dataUscita,
				paese => $paese,
				durata => $durata,
				anno => $anno,
				regia => $regia,
				attori => $attori,
				genere => $genere,
				trama => $trama,
				incasso => $incasso,
				valutazioneSito => $valutazioneSito,
				recensione => $recensione,
				idFilm => $id,
				commento => $commento,
				errCommento => (defined $errCommento),
				errMessage => $errCommento,
				loggato => $loggato);

	my $templ = Template->new;
	$templ->process('Templates/filmTemplate.tt', \%data) || die "Template process failed: ", $templ->error(), "\n";
	my $parser = XML::LibXML->new();
	my $xslt = XML::LibXSLT->new();
	my $source = $parser->parse_file(DBFunctions::percorsoCommentiFilm."$id.xml");
	my $style_doc = $parser->parse_file(DBFunctions::percorosoTrasformataCommenti);
	my $stylesheet = $xslt->parse_stylesheet($style_doc);
	my $results = $stylesheet->transform($source);
	my $s = $results->toString;
	$s =~ s/\<\?xml version=\"1.0\"\?\>//;
	print $s;
	PageSkeleton::printContentEnd();
	PageSkeleton::printFooter();
	PageSkeleton::printBodyEnd();
	PageSkeleton::printHtmlEnd();
} else {
	$query->header();
	print $query->header(-location=>" TuttiIFilm.cgi");
}
