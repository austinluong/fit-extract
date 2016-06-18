fitExtract (Conductivity Data Extraction for EC-LAB)
================================================
Created this to quickly extract resistance values from .fit files created from EC-Lab.
Requires python3 and pandas.

To install pandas run from the command line: pip install pandas

Read comments in LithiumSymmetric.py and Symmetric.py for usage instructions.
Notes both LithiumSymmetric.py and Symmetric.py require ReadFile.py in the same folder
in order to run.


TODO
----
- Improve README
- Use getopt for options
- Combine LithiumSymmetric.py and Symmetric.py w/ options
- Improve data extraction with searching
- Create tests
- Run all channels in same folder and separate into different sheets