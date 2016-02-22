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
$input{"selezione"}=$query->param("filmDaRimuovereDaInSala");
my @return = FilmFormControl::controlloSelezione(\%input);
if ($return[1]==1){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	$session->param("errSelezione", $return[0]);
	$session->flush();
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../RimuoviFilmDaSala.cgi");
} else {
	$input{'filmDaRimuovereDaInSala'}=$query->param('filmDaRimuovereDaInSala');
	my $db_path=DBFunctions::percorsoDBFilms;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my $query='/database/films/film[@id='.$input{"filmDaRimuovereDaInSala"}."]/inSala/text()";
	my $film=$root->find($query) || die "film non trovato";
	foreach my $f ($film->get_nodelist){
		$f->setData('no');
	}
	open(OUT, ">$db_path") || die("impossibile aprire il file");
	print OUT $doc->toString;
	close(OUT);
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	print $session->header(-location=>"../ConfermaRimozioneDaInSala.cgi");
}

