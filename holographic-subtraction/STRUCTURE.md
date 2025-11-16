PROJECT STRUCTURE

=================



holographic-subtraction/

│

├── README.md                          Main project description and results

├── LICENSE                            MIT License

├── .gitignore                         Git ignore rules

├── STRUCTURE.md                       This file - folder organization

│

├── paper/

│   ├── holographic\_subtraction.pdf   Full paper with embedded figures (796 KB)

│   └── figs/                          Figure folder (currently empty)

│

├── code/

│   └── generate\_all\_figures.py       Script to recreate all 4 paper figures

│

├── data/                              Numerical simulation results (CSV files)

├── docs/                              Supplementary documentation

├── src/                               Auxiliary source code modules

├── issues/                            Issue tracking notes

└── manifest/                          Project metadata





FOLDER DESCRIPTIONS

===================



paper/

------

Contains the main research paper.



\- holographic\_subtraction.pdf: Complete manuscript (796 KB)

&nbsp; All figures are embedded inside the PDF.



\- figs/: Empty folder for standalone figure files.

&nbsp; Can be populated by running code/generate\_all\_figures.py





code/

-----

Python scripts for simulations and analysis.



Current:

\- generate\_all\_figures.py: Creates 4 publication figures

&nbsp; \* epsilon\_vs\_N.pdf

&nbsp; \* w\_theta\_comparison.pdf  

&nbsp; \* chandra\_w\_theta.pdf

&nbsp; \* epsilon\_vs\_alpha.pdf



Planned:

\- vortex\_simulation.py (Metropolis-Hastings on sphere)

\- free\_energy\_optimization.py

\- dimensional\_scan.py

\- landy\_szalay.py (angular correlation estimator)





data/

-----

Numerical outputs in CSV format.



Planned files:

\- epsilon\_vs\_N.csv (suppression parameter vs N)

\- w\_theta\_simulation.csv (angular correlations)

\- vortex\_positions.csv (equilibrated BH positions)





docs/

-----

Extended documentation.



Planned:

\- derivation\_notes.pdf (detailed math)

\- FAQ.md

\- interactive notebooks





src/

----

Reusable Python modules.



Example:

\- geometry.py (S2 distances, embeddings)

\- thermodynamics.py (free energy functional)

\- statistics.py (bootstrap, estimators)





CURRENT STATUS

==============



✓ Paper complete (PDF with all figures)

✓ Figure generation script ready

⧗ Simulation scripts in development

⧗ Data files to be uploaded

⧗ Documentation planned





Last updated: December 16, 2025

