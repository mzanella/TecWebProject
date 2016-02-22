#!/usr/bin/perl -w
package DBFunctions;
use CGI;
use CGI::Session();
use Fcntl;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Fcntl ':flock';
#use strict;
use File::Basename;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";

sub percorsoDBFilms {
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/DBfilms.xml";
	return $db_path;
}

sub percorsoDBUtenti {
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/DButenti.xml";
	return $db_path;
}

sub percorsoCommentiFilm {
	#Restituisce la cartella, il nome fle va concatenato
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/commenti/Films/";
	return $db_path;
}

sub percorsoGeneriFilm {
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/generi.xml";
	return $db_path;
}

sub percorsoCommentiFilmProssimamente {
	#Restituisce la cartella, il nome fle va concatenato
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/commenti/FilmsProssimamente/";
	return $db_path;
}

sub percorosoTrasformataCommenti {
	#Restituisce la cartella, il nome fle va concatenato
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/commenti/commenti.xsl";
	return $db_path;
}

sub percorsoTrasformataUltimiFilm {
	#Restituisce la cartella, il nome fle va concatenato
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/film.xsl";
	return $db_path;
}

sub percorsoLocandine {
	my $path_of_this_module = File::Basename::dirname( __FILE__ );
	my $db_path="$path_of_this_module/../../../data/database/locandine/";
	return $db_path;
}

