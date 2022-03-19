# Variables
ccode = A list of buggy programs.

## Classification

The WordClassification.py takes a list of buggy programs as input and break the file into 10 corrupted training samples. The output will be saved in a pickle.
The CsvClassifier.py takes the pickle from WordClassification and return 2 csv files. The training csv(90%) and the validation csv(10%).

### Example
#### input
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

#### output
  14



## EncoderDecoder
The WordEncoderDecoder.py takes a list of buggy programs as input and create 10 corrupted training samples. These samples will be saved as the csv files.
### Example
#### input
<L6>public class HollePrinter
<L5>{
<L4> public static void main(String[] args)
<L3> {
<L2> String blah = (""Hello, World!"");
<L1> String blah2 = blah.replace(""e"", ""a"");
<L0> String blah3 = blah2.replace(""o"", ""b"");
<E> String blah4 = blah3.replace(""a"", """");
<R0> String finalblah = blah4.replace(""b"", ""e"");
<R1> System.out.println(finalblah);
<R2> }
<R3>}
<R4> 
<R5>

#### output
String blah4 = blah3.replace(""a"", ""o"");
