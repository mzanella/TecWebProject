#!/usr/bin/perl -w

my $titolo="titolo";
my $dataUscita="dataUscita";
my $paese="paese";
my $durata="durata";
my $incasso="incasso";
my $valutazionePubblico="valutazionePubblico";
my $valutazioneCritica="valutazioneCritica";
my $descrizione="descrizione";
my $srclocandina="srclocandina";
my $altlocandina="altlocandina";

&aggiungiFilm($titolo,$dataUscita,$paese,$durata,$incasso,$valutazionePubblico,$valutazioneCritica,$descrizione,$srclocandina,$altlocandina);

sub aggiungiFilm{
	print "Content-Type: text/html\n\n";
	use XML::LibXML;
	my $file="filmMinions_.xml"; 						#file di cui fare il parsing
	my $parser=XML::LibXML->new();						#creazione del parser
	my $doc=$parser->parse_file($file) || die("file non trovato \n");	#parsing del file
	#$doc->documentElement->setNamespace("http://www.dominio.com","d"); 	#imposta il dominio poi bisogna mettere le d nelle espressioni XPath
	my $root=$doc->getDocumentElement;					#estrazione radice
	my $query;
	#$query="/listaFilm/film[last()]/titolo/text()";			#query in XPath
	#my $node=$doc->findnodes($query)->get_node(1); 			#puntatore $node viene messo sul nodo cercato con la query
	$query="/listaFilm/film[last()]/attribute::id";				#query per cercare id dell'ultimo film
	my $lastID=$doc->findvalue($query);					#estrae il valore dell'attributo cercato con la query
	my $newID=$lastID+1;

	#creazione del nuovo film da far diventare nodo ( i parametri si trovano nell'array @_ )
	my $newFilm="\n<film id=\"$newID\">
<titolo>$_[0]</titolo>
<dataUscita>$_[1]</dataUscita>
<paese>$_[2]</paese>
<durata unitaTempo=\"Min.\">$_[3]</durata>
<incasso unitaIncasso=\"M\">$_[4]</incasso>
<valutazionePubblico>$_[5]</valutazionePubblico>
<valutazioneCritica>$_[6]</valutazioneCritica>
<descrizione>$_[7]</descrizione>
<locandina src=\"$_[8]\" alt=\"$_[9]\" />
</film>";

	my $newNodo=$parser->parse_balanced_chunk($newFilm);			#creazione nodo + controllo sia ben formato
	$query="/listaFilm";
	my $node=$doc->findnodes($query)->get_node(1);
	$node->appendChild($newNodo);						#nodo messo nell'albero
	open(OUT, ">$file");							#apertura file
	print OUT $doc->toString;						#serializzazione + salvataggio
	close(OUT);								#chiusura file
}
