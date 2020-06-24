# LZW Compress/Uncompress Algorithm

### Statement:

Implement a unique python 3 script algorithm that resolve LZW compression-decompression

Only available libraries are:
* Pandas/csv
* Numpy
* Argparse

###### ----------------------
#### Compression
Should be called with ```quentin.le-helloco_LZW.py -c -p path/to/file.txt```

```-c``` is used to specified compression and ```-p``` for the path


###### Return
The dictionnary file as a csv ```myfile_dico.csv``` with ```%``` as the reserved character.

The text file ```myfile.lzw```:
* a string of the binary code as first line
* the size before and after compression on second and third line
* the compression rate as fourth line.

The table as if it was done by hand as a csv ```myfile_LZWtable.csv```
###### ----------------------
##### Uncompression
Should be called with ```quentin.le-helloco_LZW.py -u -p path/to/file.lzw```

```-u``` is used to specified uncompression and ```-p``` for the path

Unlike the compression file, this one will only have the first line (binary code) of the txt format.
The dictionnary will be given in the same directory, also it should be automatically loaded with the file given in argument.

###### Return
The text file ```myfile2.txt``` containing the uncompressed text, to be save in the current directory of the script.
###### ----------------------
##### Utils
For csv, the separator is ```,```.

All return files are to be written in the current directory of the script.

Particularly, the first line of csv table file should be exactly the same as the one given, as they will be tested that way

The script will be placed in a ```quentin.le-helloco/``` directory.
The parent directory will contained ```compression/``` and ```decompression/``` each containing the .txt and .lzw file to test


