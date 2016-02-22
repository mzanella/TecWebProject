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
my $commento = DBFunctions::inputControl(Encode::decode_utf8($query->param("commento")));
my $idFilm = $query->param("idFilm");

my %errors;
my $error=0;

my $errorstring=undef;
if (length($commento)<10){
	$errorstring="Errore: commento troppo corto";
	$error=1;
}

$errors{"errCommento"} = $errorstring;
$errors{"commento"} = $commento;

if ($error>0){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	foreach my $key(keys %errors) {
		my $value = $errors{$key};
		$session->param($key, $value);
	}
	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../filmProssimamente.cgi?id=$idFilm");
}
else{
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	my $email = $session->param("utenteEmail");
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	DBFunctions::aggiungiCommentoProssimamente($email, $commento, $idFilm);
	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../filmProssimamente.cgi?id=$idFilm");
}
