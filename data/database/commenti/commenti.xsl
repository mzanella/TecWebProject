<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output indent='yes' omit-xml-declaration="yes" />
<xsl:template match="/database/commenti">
	<div id="numeroCommenti">
		<p id="paragraphNumeroCommenti">
			<xsl:value-of select="count(commento)" /> commenti
		</p>
	</div>
	<xsl:for-each select="commento">
		<xsl:sort select="data" order="descending"/>
		<xsl:sort select="ora" order="descending"/>
		<div class="commento">
			<p class="datiCommento">
				<span class="autoreCommento">
				<xsl:value-of select="autore/nome" />&#160;<xsl:value-of select="autore/cognome" />
				</span>
				<span class="dataCommento">
				<xsl:value-of select="data" /> &#160;
				</span>
				<span class="oraCommento">
				<xsl:value-of select="ora" />
				</span>
			</p>
			<p class="testoCommento">
				<xsl:value-of select="testo" />
			</p>
		</div>
	</xsl:for-each>
</xsl:template>
</xsl:stylesheet>
