#!/usr/bin/perl -w
use CGI;
use CGI::Session();
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib 'modules/';
use DBFunctions;
use FilmFormControl;
#print "Content-Type: text/html\n\n";

my $query = CGI->new();
my %input;
my @names = $query->param();
foreach $name (@names) {
	$input{$name}=$query->param($name);
}
$input{"selezione"}=$query->param("filmSelezionato");
my @return = FilmFormControl::controlloSelezione(\%input);
if ($return[1]==1){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	$session->expire("+1h");
	$session->param("errSelezione", $return[0]);
	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../CancellaFilm.cgi");
} else {
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	$session->expire("+1h");
	my $db_path=DBFunctions::percorsoDBFilms;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my $query='/database/films/film[@id='.$input{"filmSelezionato"}.']';
	my $film=$root->find($query) || die "film non trovato";
	my $f = $film->pop();
	$query="/database/films";
	$film=$root->find($query) || die "film non trovato";
	my $fa = $film->pop();
	$fa->removeChild($f);
	open(OUT, ">", $db_path) || die("impossibile aprire il file");
	print OUT $doc->toString;
	close(OUT);
	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../ConfermaRimozione.cgi");
}