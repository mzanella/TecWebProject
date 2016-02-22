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
use Digest::MD5;
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

my $errorstring=undef;
if (length($input{'email'})==0){
	$errorstring="Errore: email è un campo obbligatorio";
	$error=1;
} elsif (!($input{'email'}=~/^([\w\-\+\.]+)@([\w\-\+\.]+)\.([\w\-\+\.]+)$/)){
	$errorstring="Errore: email non valida";
	$error=1;
} else {
	my $db_path=DBFunctions::percorsoDBUtenti;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my $query="/database/utenti/utente[email=\"$input{email}\"]";
	my $nUsers=$doc->findvalue("count($query)") || 0;
	if ($nUsers>0){
		$errorstring="Errore: email già presente";
		$error=1;
	}
}
$errors{'errEmail'}=$errorstring;

$errorstring=undef;
if (length($input{'password'})==0){
	$errorstring="Errore: password è un campo obbligatorio";
	$error=1;
} elsif (length($input{'password'})<8){
	$errorstring="Errore: password troppo corta";
	$error=1;
}
$errors{'errPassword'}=$errorstring;

$errorstring=undef;
if (length($input{'passwordConferma'})==0){
	$errorstring="Errore: password di conferma è un campo obbligatorio";
	$error=1;
}
elsif (!($input{'passwordConferma'}=~/^$input{'password'}/)){
	$errorstring="Errore: password e password di conferma differenti";
	$error=1;
}
$errors{'errPasswordConferma'}=$errorstring;

$errorstring=undef;
if (length($input{'nome'})==0){
	$errorstring="Errore: nome è un campo obbligatorio";
	$error=1;
}
$errors{'errNome'}=$errorstring;

$errorstring=undef;
if (length($input{'cognome'})==0){
	$errorstring="Errore: cognome è un campo obbligatorio";
	$error=1;
}
$errors{'errCognome'}=$errorstring;

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time);
$errorstring=undef;
if (length($input{'giorno'})==0 || length($input{'mese'})==0 || length($input{'anno'})==0){
	$errorstring="Errore: data non completa";
	$error=1;
} elsif (!($input{'giorno'}=~/^[0-9]*$/)){
	$errorstring="Errore: giorno contiene caratteri non validi";
	$error=1;
} elsif (!($input{'mese'}=~/^[0-9]*$/)){
	$errorstring="Errore: mese contiene caratteri non validi";
	$error=1;
} elsif (!($input{'anno'}=~/^[0-9]*$/)){
	$errorstring="Errore: anno contiene caratteri non validi";
	$error=1;
} elsif ($input{'giorno'}>31){
	$errorstring="Errore: giorno non valido";
	$error=1;
} elsif ($input{'mese'}>12){
	$errorstring="Errore: mese non valido";
	$error=1;
} elsif ($input{'anno'}>($year+1900-6)||$input{'anno'}<($year+1900-120)){
	$errorstring="Errore: anno non valido";
	$error=1;
} elsif ($input{'giorno'}>30 and ($input{'mese'}==11 || $input{'mese'}==4 || $input{'mese'}==6 || $input{'mese'}==9)){
	$errorstring="Errore: data non valida";
	$error=1;
} elsif ($input{'giorno'}>28 and $input{'mese'}==2 and $input{'anno'}%4!=0){
	$errorstring="Errore: data non valida";
	$error=1;
} elsif ($input{'giorno'}>29 and $input{'mese'}==2 and $input{'anno'}%4==0){
	$errorstring="Errore: data non valida";
	$error=1;
}
$errors{'errDataDiNascita'}=$errorstring;

if ($error==1){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session->close();
	$session->delete();
	$session->flush();

	my $session = CGI::Session->new();
	$session->expire("500");
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
	print $session->header(-location=>"../Registrati.cgi");
} elsif ($error==0){
	$giorno=$input{'giorno'};
	if ($giorno<10){
		$giorno="0".$giorno;
	}
	$mese=$input{'mese'};
	if ($mese<10){
		$mese="0".$mese;
	}

	my $ctx = Digest::MD5->new;
	$ctx->add($input{'password'});
	my $digest = $ctx->b64digest;

	$dataDiNascita=$input{'anno'}."-".$mese."-".$giorno;

	my $db_path=DBFunctions::percorsoGeneriFilm;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my $query="/generi/genere";
	my @generi = $doc->findnodes($query);
	my $generiPreferiti = "<generiPreferiti>";
	foreach $genere (@generi){
		$genere = $genere->findvalue(".");
		foreach $key (keys %input){
			if ($key eq $genere){
				$generiPreferiti = $generiPreferiti."<genere>".$genere."</genere>";
			}
		}
	}
	$generiPreferiti = $generiPreferiti."</generiPreferiti>";

	DBFunctions::aggiungiUtente($input{'nome'}, $input{'cognome'}, $dataDiNascita, $input{'email'}, $digest, $generiPreferiti);

	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session->close();
	$session->delete();
	$session->flush();

	$session = CGI::Session->new();
	$session->expire("+1h");
	$session->param("utenteEmail", $input{'email'});
	$session->param("utenteNome", $input{'nome'});
	$session->param("utenteAdmin", "no");

	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../index.cgi");
}
