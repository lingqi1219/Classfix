## Variables
ccode = A list of buggy programs.

## Classification

The SymbolNoising.py takes a list of buggy programs as input and break the file into 10 corrupted training samples, saves in a pickle.
The toCSVClassification.py takes the outputpickle return 2 csv files. The training csv(90%) and the validation csv(10%).

### Example
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
The WordEncoderDecoder.py takes a list of buggy programs as input and create 10 corrupted training samples. These samples will be saved as pickle. Use toCSV.py to generate the csv files.

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
