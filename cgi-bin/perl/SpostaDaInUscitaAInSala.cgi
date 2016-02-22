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
	$input{$name}=DBFunctions::inputControl(Encode::decode_utf8($query->param($name));
}

my %errors;
my $error=0;

$input{"selezione"}=DBFunctions::inputControl(Encode::decode_utf8($query->param("filmSelezionato")));
my @return = FilmFormControl::controlloSelezione(\%input);
$errors{'errSelezione'}=$return[0];
$error=$error+$return[1];

@return = FilmFormControl::controlloRecensione(\%input);
$errors{'errRecensione'}=$return[0];
$error=$error+$return[1];

@return = FilmFormControl::controlloIncasso(\%input);
$errors{'errIncasso'}=$return[0];
$error=$error+$return[1];


@return = FilmFormControl::controlloValutazione(\%input);
$errors{'errValutazione'}=$return[0];
$error=$error+$return[1];

if ($error>0){
	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	$session->expire("+1h");

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
	print $session->header(-location=>"../SelezionaFilmUscitaToSala.cgi");
} else {
	
	$input{'filmSelezionato'}=DBFunctions::inputControl(Encode::decode_utf8($query->param('filmSelezionato')));
	my $rec=DBFunctions::inputControl(Encode::decode_utf8($query->param('recensione')));
	my $inc=DBFunctions::inputControl(Encode::decode_utf8($query->param('incasso')));
	my $val=DBFunctions::inputControl(Encode::decode_utf8($query->param('ValutazioneFilm')));
	my $db_path=DBFunctions::percorsoDBFilms;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement ;
	my $query='/database/filmsProssimamente/filmProssimamente[@id='.$input{"filmSelezionato"}.']';
	my $film=$root->find($query) || die "film non trovato";
	my $f = $film->pop();
	my $fa = $f->getElementsByTagName("locandina")->pop;
	$query="/database/filmsProssimamente";
	$film=$root->find($query) || die "film non trovato";
	my $fr = $film->pop();
	$fr->removeChild($f);
	open(OUT, ">", $db_path) || die("impossibile aprire il file");
	print OUT $doc->toString;
	close(OUT);
	my @par;
	$par[0] = $f->getElementsByTagName("titolo");
	$par[1] = $f->getElementsByTagName("dataUscita");
	$par[2] = $f->getElementsByTagName("paese");
	$par[3] = $f->getElementsByTagName("durata");
	$par[4] = $f->getElementsByTagName("trama");
	$par[5] = $f->getElementsByTagName("genere");
	$par[6] = $f->getElementsByTagName("annoProduzione");
	$par[7] = $f->getElementsByTagName("attori");
	$par[8] = $f->getElementsByTagName("regia");

	my $newid = DBFunctions::aggiungiFilm($fa->getAttribute("src"),
							  $fa->getAttribute("alt"),
							  $par[0],
							  $par[1],
							  $par[2],
							  $par[3],
							  $par[4],
							  $inc,$val,$rec,
							  $par[5],
							  $par[6],
							  "si",
							  $par[7],
							  $par[8]);	

	my $oldid = $input{'selezione'};

	my $oldpath = DBFunctions::percorsoCommentiFilmProssimamente."$oldid.xml";
	my $newpath = DBFunctions::percorsoCommentiFilm."$newid.xml";

	#print "Content-Type: text/html\n\n";
	#print $oldpath;
	open ( my $filein, "<$oldpath" ) or die "$!";
    #flock($filein, LOCK_EX) or die "Could not lock 'IN' - $!";
    open ( my $fileout, ">$newpath" ) or die "$!";
    #flock($fileout, LOCK_EX) or die "Could not lock 'OUT' - $!";
	while (my $row = <$filein>) {
		chomp $row;
		print $fileout $row;
	}

	close $filein;
	close $fileout;

	my $session = CGI::Session->load() or die $!;
	my $SID = $session->id();
	$session=FilmFormControl::rigeneraSessione($session);
	my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
	$session->header();
	print $session->header(-location=>"../ConfermaSpostamento.cgi");
}




