#!/usr/bin/perl
#In questo modulo vengono definite alcune funzioni utili per generare codice html
package HtmlFunctions;
use strict;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
#Questa funzione serve a stampare un range di numeri racchiusi dal tag <option>.
#Parametri attesi: 2 interi limInf e limSup che rappresentano il range dei numeri da stampare.
sub printOptionsNumber{
	my $limiteInferiore = $_[0];
	my $limiteSuperiore = $_[1];

	for(my $index = $limiteInferiore; $index <= $limiteSuperiore; $index++){
		print "<option value=\"$index\">$index</option>";
	}
}

#Questa funzione stampa gli options da 1 a 31.
sub printOptionDays{
	printOptionsNumber(1,31);
}

#Questa funzione stampa gli options da 1 a 12.
sub printOptionMonths{
	printOptionsNumber(1,12);
}

#Ogni modulo perl deve terminare con la linea seguente
1;
