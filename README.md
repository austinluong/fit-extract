fitExtract (Conductivity Data Extraction for EC-LAB)
================================================
Extracts RInterface and RElectrolyte data from all '.fit' files in
a specified folder and writes the extracted data into a 'Data.xlsx' in the
same folder. '.fit' files are created by clicking save in the EC-LAB software
after fitting (minimizing) a curve with Zfit. If data from multiple channels
is in the same folder, then the data will be separated into different sheets
in the same "Data.xlsv" file.

Requires python3 and pandas.

To install pandas, run from the command line:

    pip install pandas

Requires readFile.py and fitExtract.py to be in the same folder.


USAGE
-----
Run from the command line:

    $ cd [path]/folder_with_fitExtract.py
    $ python fitExtract.py [options]

Running with no options will run the program in the same folder as fitExtract
By default the program will only extract R2 (used for Ni/Al symmetric cells)
R1 should be set to 0.1 ohm in EC-Lab.

Important: Do not change file names of any of the files. This program requires
           that the file name end in the default channel number format to work.

Arguments available are:
Folder (-f)

    $ python fitExtract.py -f [folderpath1] [folderpath2] ...

Runs the program in the specified folders. The path must be in quotes.

Lithium Symmetric (-ls)

    $ python fitExtract.py -ls

Extracts R2 and R3 and determines which is RInterface and RElectrolyte by setting
the one with the higher value to be RInterface (not always correct but can adjusted
manually in the .xlsv if needed).

Additional (-add)

    $ python fitExtract.py -add param1 param2 ...

In additional to the default parameters extracted (R2, R3), the program will
also extract the specfied parameters (Ex: Q2, a1). Note case matters.

Custom (-c)

    $ python fitExtract.py -c param1 param2 ...

Extracts specified parameters intead of default (R2).


Examples:

$ python fitExtract.py -f 'C:\Users\[USER_NAME]\[PATH]' 'C:\Users\[USER_NAME]\[PATH2]' -ls -add Q2
Result - Data.xlsx file created in both paths specified with following information:

    Sheet Name: Ch 7

    File Name | RElectrolyte (ohm) | RInterface | Q2 (F.s^(a-1)
    ------------------------------------------------------------
    file.fit  | 12345              | 29929      | .00000023
    ...       | ...                | ...        | ...

    Additional Sheets: Ch 8, Ch 9


TODO
-----
- Implement getopt for options
- Create tests
- Run all channels in same folder and separate into different sheets