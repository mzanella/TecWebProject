#!/usr/bin/perl
#In questo modulo sono presenti le funzioni per generare la pagina in html
package PageSkeleton;
use strict;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;

use lib 'modules/';
use DBFunctions;
use File::Basename;

sub printDocType{
	print
	"<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
	<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">";
}

sub printHead{
	my $nomePagina = $_[0];
	my $description=$_[1];
	my $keyword=$_[2];
	print
	"<head>
		<link href=\"../public_html/style/css/style.css\" rel=\"stylesheet\" type=\"text/css\" />
		<link href=\"../public_html/style/css/styleFont.css\" rel=\"stylesheet\" type=\"text/css\" />
		<script type=\"text/javascript\" src=\"../public_html/javascript/jquery-1.11.1.min.js\"></script>
		<script type=\"text/javascript\" src=\"../public_html/javascript/button.js\"></script>
		<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
		<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
		<meta name=\"title\" content=\"$nomePagina\" />
		<meta name=\"description\" content=\"$description\" />
		<meta name=\"keyword\" content=\"$keyword\" />
		<meta name=\"language\" content=\"italian it\" />
		<meta name=\"author\" content=\"Oscar Elia Conti, Federico Tavella, Marco Zanella\" />
		<title> $nomePagina </title>
	</head>";
}

sub printHeadStart{
	print
		"<head>
		<link href=\"../public_html/style/css/style.css\" rel=\"stylesheet\" type=\"text/css\" />
		<link href=\"../public_html/style/css/styleFont.css\" rel=\"stylesheet\" type=\"text/css\" />
		<script type=\"text/javascript\" src=\"../public_html/javascript/jquery-1.11.1.min.js\"></script>
		<script type=\"text/javascript\" src=\"../public_html/javascript/button.js\"></script>";
}

sub printHeadEnd{
	my $nomePagina = $_[0];
	my $description=$_[1];
	my $keyword=$_[2];

	print
	"<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
	<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
	<meta name=\"title\" content=\"$nomePagina\" />
	<meta name=\"description\" content=\"$description\" />
	<meta name=\"keyword\" content=\"$keyword\" />
	<meta name=\"language\" content=\"italian it\" />
	<meta name=\"author\" content=\"Oscar Elia Conti, Federico Tavella, Marco Zanella\" />
	<title> $nomePagina</title>
	</head>";
}

sub printBodyStart{
	print
	"<body onload=\"ridimensionamentoPagina();\">";
}

sub printHeader{
	print
	"<div id=\"header\">
		<img id=\"imgHeader\" src=\"../public_html/style/images/logo.png\" alt=\"logo\" />
	</div>";
}

sub printNav{
	#creo array con le voci del menu prestabilite
	my @vociMenu;
	$vociMenu[0] = "<li><a href=\"index.cgi\" tabindex=\"2\"><span xml:lang=\"en\">HOME</span></a></li>";
	$vociMenu[1] = "<li><a href=\"TuttiIFilm.cgi\" tabindex=\"3\">TUTTI I FILM</a></li>";
	$vociMenu[2] = "<li><a href=\"OraInSala.cgi\" tabindex=\"4\">ORA IN SALA</a></li>";
	$vociMenu[3] = "<li><a href=\"Prossimamente.cgi\" tabindex=\"5\">PROSSIMAMENTE</a></li>";
	#leggo la voce del menu corrispondente alla pagina selezionata e la sostituisco nelle vociMenu
	my $voceCorrente = $_[0];
	$voceCorrente=~ s/ - InstaFilm//;
	if ($voceCorrente eq "Home") {
		$vociMenu[0] = "<li class=\"selected\"><span xml:lang=\"en\">HOME</span></li>";
	} elsif ($voceCorrente eq "Tutti i film") {
		$vociMenu[1] = "<li class=\"selected\">TUTTI I FILM</li>";
	} elsif ($voceCorrente eq "Ora in sala"){
		$vociMenu[2] = "<li class=\"selected\">ORA IN SALA</li>";
	} elsif ($voceCorrente eq "Prossimamente"){
		$vociMenu[3] = "<li class=\"selected\">PROSSIMAMENTE</li>";
	}

	print
	"<div id=\"nav\">
		<div id=\"closeButton\">
			<a class=\"icon-close\"></a>
		</div>
		<div id=\"menuButton\">
			<a class=\"icon-menu\"></a>
		</div>
		<ul class=\"menulist\">
			<li id=\"saltamenu\"><a href=\"#content\" tabindex=\"1\">Salta il menù</a></li>
			@vociMenu
		</ul>
	</div>";
}

sub printBreadCrumb{
	my $posizione = $_[0];
	$posizione =~ s/ - InstaFilm//;
	if ($posizione eq "Home"){
		$posizione = "<span xml:lang=\"en\">Home</span>";
	}

	print
	"<div id=\"breadcrumbs\">
		<p id=\"breadcrumbsText\">Ti trovi in: $posizione</p>
	</div>";
}

sub printLoginBar{
	#recupero le info della sessione
	my %sessionInfo=DBFunctions::loadSession;
	#Recupero pagina chiamante per generare id pagina
	my $name = basename($0);
	print "<div id=\"loginBar\">";
	if ($sessionInfo{"utenteNome"} eq undef){
		my $idFilm = $_[0];
		if(defined $idFilm){
			print "<a href=\"Registrati.cgi\" class=\"loginLink\" tabindex=\"6\">Registrati</a>
				   <a href=\"Login.cgi?id=$name?id=$idFilm\" class=\"loginLink\" tabindex=\"7\">Login</a>";
		}
		else{
			print "<a href=\"Registrati.cgi\" class=\"loginLink\" tabindex=\"6\">Registrati</a>
				   <a href=\"Login.cgi?id=$name\" class=\"loginLink\" tabindex=\"7\">Login</a>";
		}
	} else {
		my $nome = $sessionInfo{"utenteNome"};
		print "<p>Ciao, $nome <a href=\"Logout.cgi\" class=\"loginLink\" tabindex=\"6\">Logout</a>";
		if ($sessionInfo{"utenteAdmin"} eq "si"){
			my $admin = DBFunctions::controlAdmin($sessionInfo{"utenteEmail"});
			if ($admin==1){
				print "<a href=\"Amministrazione.cgi\" class=\"loginLink\" tabindex=\"7\">Amministrazione</a></p>";
			}
		}

	}
	print "</div>";
}

sub printContentStart{
	print
	"<div id=\"content\">";
}

sub printContentEnd{
	print
	"</div>";
}

sub printFooter{
	print
	"<div id=\"footer\">
	<p class=\"elementiFooter\">
		<a href=\"http://validator.w3.org/check?uri=referer\">
		<img src=\"http://www.w3.org/Icons/valid-xhtml10\" alt=\"Valid XHTML 1.0 Strict\" height=\"31\" width=\"88\" /></a>
		<a href=\"http://jigsaw.w3.org/css-validator/check/referer\">
		<img style=\"border:0;width:88px;height:31px\" src=\"http://jigsaw.w3.org/css-validator/images/vcss\" alt=\"CSS Valido!\" /></a>
		Autori: O. E. Conti, F. Tavella, M. Zanella
	</p>
	</div>";
}

sub printBodyEnd{
	print
	"</body>";
}

sub printHtmlEnd{
	print
	"</html>";
}

#Ogni modulo perl deve terminare con la linea seguente
1;
