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
	$input{$name}=$query->param($name);
}
my $paginaProvenienza = $query->param("paginaProvenienza");
#print $paginaProvenienza;
my %errors;
my $error=0;

my $errorstring=undef;
if (length($input{'email'})==0){
	$errorstring="Errore: email non inserita";
	$error=1;
} elsif (!($input{'email'}=~/^([\w\-\+\.]+)@([\w\-\+\.]+)\.([\w\-\+\.]+)$/)){
	$errorstring="Errore: email non valida";
	$error=1;
}
 else {
	my $db_path=DBFunctions::percorsoDBUtenti;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement;
	my $query="/database/utenti/utente[email=\"$input{email}\"]";
	my $nUsers=$doc->findvalue("count($query)") || 0;
	if ($nUsers>0){
		if (length($input{'password'})==0){
			$errorstring="Errore: password non inserita";
			$error=1;
		} else {
			$query="/database/utenti/utente[email=\"$input{\"email\"}\"][1]/password";
			my $password=$doc->findvalue($query);
			my $ctx = Digest::MD5->new;
			$ctx->add($input{'password'});
			my $digest = $ctx->b64digest;
			if ($digest ne $password) {
				$errorstring="Errore: password errata";
				$error=1;
			}
		}
	}
	else {
		$errorstring="<span id=\"erroreLogin\">Errore: email non riconosciuta</span>";
		$error=1;
	}
}

$errors{'errore'}=$errorstring;

if ($error==1){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session->close();
	$session->delete();
	$session->flush();

	$session = CGI::Session->new();
	$session->expire("+1h");
	foreach my $key(keys %errors) {
		my $value = $errors{$key};
		$session->param($key, $value);
	}

	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../Login.cgi?id=$paginaProvenienza");
} elsif ($error==0){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session->close();
	$session->delete();
	$session->flush();

	$session = CGI::Session->new();
	$session->expire("+1h");
	$session->param("utenteEmail", $input{'email'});
	my $db_path=DBFunctions::percorsoDBUtenti;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement;
	my $query="/database/utenti/utente[email=\"$input{email}\"]/nome";
	my $utenteNome=$doc->findvalue($query);
	$session->param("utenteNome", $utenteNome);
	my $query="/database/utenti/utente[email=\"$input{email}\"]/admin";
	my $admin=$doc->findvalue($query);
	$session->param("utenteAdmin", $admin);
	#$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../$paginaProvenienza");

}
