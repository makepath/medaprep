medaprep
#########

medaprep is used to prepare ``xarray`` Datasets for downstream tasks.

Usage
#####

medaprep.skim.features
-----------------------

.. code-block:: python

    >>> import numpy as np
    >>> import pandas as pd
    >>> import xarray as xr
    >>> from medaprep import skim
    >>> temp = 15 + 8 * np.random.randn(2, 2, 3)
    >>> precip = 10 * np.random.rand(2, 2, 3)
    >>> lon = [[-99.83, -99.32], [-99.79, -99.23]]
    >>> lat = [[42.25, 42.21], [42.63, 42.59]]
    >>> ds = xr.Dataset(
      {
          "temperature": (["x", "y", "time"], temp),
          "precipitation": (["x", "y", "time"], precip),
          },
      coords={
          "lon": (["x", "y"], lon),
          "lat": (["x", "y"], lat),
          "time": pd.date_range("2014-09-06", periods=3),
          "reference_time": pd.Timestamp("2014-09-05"),
          },
                     )
     >>> df = skim.features(ds)
     >>> df
         variables       data_types  NaNs    mean    std     maximums    minimums
     0   temperature     float64     False   14.3177 9.08339 30.3361     -7.76803
     1   precipitation   float64     False   4.62568 3.03081 9.89768     0.147005

For more details see `Documentation`_ and `Example Notebooks`_.

Installation
############

Using pip
---------

.. code-block:: bash

   pip install medaprep

Using Conda
-----------

.. code-block:: bash

   conda install -c conda-forge medaprep


Developing
##########

pre-commit setup
----------------

This project uses `pre-commit`, `isort`, `black`, and `flake8` to help enforce best practices. These libraries are all included in `requirements-dev.txt` and can be installed with `pip` by running:

.. code-block:: bash
   
   pip install -r requirements-dev.txt

Once pre-commit is installed, install the hooks specified by the config file into `.git`:

.. code-block:: bash

   pre-commit install

You can then test pre-commit by running:

.. code-block:: bash

   pre-commit
