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
#print "Content-Type: text/html\n\n";

my $query = CGI->new();
my %input;
my @names = $query->param();
foreach $name (@names) {
	$input{$name}=DBFunctions::inputControl(Encode::decode_utf8($query->param($name)));
}

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
	print $session->header(-location=>"../RecensisciNuovoFilm.cgi");
} else {
	$src = FilmFormControl::saveImage(\%input, $query);
	$giorno=$input{'giornoUscita'};
	if ($giorno<10){
		$giorno="0".$giorno;
	}
	$mese=$input{'meseUscita'};
	if ($mese<10){
		$mese="0".$mese;
	}
	$dataUscita=$input{'annoUscita'}."-".$mese."-".$giorno;

	DBFunctions::aggiungiFilm($input{'locandina'}, $input{'locDescr'}, $input{'titolo'}, $dataUscita, 
		$input{'paeseDiProduzione'}, $input{'durata'}, $input{'trama'}, $input{'incasso'}, $input{'ValutazioneFilm'},
		$input{'recensione'}, $input{'genere'}, $input{'annoProduzione'}, "no", $input{'attori'}, $input{'regia'}, );

	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);

	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../ConfermaRecensione.cgi");
}
