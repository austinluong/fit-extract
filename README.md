fit-extract (Data Extraction for EC-LAB)
================================================
Extracts parameter (R2, R3, Q1, etc.) data from all '.fit' files in
a specified folder and writes the extracted data into a 'Data.xlsx' in the
same folder. '.fit' files are created by clicking save in the EC-LAB software
after fitting (minimizing) a curve with Zfit. If data from multiple channels
is in the same folder, then the data will be separated into different sheets
in the same "Data.xlsv" file.

Requires python 3.2.x or above and pandas (should install automatically).


INSTALL
-----
Run from the command line:
    
    $ pip install fit-extract

Alternatively, you can download the zip from github or use git clone.


USAGE
-----
Navigate to the folder containing the .fit files using the command line:

    $ cd [FOLDERPATH]
    $ python fit-extract [OPTIONS]

Running with no options will run the program in the current directory. By default 
the program will extract R2 and R3 and group the lower values and higher value of 
each pair into the same column to ensure consistency. R1 should be set to 0.1 ohm 
in EC-Lab.

Important: Do not change file names of any of the files. This program requires
           that the file name end in the default channel number format to work.

#### Arguments and Options:

###### Help (--help or -h)

    $ python fit-extract -h
    
Displays usage information.

###### Folder (--folder or -f)

    $ python fit-extract -f [FOLDERPATH [FOLDERPATH...]]

Runs the program in the specified folders (multiple can be specified). 
The path must be in quotes.

###### Additional (--additional or -a)

    $ python fit-extract -add [PARAM [PARAM...]]

In additional to the default parameters extracted (R2, R3), the program will
also extract extra specfied parameters (Ex: Q2, a1). Note case matters.

###### Custom (--custom or -c)

    $ python fit-extract -c [PARAM [PARAM...]]

Extracts specified parameters intead of default (R2).

###### Group By Size (--groupbysize or -gs)
    
    $ python fit-extract -c [PARAM_1 PARAM_2]

Ensures consistency between two of the same type of parameter (default: ['R2', 'R3']) 
by grouping their values by size.



#### Example:

    $ python fit-extract -f 'C:\Users\[USER_NAME]\[PATH]' 'C:\Users\[USER_NAME]\[PATH2]' -ls -add Q2 a1
    
Result - Data.xlsx file created in both paths specified with following information:

    Sheet Name: Ch 7

    File Name | R2 (ohm)           | R3 (ohm)         | Q2 (F.s^(a-1)) | a1 ()
    -------------------------------------------------------------------------------
    file.fit  | 12345              | 29929            | .00000023      | 0.124
    ...       | ...                | ...              | ...            | ...

    Additional Sheets: Ch 8, Ch 9


TODO
-----
- Create tests (IN PROGRESS)
- Implement better sorting for filenames (LOW PRIORITY)