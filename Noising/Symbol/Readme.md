# How to use

## Important variables
ccode = A list of buggy programs.
ccode is a list of string. It is a list of error-free java programs. Use this variable to store the input files.

## Classification
The SymbolNoising.py takes a list of buggy programs as input and break the file into 10 corrupted training samples. The output of this program is a pickle.
The toCSVClassification.py takes the output pickle and return 2 csv files. The training csv(90%) and the validation csv(10%).

run 'python SymbolNoising.py' to generate the training set and run 'python toCSVClassification.py' to create csv files.


### Training Example
#### input
```java
<L>
<L>
<L>
<L>
<L>

/**
 * ##### # ########### ## ##### ############ ####.
 * 
 * @###### (#### ####) 
 * @####### (# ####### ###### ## # ####)
 */
public class TableProgram
{
public static void main(String args[]
{
    System.out.println(""///////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\"""");
}
}       
```
#### output
  14



## EncoderDecoder
The WordEncoderDecoder.py takes a list of buggy programs as input and create 10 corrupted training samples. These samples will be saved as pickle. We use toCSV.py to generate the csv files.

### Example
#### input
```java
<L1>import java.util.*;
<L0>import java.io.*;
<E>import java.util.Scanner
<R0>
<R1>

```
#### output
import java.util.Scanner;
