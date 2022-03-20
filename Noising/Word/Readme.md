# How to use

## Important variables
ccode = A list of buggy programs.
ccode is a list of string. It is a list of error-free java programs. Use this variable to store the input files.

## Classification

The WordClassification.py takes a list of buggy programs as input and break the file into 10 corrupted training samples. The output will be saved in a pickle.
The CsvClassifier.py takes the pickle from WordClassification and return 2 csv files. The training csv(90%) and the validation csv(10%).

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
The WordEncoderDecoder.py takes a list of buggy programs as input and create 10 corrupted training samples. These samples will be saved as the csv files.
### Example
#### input
```java
<L1>        System.out.print(" 1 ");
<L0>        System.out.print(" 2 ");
<E>        System.out.(" hello ");
<R0>        System.out.print(" 3 ");
<R1>       System.out.print(" 4 ");
```
#### output
        System.out.print(" hello ");
