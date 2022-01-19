=======================
SiEPIC Analysis Package
=======================


.. image:: https://img.shields.io/pypi/v/siepic_analysis_package.svg
        :target: https://pypi.python.org/pypi/siepic_analysis_package

.. image:: https://img.shields.io/travis/mustafacc/siepic_analysis_package.svg
        :target: https://travis-ci.com/mustafacc/siepic_analysis_package

.. image:: https://readthedocs.org/projects/siepic-analysis-package/badge/?version=latest
        :target: https://siepic-analysis-package.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A Python (v3.6.5) package that provides a set of basic analysis functions commonly used in integrated photonics.



* Documentation: https://siepic-analysis-package.readthedocs.io.


Features
--------

## Functions
* **calibrate**

Calibrates an input spectrum response with respect to another input response.

* **calibrate_envelope**

Calibrates an input spectrum response with respect to the envelope of another input response. This is useful for calibrating non-periodic responses using another non-periodic response. i.e. calibrating the reflection port spectrum of a Bragg response using its through port spectrum.

* **baseline_correction**

Calibrates an input response with respect to it's baseline. This is useful for calibrating periodic responses, using their own response as a reference, i.e. a ring resonator response or a mach-zehnder interferometer response.

* **cutback**

Extrapolate the losses of different input data files losses using the cutback method.


* **to_s_params**

Converts the input data to generate a .dat file compatible with Lumerical INTERCONNECT's N-port s-parameter file format. 

* **download_response**

Downloads a .mat response (Caverley's pyoptomip format) from a url and parses data into a variable. 