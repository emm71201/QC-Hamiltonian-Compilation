## QC Hamiltonian Compilation

### PURPOSE:  Compile a quantum circuit of the *Hamiltonian Time Evolution Operator*

### Author: EDISON MURAIRI [(LinkedIn Profile)](https://www.linkedin.com/in/edison-murairi/)

### Citing: 
<code>
@article{PhysRevD.106.094504, 
  title = {How many quantum gates do gauge theories require?}, 
  author = {Murairi, Edison M. and Cervia, Michael J. and Kumar, Hersh and Bedaque, Paulo F. and Alexandru, Andrei}, 
  journal = {Phys. Rev. D}, 
  volume = {106}, 
  issue = {9}, 
  pages = {094504}, 
  numpages = {13}, 
  year = {2022}, 
  month = {Nov}, 
  publisher = {American Physical Society}, 
  doi = {10.1103/PhysRevD.106.094504}, 
  url = {https://link.aps.org/doi/10.1103/PhysRevD.106.094504} 
}
</code>


### QUICK TUTORIAL
This tutorial walks the user through using this compiler with the default parameters. <br> 
- __Step 0__:
> Expand the Hamiltonian as a linear combination of Pauli Operators (Pauli Strings).
- __Step 1__:
> Prepare the Hamiltonian File:
The Hamiltonian file is a CSV file. Each line representts a Pauli operator and its coefficient. <br>
Therefore, each line has two columns:
> > The first column is a Pauli operator writen as a string of the Pauli matrices <br>
> > The second column is just the coefficient of the Pauli operator (with the minus sign if necessary). <br>
> > The first and second columns are separated by a comma and there is no space before or after the comma. 

__Example__: The Hamiltonian file: *sigma.csv* 
<code>
ZZII,-0.25 <br>
ZIII,-0.25 <br>
IZII,-0.25 <br>
IIZZ,-0.25 <br>
IIZI,-0.25 <br>
IIIZ,-0.25 <br>
IYIY,0.3 <br>
YZYZ,0.3 <br>
YXYX,0.3 
</code>

- __Step 2__: Run the compiler <br>
> Using the terminal, navigate to the *QC_Hamiltonian_Compilation* folder <br>
> Type the command _python3 compiler.py -f \<path to the Hamiltonian file\>  -o <\output directory\> -dt <\dt\> <br>
> If no -o is given, then the circuit will be compiled and a folder called RESULTS_\<input_file\> will be created in the current directory. <br>
> If no -dt is given, then the circuit will be a parametric circuit with parameter called dt. <br>
> In the results folder, there is a file __QC.qpy__. It contains the final quantum circuit. <br>

- __Step 3__: Reading the QC.qpy file  <br>
> See the file <\playground.py\> for an example of how to load the circuit. <br>
> One can copy the circuit data with a fixed parameter value (dt) to a qasm file, which can be read by most platforms.

### ADVANCED TUTORIAL

#### SPECIFY THE GROUPING STRATEGY:
One step of the compiler is to group the Pauli strings into clusters (sets) in which all the Pauli strings commute. 
In principle, it is desirable to use a few clusters as possible. <br>

The grouping is done via graph coloring. The coloring strategies (as implemented in NETWORKX) available are 
- DSATUR: Default <br>
- largest_first <br>
- random_sequential <br>
- smallest_last <br>
- independent_set <br>
- connected_sequential_bfs <br>
- connected_sequential_dfs <br>
- saturation_largest_first <br>

To specify the stratgy, add the parameter *-g \<name_of_the_strategy\>* when running the compiler. <br>
For example, to group the Pauli strings with the *indepndent_set* strategy, type the command: <br>
> > *python3 compiler.py -f \<path to the Hamiltonian file\>  -o \<output_file\> -g independent_set* <br>


#### VIEWING THE INTERMEDIATE RESULTS:
> The intermediate results are stored in the output directory. <br>
> There is a folder with name starting with *Cluster_* for each set of commuting Pauli strings. <br>
> Each Cluster Folder contains 4 files:
- __commuting_pauli_strings.npy__: The list of the Pauli strings in this cluster. <br>
> > Extract this list using NUMPY LOAD <br>
> > Import the Module pstring provided by our codes. Print the Pauli strings. <br> 
<img src="examples/print_commuting_paulis.jpg" alt="Alt text" title="Print the Commuting Paulis Example">

- __diagonalized_pauli_strings_tableau.npy__:
> > This file contains the diagonalized Pauli strings in Tableau Representation: X, Z, S, Coefs. <br>
> > - X: Contains only 0 (since the Pauli strings are diagonal). <br>
> > - Z: Each row of Z is a Pauli string. 0 means the Pauli matrix is the identity. 1 means the Pauli matrix is the z pauli matrix. <br>
> > - S: Each row of S contains the sign of the Pauli string. 0 means the sign is + (plus) and 1 means the sign is - (minus).
> > - Coefs: Each row contains the absolute value of the Coeficient of the Pauli string.
<img src="examples/diag_tableau_example.jpg" alt="Alt text" title="Read the Diagonalized Paulis Example">

_ **diagonalizing_circuit.qpy**: The quantum circuit of the unitary operator that simultaneously diagonalizes these commuting Pauli strings. 
> See the file <\playground.py\> for how to load the circuit.

_ __time_evolution_circuit.qpy__: The circuit of the time evolution operator of the diagonalized Pauli strings. 
> See the file <\playground.py\> for how to load the circuit.
