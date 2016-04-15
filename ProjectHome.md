# epic for Proteomics #
**epic**: Estimating Peptide Identification Confidence can estimate p- and q-values along with False Discovery Rates (FDR) for bottom-up proteomics experiments involving tandem mass spectrometry. This is achieved by transforming the original scores from peptide search engines such as Sequest, X!Tandem, and Spectrum Mill, to a form that separates true and random hits and fitting a mixture of multivariate Gaussian models to them. This work extends the approach by [PeptideProphet](http://peptideprophet.sourceforge.net/).

Input to **epic** is a [tabular csv file](epicTables.md) with score values. It has native support for [\_xt.txt](http://omics.pnl.gov/software/PeptideHitResultsProcessor.php) and [\_fht.txt and \_syn.txt](http://omics.pnl.gov/software/PeptideFileExtractor.php) file formats from [PNNL](http://omics.pnl.gov/software/).

epic is written in Python with Qt (with  [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/download) bindings) for user interface.

See [here](epicScreenshots.md) for few screenshots of epic.

_epic project is developed and maintained by [Ashoka Polpitiya](http://www.tgen.org/research/index.cfm?pageid=77&peopleid=768) (ashoka\_at\_tgen.org, ashoka.pol\_at\_gmail.com)._

_Significant portions of the work were performed at Translational Genomics Research Institute (TGen) in Phoenix, Arizona with the generous support from Virginia G. Piper Charitable Trust and the Flinn Foundation._

![http://epic-fdr.googlecode.com/files/epic_surfaces.png](http://epic-fdr.googlecode.com/files/epic_surfaces.png)<br><br>
<img src='http://epic-fdr.googlecode.com/files/epic_about2.png' />