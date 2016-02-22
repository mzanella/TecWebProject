#!/usr/bin/perl -w
use CGI;
use CGI::Session();
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Unicode::String; 
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib 'modules/';
use FilmFormControl;
use DBFunctions;

my $query = CGI->new();
my %input;
my @names = $query->param();
foreach $name (@names) {
	$input{$name}=DBFunctions::inputControl(Encode::decode_utf8($query->param($name)));
}
$input{"selezione"}=DBFunctions::inputControl($query->param("filmSelezionato"));

my %errors;
my $error=0;

my @return = FilmFormControl::controlloTitolo(\%input);
$errors{'errTitolo'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloPaese(\%input);
$errors{'errPaese'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloDurata(\%input);
$errors{'errDurata'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloRegia(\%input);
$errors{'errRegia'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloAttori(\%input);
$errors{'errAttori'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloTrama(\%input);
$errors{'errTrama'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloData(\%input);
$errors{'errDataUscita'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloRecensione(\%input);
$errors{'errRecensione'}=$return[0];
$error=$error+$return[1];


my @return = FilmFormControl::controlloValutazione(\%input);
$errors{'errValutazione'}=$return[0];
$error=$error+$return[1];

my @return = FilmFormControl::controlloIncasso(\%input);
$errors{'errIncasso'}=$return[0];
$error=$error+$return[1];

@return = FilmFormControl::controlloDescrizioneLoc(\%input);
$errors{'errDescrLoc'}=$return[0];
$error=$error+$return[1];

if ($error>0){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	foreach my $key(keys %errors) {
		my $value = $errors{$key};
		$session->param($key, $value);
	}
	foreach my $key(keys %input) {
		my $value = $input{$key};
		$session->param($key, $value);
	}
	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../ModificaFilm.cgi");
} else {
	my $src=FilmFormControl::saveImage(\%input, $query);
	$alt=$query->param("locDescr");

	$giorno=$input{'giornoUscita'};
	if ($giorno<10){
		$giorno="0".$giorno;
	}
	$mese=$input{'meseUscita'};
	if ($mese<10){
		$mese="0".$mese;
	}
	$dataUscita=$input{'annoUscita'}."-".$mese."-".$giorno;

	my $db_path=DBFunctions::percorsoDBFilms;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	$query='/database/films/film[@id='.$input{"id"}."]";
	my $film=$root->find($query) || die "film non trovato";
	my $f = $film->pop();
	my $fa = $f->getElementsByTagName("locandina")->pop;
	$fa->setAttribute("src", $src);
	$fa->setAttribute("alt", $alt);
	my @t = $f->findnodes("titolo/text()");
	$t[0]->setData($input{"titolo"});
	my $giorno=$input{'giornoUscita'};
	if ($giorno<10){
		$giorno="0".$giorno;
	}
	my $mese=$input{'meseUscita'};
	if ($mese<10){
		$mese="0".$mese;
	}

	my $dataUscita=$input{'annoUscita'}."-".$mese."-".$giorno;
	@t = $f->findnodes("dataUscita/text()");
	$t[0]->setData($dataUscita);
	@t = $f->findnodes("paese/text()");
	$t[0]->setData($input{"paeseDiProduzione"});
	@t = $f->findnodes("durata/text()");
	$t[0]->setData($input{"durata"});
	@t = $f->findnodes("trama/text()");
	$t[0]->setData($input{"trama"});
	@t = $f->findnodes("incasso/text()");
	$t[0]->setData($input{"incasso"});
	@t = $f->findnodes("valutazioneSito/text()");
	$t[0]->setData($input{"ValutazioneFilm"});
	@t = $f->findnodes("recensione/text()");
	$t[0]->setData($input{"recensione"});
	@t = $f->findnodes("genere/text()");
	$t[0]->setData($input{"genere"});
	@t = $f->findnodes("annoProduzione/text()");
	$t[0]->setData($input{"annoProduzione"});
	@t = $f->findnodes("attori/text()");
	$t[0]->setData($input{"attori"});
	@t = $f->findnodes("regia/text()");
	$t[0]->setData($input{"regia"});

	open(OUT, ">", "$db_path") || die("impossibile aprire il file");
	print OUT $doc->toString;
	close(OUT);

	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);

	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../ConfermaModifica.cgi");
}
