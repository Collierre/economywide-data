# Scripts for data processing to support EconomyWide

## To use mapit coding

Put the two files mapit_coder.py and mapit_ew.py in a directory on your computer. Then go to that directory in terminal (assuming you're on a mac). To run it type:

python mapit_coder.py

You have to specify certain options, they are:

* -i input-file.csv (replace input-file.csv with name of your csv file - required)
* -o output-file.csv (replace output-file.csv with name of your csv file - required)
* -t (include this if your input file contains a header row and you want to start a new output file with a new header row. If left off output file will be appended not replaced)
* -s num (replace num with number of lines to skip in input-file. Default is 0)