sub inputControl {
	#$s =~ s/([^a-zA-Z\d\s:,])/\\$1/g;
	my $s=$_[0];
	$s =~ s/(&)/&amp;/g;
	$s =~ s/(<)/&lt;/g;
	$s =~ s/(>)/&gt;/g;
	$s =~ s/(#)/&#35;/g;
	$s =~ s/(!)/&#33;/g;
	$s =~ s/(")/&#34;/g;
	$s =~ s/(\$)/&#36;/g;
	$s =~ s/(')/&#39;/g;
	$s =~ s/(\/)/&#47;/g;
	$s =~ s/(\?)/&#63;/g;
	#$s =~ s/(@)/&#64;/g;
	$s =~ s/(\\)/&#92;/g;
	$s =~ s/(\|)/&#124;/g;
	$s =~ s/(~)/&#126;/g;

	return $s;
}

sub inizioAggiunta {
	my $db_path=$_[2];
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");	#parsing del file
	my $root=$doc->getDocumentElement;
	my $cat=$_[0];
	my $subcat=$_[1];
	my $query="count(/database/".$cat."/".$subcat.")";
	my $nUsers=$doc->findvalue($query);
	my $newID=0;
	if ($nUsers==0){
		$query="/database/".$cat;
	}
	else{
		$query="/database/".$cat."/".$subcat."[last()]/attribute::id";
		my $lastID=$doc->findvalue($query);
		$newID=$lastID+1;
		$query="/database/".$cat;
	}
	my @returnItems=($parser, $doc, $root, $query, $newID);
	return @returnItems;
}

sub inizioAggiuntaCommento {
	my $db_path=$_[2];
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");	#parsing del file
	my $root=$doc->getDocumentElement;
	my $cat=$_[0];
	my $subcat=$_[1];
	$query="/database/".$cat;
	my @returnItems=($parser, $doc, $root, $query);
	return @returnItems;
}

sub scriviDB {
	my $parser=$_[0];
	my $newItem=$_[1];
	my $doc=$_[2];
	my $query=$_[3];
	my $db_path=$_[4];
	my $newNodo=$parser->parse_balanced_chunk($newItem) || die("something goes wrong");
	my $node=$doc->findnodes($query)->get_node(1) || die("error:".$!);
	$node->appendChild($newNodo) || die;

	open(my $file, ">", "$db_path") || die $db_path."->".$!;
	flock($file, LOCK_EX) or die "Could not lock '$file' - $!";
	print $file $doc->toString;
	close($file);
}

sub aggiungiUtente {
	my $nome=$_[0];
	my $cognome=$_[1];
	my $dataDiNascita=$_[2];
	my $email=$_[3];
	my $password=$_[4];
	my $generiPreferiti=$_[5];

	my @returnItems=&inizioAggiunta("utenti", "utente", &percorsoDBUtenti);
	my $parser=$returnItems[0];
	my $doc=$returnItems[1];
	my $root=$returnItems[2];
	my $query=$returnItems[3];
	my $newID=$returnItems[4];

	my $newUser=
"<utente id=\"$newID\">
<nome>$nome</nome>
<cognome>$cognome</cognome>
<dataDiNascita>$dataDiNascita</dataDiNascita>
<email>$email</email>
<password>$password</password>
<admin>no</admin>
$generiPreferiti
</utente>";

	&scriviDB($parser, $newUser, $doc, $query, &percorsoDBUtenti);
}

sub aggiungiFilm {
	my $src=$_[0];
	my $alt=$_[1];
	my $titolo=$_[2];
	my $dataUscita=$_[3];
	my $paese=$_[4];
	my $durata=$_[5];
	my $trama=$_[6];
	my $incasso=$_[7];
	my $valutazioneSito=$_[8];
	my $recensione=$_[9];
	my $genere=$_[10];
	my $annoProduzione=$_[11];
	my $inSala=$_[12];
	my $cast=$_[13];
	my $regia=$_[14];

	my @returnItems=&inizioAggiunta("films", "film", &percorsoDBFilms);
	my $parser=$returnItems[0];
	my $doc=$returnItems[1];
	my $root=$returnItems[2];
	my $query=$returnItems[3];
	my $newID=$returnItems[4];
	my $newUser="
<film id=\"$newID\">
<locandina src=\"$src\" alt=\"$alt\" />
<titolo>$titolo</titolo>
<dataUscita>$dataUscita</dataUscita>
<paese>$paese</paese>
<durata>$durata</durata>
<trama>$trama</trama>
<incasso valuta=\"euro\" unitaMisura=\"M.\">$incasso</incasso>
<valutazioneSito>$valutazioneSito</valutazioneSito>
<recensione>$recensione</recensione>
<genere>$genere</genere>
<annoProduzione>$annoProduzione</annoProduzione>
<inSala>$inSala</inSala>
<attori>$cast</attori>
<regia>$regia</regia>
</film>";

	&scriviDB($parser, $newUser, $doc, $query, &percorsoDBFilms);

	my $init='<?xml version="1.0" encoding="UTF-8"?> <database><commenti> </commenti></database>';
	my $path= &percorsoCommentiFilm."$newID.xml";

	unless(open FILE, '>'.$path) {
    	# Die with error message
    	# if we can't open it.
   		die $!;
	}
    flock(FILE, LOCK_EX) or die "Could not lock '$file' - $!";
    print FILE $init;
    close FILE;
    $mode = "6666";   chmod oct($mode), "$path";

    return $newID;
}

sub aggiungiFilmProssimamente {
	my $src=$_[0];
	my $alt=$_[1];
	my $titolo=$_[2];
	my $dataUscita=$_[3];
	my $paese=$_[4];
	my $durata=$_[5];
	my $trama=$_[6];
	my $genere=$_[7];
	my $annoProduzione=$_[8];
	my $inSala=$_[9];
	my $cast=$_[10];
	my $regia=$_[11];

	my @returnItems=&inizioAggiunta("filmsProssimamente", "filmProssimamente", &percorsoDBFilms);
	my $parser=$returnItems[0];
	my $doc=$returnItems[1];
	my $root=$returnItems[2];
	my $query=$returnItems[3];
	my $newID=$returnItems[4];

	my $newUser="<filmProssimamente id=\"$newID\">
<locandina src=\"$src\" alt=\"$alt\" />
<titolo>$titolo</titolo>
<dataUscita>$dataUscita</dataUscita>
<paese>$paese</paese>
<durata>$durata</durata>
<trama>$trama</trama>
<genere>$genere</genere>
<annoProduzione>$annoProduzione</annoProduzione>
<inSala>$inSala</inSala>
<attori>$cast</attori>
<regia>$regia</regia>
</filmProssimamente>";

	&scriviDB($parser, $newUser, $doc, $query, &percorsoDBFilms);

	my $init='<?xml version="1.0" encoding="UTF-8"?> <database><commenti> </commenti></database>';
	my $path= &percorsoCommentiFilmProssimamente."$newID.xml";

	unless(open FILE, '>'.$path) {
    	# Die with error message
    	# if we can't open it.
   		die $!;
	}
    flock(FILE, LOCK_EX) or die "Could not lock '$file' - $!";
    print FILE $init;
    close FILE;
    $mode = "6666";   chmod oct($mode), "$path";
}

sub aggiungiCommentoNoProssimamente {
	my $email=$_[0];
	my $testo=$_[1];
	my $idFilm=$_[2];
	my($day, $month, $year)=(localtime)[3,4,5];
	my $dataCommento= ($year+1900)."-".($month+1)."-$day";
	my($min,$hour)=(localtime)[1,2];
	if ($min<10){
		$min="0".$min;
	}
	if ($hour<10){
		$hour="0".$hour;
	}
	my $oraCommento="$hour:$min";

	my $db_path= &percorsoDBUtenti;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement;
	my $query="/database/utenti/utente[email=\"$email\"]/nome";
	my $utenteNome=$doc->findvalue($query);
	my $query="/database/utenti/utente[email=\"$email\"]/cognome";
	my $utenteCognome=$doc->findvalue($query);

	$db_path=&percorsoCommentiFilm."$idFilm.xml";
	my @returnItems=&inizioAggiunta("commenti", "commento", $db_path);
	my $parser=$returnItems[0];
	my $doc=$returnItems[1];
	my $root=$returnItems[2];
	my $query=$returnItems[3];
	my $newCommento="
<commento>
	<autore>
		<nome>$utenteNome</nome>
		<cognome>$utenteCognome</cognome>
		<email>$email</email>
	</autore>
	<data>$dataCommento</data>
	<ora>$oraCommento</ora>
	<testo>$testo</testo>
</commento>";

	&scriviDB($parser, $newCommento, $doc, $query, $db_path);
}

sub aggiungiCommentoProssimamente {
	my $email=$_[0];
	my $testo=$_[1];
	my $idFilm=$_[2];
	my($day, $month, $year)=(localtime)[3,4,5];
	my $dataCommento= ($year+1900)."-".($month+1)."-$day";
	my($min,$hour)=(localtime)[1,2];
	if ($min<10){
		$min="0".$min;
	}
	if ($hour<10){
		$hour="0".$hour;
	}
	my $oraCommento="$hour:$min";

	my $db_path= &percorsoDBUtenti;
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $root=$doc->getDocumentElement;
	my $query="/database/utenti/utente[email=\"$email\"]/nome";
	my $utenteNome=$doc->findvalue($query);
	my $query="/database/utenti/utente[email=\"$email\"]/cognome";
	my $utenteCognome=$doc->findvalue($query);

	$db_path=&percorsoCommentiFilmProssimamente."$idFilm.xml";
	my @returnItems=&inizioAggiunta("commenti", "commento", $db_path);
	my $parser=$returnItems[0];
	my $doc=$returnItems[1];
	my $root=$returnItems[2];
	my $query=$returnItems[3];
	my $newCommento="
<commento>
	<autore>
		<nome>$utenteNome</nome>
		<cognome>$utenteCognome</cognome>
		<email>$email</email>
	</autore>
	<data>$dataCommento</data>
	<ora>$oraCommento</ora>
	<testo>$testo</testo>
</commento>";

	&scriviDB($parser, $newCommento, $doc, $query, $db_path);
}

sub controlAdmin{
	my $emailAdmin = $_[0];

	my $db_path=&percorsoDBUtenti;
	if (@_>1){
		$db_path=$_[1];
	}
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($db_path) || die("file non trovato \n");
	my $query="/database/utenti/utente[email=\"$emailAdmin\"]/admin";
	my $realAdmin=$doc->findvalue($query);
	return ($realAdmin eq "si" and $emailAdmin ne "");
}

sub loadSession{
	#per recuperare session
	my $cgi = new CGI;
	my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
	my $session = load CGI::Session();
	#creo array associativo con le info recuperate dalla session
	my %sessionInfo;
	$sessionInfo{"utenteNome"}=$session->param("utenteNome") || undef;
	$sessionInfo{"utenteEmail"}=$session->param("utenteEmail") || undef;
	$sessionInfo{"utenteAdmin"}=$session->param("utenteAdmin") || undef;

	return %sessionInfo;
}

1;
