.. EnergyScope_documentation documentation master file, created by
   sphinx-quickstart on Thu Sep 30 10:32:01 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The EnergyScope model
=====================

.. warning:: New and updated version of the documentation is available in this `library <https://www.energyscope.net/latest/>`_.

The EnergyScope project is an open-source whole-energy system for regional energy system. The model optimises the design and hourly operation over a year for a target year.


.. .. figure:: /images/estd_graphical_abstract.png
   :alt: Graphical abstract
   :name: fig:graphical_abstract
   :width: 16cm

EnergyScope is developed by EPFL (Switzerland) and UCLouvain (Belgium).
This documentation introduces the *core* model EnergyScope with  performances details in the :doc:`/sections/Overview` section.
It has been applied to various countries and extended to face most of its limitations.
For more information on versions, applications, and acknowledgments, see the :doc:`/sections/Releases` section.

Downloading EnergyScope
=======================

The public version of EnergyScope can be downloaded in the Releases section or from its github repository (using the Clone or Download button on the right side of the screen): https://github.com/energyscope/EnergyScope
You might be interested by two different versions:

* `Open solver <https://github.com/energyscope/EnergyScope/tree/GLPK_latest>`_ : uses open-source solver and can directly be run, see `getting started with GLPK <https://energyscope.readthedocs.io/en/master/sections/Getting%20started.html>`_ .
* `Python wrapper <https://github.com/energyscope/EnergyScope/tree/EnergyScope.py>`_ : uses Python for pre/post processing and plotting. It supports ampl-cplex/gurobi solvers but can also work with open-source alternatives. See  `getting started with Python <https://energyscope.readthedocs.io/en/energyscope.py/sections/Getting%20started.html>`_

Main contributors
=================

* Stefano **Moret** (`website <https://www.stefanomoret.com/>`_): moret.stefano@gmail.com
* Gauthier **Limpens** : gauthierLimpens@gmail.com

There are many other developers making this model a community!
You will meet them (and their work) in :doc:`/sections/Releases` section.


Contents
=========

.. toctree::
   :maxdepth: 1

   sections/Overview
   sections/Releases
   sections/Getting started
   sections/How to contribute
   sections/Model formulation
   sections/Input Data
   sections/Bibliography

.. Indices and tables
   ==================
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

