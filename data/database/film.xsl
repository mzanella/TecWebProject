<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output indent="yes" omit-xml-declaration="yes" />
	<xsl:template match="/">
		<xsl:if test="database/films/film[last()]">
			<h1>Ultimi Film</h1>
			<div class="listaFilm">
				<dl class="anteprimaFilm">
					<xsl:variable name="id" select="database/films/film[last()]/@id" />
					<xsl:variable name="alt" select="database/films/film[last()]/locandina/@alt" />
					<xsl:variable name="src" select="database/films/film[last()]/locandina/@src" />
					<xsl:variable name="titolo" select="database/films/film[last()]/titolo" />
					<dt class="anteprimaTitoloFilm"><a href='film.cgi?id={$id}' ><xsl:value-of select="database/films/film[last()]/titolo" /></a></dt>
					<dd><img class="anteprimaFilmImg" src="{$src}" alt="{$alt}" title="Locandina del film: {$titolo}"/></dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Durata: </span>
						<xsl:value-of select="database/films/film[last()]/durata" /> min.
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Anno: </span>
						<xsl:value-of select="database/films/film[last()]/annoProduzione" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Regia: </span>
						<xsl:value-of select="database/films/film[last()]/regia" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Attori: </span>
						<xsl:value-of select="database/films/film[last()]/attori" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Genere: </span>
						<xsl:value-of select="database/films/film[last()]/genere" />
					</dd>
				</dl>
				<xsl:if test="database/films/film[last()-1]">
					<dl class="anteprimaFilm">
						<xsl:variable name="id" select="database/films/film[last()-1]/@id" />
						<xsl:variable name="alt" select="database/films/film[last() -1]/locandina/@alt" />
						<xsl:variable name="src" select="database/films/film[last() -1]/locandina/@src" />
						<xsl:variable name="titolo" select="database/films/film[last()-1]/titolo" />
						<dt class="anteprimaTitoloFilm"><a href='film.cgi?id={$id}' ><xsl:value-of select="database/films/film[last() -1]/titolo" /></a></dt>
						<dd><img class="anteprimaFilmImg" src="{$src}" alt="{$alt}" title="Locandina del film: {$titolo}"/></dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Durata: </span>
							<xsl:value-of select="database/films/film[last() -1]/durata" /> min.
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Anno: </span>
							<xsl:value-of select="database/films/film[last() -1]/annoProduzione" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Regia: </span>
							<xsl:value-of select="database/films/film[last()-1]/regia" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Attori: </span>
							<xsl:value-of select="database/films/film[last() -1]/attori" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Genere: </span>
							<xsl:value-of select="database/films/film[last() -1]/genere" />
						</dd>
					</dl>
				</xsl:if>
			</div>
		</xsl:if>
		<xsl:if test="database/filmsProssimamente/filmProssimamente[last()]">
			<h1>Prossimamente al cinema</h1>
			<div class="listaFilm">
				<dl class="anteprimaFilm">
					<xsl:variable name="id" select="database/filmsProssimamente/filmProssimamente[last()]/@id" />
					<xsl:variable name="alt" select="database/filmsProssimamente/filmProssimamente[last()]/locandina/@alt" />
					<xsl:variable name="src" select="database/filmsProssimamente/filmProssimamente[last()]/locandina/@src" />
					<xsl:variable name="titolo" select="database/filmsProssimamente/filmProssimamente[last()]/titolo" />
					<dt class="anteprimaTitoloFilm"><a href="filmProssimamente.cgi?id={$id}" ><xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()]/titolo" /></a></dt>
					<dd><img class="anteprimaFilmImg" src="{$src}" alt="{$alt}" title="Locandina del film: {$titolo}"/></dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Durata: </span>
						<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()]/durata" /> min.
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Anno: </span>
						<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()]/annoProduzione" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Regia: </span>
						<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()]/regia" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Attori: </span>
						<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()]/attori" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Genere: </span>
						<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()]/genere" />
					</dd>
				</dl>
					<xsl:if test="database/filmsProssimamente/filmProssimamente[last()-1]">
					<dl class="anteprimaFilm">
						<xsl:variable name="id" select="database/filmsProssimamente/filmProssimamente[last()-1]/@id" />
						<xsl:variable name="alt" select="database/filmsProssimamente/filmProssimamente[last()-1]/locandina/@alt" />
						<xsl:variable name="src" select="database/filmsProssimamente/filmProssimamente[last()-1]/locandina/@src" />
						<xsl:variable name="titolo" select="database/filmsProssimamente/filmProssimamente[last()-1]/titolo" />
						<dt class="anteprimaTitoloFilm"><a href="filmProssimamente.cgi?id={$id}" ><xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()-1]/titolo" /></a></dt>
						<dd><img class="anteprimaFilmImg" src="{$src}" alt="{$alt}" title="Locandina del film: {$titolo}"/></dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Durata: </span>
							<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()-1]/durata" /> min.
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Anno: </span>
							<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()-1]/annoProduzione" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Regia: </span>
							<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()-1]/regia" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Attori: </span>
							<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()-1]/attori" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Genere: </span>
							<xsl:value-of select="database/filmsProssimamente/filmProssimamente[last()-1]/genere" />
						</dd>
					</dl>
				</xsl:if>
			</div>
		</xsl:if>
		<xsl:if test="database/films/film[valutazioneSito='5'][last()]">
			<h1>Imperdibili</h1>
			<div class="listaFilm">
				<dl class="anteprimaFilm">
					<xsl:variable name="id" select="database/films/film[valutazioneSito='5'][last()]/@id" />
					<xsl:variable name="alt" select="database/films/film[valutazioneSito='5'][last()]/locandina/@alt" />
					<xsl:variable name="src" select="database/films/film[valutazioneSito='5'][last()]/locandina/@src" />
					<xsl:variable name="titolo" select="database/films/film[valutazioneSito='5'][last()]/titolo" />
					<dt class="anteprimaTitoloFilm"><a href="film.cgi?id={$id}" ><xsl:value-of select="database/films/film[valutazioneSito='5'][last()]/titolo" /></a></dt>
					<dd><img class="anteprimaFilmImg" src="{$src}" alt="{$alt}" title="Locandina del film: {$titolo}"/></dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Durata: </span>
						<xsl:value-of select="database/films/film[valutazioneSito='5'][last()]/durata" />  min.
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Anno: </span>
						<xsl:value-of select="database/films/film[valutazioneSito='5'][last()]/annoProduzione" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Regia: </span>
						<xsl:value-of select="database/films/film[valutazioneSito='5'][last()]/regia" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Attori: </span>
						<xsl:value-of select="database/films/film[valutazioneSito='5'][last()]/attori" />
					</dd>
					<dd class="datoFilm"><span class="nomeDatoFilm">Genere: </span>
						<xsl:value-of select="database/films/film[valutazioneSito='5'][last()]/genere" />
					</dd>
				</dl>
					<xsl:if test="database/films/film[valutazioneSito='5'][last()-1]">
					<dl class="anteprimaFilm">
						<xsl:variable name="id" select="database/films/film[valutazioneSito='5'][last()-1]/@id" />
						<xsl:variable name="alt" select="database/films/film[valutazioneSito='5'][last()-1]/locandina/@alt" />
						<xsl:variable name="src" select="database/films/film[valutazioneSito='5'][last()-1]/locandina/@src" />
						<xsl:variable name="titolo" select="database/films/film[valutazioneSito='5'][last()-1]/titolo" />
						<dt class="anteprimaTitoloFilm"><a href="film.cgi?id={$id}" ><xsl:value-of select="database/films/film[valutazioneSito='5'][last()-1]/titolo" /></a></dt>
						<dd><img class="anteprimaFilmImg" src="{$src}" alt="{$alt}" title="Locandina del film: {$titolo}" /></dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Durata: </span>
							<xsl:value-of select="database/films/film[valutazioneSito='5'][last()-1]/durata" /> min.
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Anno: </span>
							<xsl:value-of select="database/films/film[valutazioneSito='5'][last()-1]/annoProduzione" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Regia: </span>
							<xsl:value-of select="database/films/film[valutazioneSito='5'][last()-1]/regia" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Attori: </span>
							<xsl:value-of select="database/films/film[valutazioneSito='5'][last()-1]/attori" />
						</dd>
						<dd class="datoFilm"><span class="nomeDatoFilm">Genere: </span>
							<xsl:value-of select="database/films/film[valutazioneSito='5'][last()-1]/genere" />
						</dd>
					</dl>
				</xsl:if>
			</div>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
