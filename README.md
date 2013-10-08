pyltesim
========

Modules for simulating an LTE cellular network in python.

For some of my [academic papers] (http://scholar.google.de/citations?hl=en&user=tEM1S0EAAAAJ), I was in need of simulating the link layer of hexagonally arranged base stations that communicate with mobiles using OFDMA. For that I built this simulator.

It provides a world module that is definitely reusable for the hexagonal arrangements (or others with small modifications) and the resource allocation. The general module setup with configuration, scripts, results handling etc. could also be reused. Fading modeling or rate craving greedy could also be of interest to some. Other modules like /optim, /raps, or /quantmap are very specifically concerned with the content of my research papers (resource allocation algorithms I propose).

Feel free to browse, salvage, apply...

Requirements:
* python 2.7.3 with ssl
* numpy
* scipy
* matplotlib
* pyipopt/ipopt
* recommended: virtualenv
