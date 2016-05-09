# tangle

[SAGE](http://www.sagemath.org/) and [GAP4](http://gap-system.org/) code for working with tanglegrams.

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.16427.svg)](http://dx.doi.org/10.5281/zenodo.16427)

This code enumerates and checks the enumeration of tanglegrams, and is to accompany the papers

* Billey, S., Konvalinka, M., & Matsen IV, F. A. (2015). On the enumeration of tanglegrams and tangled chains. <http://arxiv.org/abs/1507.04976>
* Matsen IV, F. A., Billey, S., Kas, A., & Konvalinka, M. (2015, July 16). Tanglegrams: a reduction tool for mathematical phylogenetics. <http://arxiv.org/abs/1507.04784>

It does this by enumerating double cosets of the symmetric group using GAP4.
This is nice in that it gives an explicit list of the tanglegrams, but to actually count such structures please refer to the Billey et al paper for much more efficient formulas.


## Dependencies and setup
Follow [these instructions](http://www.liafa.univ-paris-diderot.fr/~labbe/blogue/2013/02/using-sage-in-the-new-ipython-notebook/) to run the `.ipynb` files in SAGE.
This project uses git submodules, so [init and update appropriately](http://git-scm.com/book/en/Git-Tools-Submodules#Cloning-a-Project-with-Submodules).

Other dependencies:

* [SCons](http://www.scons.org)
* [pandas](http://pandas.pydata.org/)
* [seaborn](https://stanford.edu/~mwaskom/software/seaborn/)


## Running the code

To run the code, just invoke `scons` in this directory.
To see how the code would be run if you did this, invoke `scons -n`.
The parameters for how the code is run are in the individual `SConscript` files for the directories describing the various types of tanglegrams.

This will run the two core scripts, `gen-tangles.py` and `check-tangles.py`.
The former script generates tanglegrams with given parameters, and the latter checks to make sure they actually correspond to distinct tanglegrams.

There are two output formats, the `.idx` file and the `.sobj` file.
The `.idx` file is simply a whitespace-separated tabular file enumerating the tanglegrams.
A line such as

    0       3       ((((1,2),3),4),5);      (((1,2),(3,5)),4);      DoubleCoset(Group([(1,2)]),(),Group([(3,5),(1,2),(1,3)(2,5)]))

says that this tanglegram is composed of trees numbered 0 and 3 (zero indexed in the corresponding tree file), with their Newick strings, and then the corresponding coset.
The `.sobj` file is a binary SAGE format saving the tanglegrams directly; see the SAGE documentation for how to load such files.


## Plotting tanglegrams

The `plot-tangle.R` script will plot the generated tanglegrams like so:

![](http://i.imgur.com/Z7FGB1p.png)

This example was generated by running `scripts/plot-tangle.R rooted-asymmetric/tangle7.idx 7230 output-filename.svg` where the arguments are:

* the path to an index file containing your tanglegram
* the 1-indexed line number of your tanglegram in that file
* an output file path

For this functionality, you will need R and the
[ape](https://cran.r-project.org/web/packages/ape/index.html) and
[dendextend](https://github.com/talgalili/dendextend)
packages, both of which you can install using `install.packages`.
