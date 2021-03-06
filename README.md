# File splitter
The script has two modes one for chart files and one for cluster files. 

## chart
The `chart` mode splits the data entries by genes, and writes them into a file containing all entries and into sub files that
contain only 50 data rows each.

## cluster
The `cluster` mode splits the cluster file into chart like files, each containing the data of one cluster. The cluster 
info is added as additional columns. Afterwards each chart like file gets handled like
the usual chart files.

## Requirements
You need to have python 2.7 installed. You can test this by executing 

    python --version
    
in a terminal. The output should look like   

    ➜ python --version
    Python 2.7.10
    
## Usage

You'll need to execute it in a terminal like

    python file_splitter.py [file_path] [chart|cluster]
    
where `file_path` is the path leading to the data file. The second argument defines how the
file gets handled. An example call would be

    python file_splitter.py path/to/chart.txt chart
    
This will produce an output like

    ➜ python file_splitter.py ../input/chart.txt 
    INFO: directory 'output' already exists, will probably overwrite the old data
    INFO: created the complete data file
    INFO: created 38 splitted files
    
In this case the output directory already existed, which is no problem. It also 
tells you that it created the file with all the data, and the splitted files. 

You will find all files in the created `output` folder, in the directory in which 
you executed the script. 

In case of handling a cluster, you will find all output files in `output/cluster`.