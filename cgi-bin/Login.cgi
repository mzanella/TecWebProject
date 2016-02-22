#!/usr/bin/perl -w
use CGI;
use lib './perl/modules/';
use PageSkeleton;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;
use lib 'modules/';
use DBFunctions;

print "Content-Type: text/html\n\n";
PageSkeleton::printDocType();
PageSkeleton::printHeadStart();
print
"	<script type=\"text/javascript\" src=\"../public_html/javascript/controlliLogin.js\"></script>";
my $nomePagina = "Login - InstaFilm";
my $description = "Pagina per effettuare il login";
my $keyword = "Film, Cinema, InstaFilm, Film in sala, Login";
PageSkeleton::printHeadEnd($nomePagina, $description, $keyword);
print "<body onload=\"ridimensionamentoPagina(); caricamento();\">";
PageSkeleton::printHeader();
PageSkeleton::printNav($nomePagina);
PageSkeleton::printBreadCrumb("Login");
PageSkeleton::printContentStart();
my $cgi = new CGI;
my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;
my $session = load CGI::Session();
my $err = $session->param("errore");
#Qui va inserito il contenuto
if ($session->param("utenteEmail") eq undef){
	my $query = CGI->new();
	my %input;
	my @names = $query->param();
	foreach $name (@names) {
		$input{$name}=$query->param($name);
	}
	$paginaProvenienza = $input{"id"};
	print
	"<h2 id=\"h2Login\">Accedi</h2>
		<form method=\"post\" action=\"perl/controlliLogin.cgi\" id=\"loginForm\" onsubmit=\"return validaForm();\">
			<fieldset id=\"loginFieldSet\">
				<label for=\"email\">E-mail:</label>
				<input type=\"text\" id=\"email\" name=\"email\" />
				<label for=\"password\">Password:</label>
				<input class=\"loginForm\" type=\"password\" id=\"password\" name=\"password\" />
				<input class=\"loginForm\" type=\"submit\" value=\"Accedi\" id=\"invio\" />
				<input class=\"loginForm\" type=\"hidden\" name=\"paginaProvenienza\" value=\"$paginaProvenienza\" />";
				&errore($err);
				print "
			</fieldset>
		</form>";
} else {
	my $nome = $session->param("utenteNome");
	print
	"<h2 id=\"h2Login\">Errore</h2>
	<p id=\"erroreLogin\">Sei già loggato come $nome.
		Se non sei tu procedi al <a href=\"Logout.cgi\">logout</a> e rieffettua il login con il tuo account.</p>";
}
#Fine contenuto
PageSkeleton::printContentEnd();
PageSkeleton::printFooter();
PageSkeleton::printBodyEnd();
PageSkeleton::printHtmlEnd();

sub errore(){
	my $s=$_[0];
	if(defined $s){
		print "<div class=\"loginMessage\"> $s </div>";
	}
}
