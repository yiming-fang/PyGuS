# PyGuS
Simple interpreter for SyGuS-based program synthesis in Python

## Motivation
SyGuS is a popular standard for formulating and solving constraints in the SMT language, and there are many state-of-art open source SMT solvers, such as CVC5. Although many solvers do provide APIs to facilitate specifying constraints in popular programming langauges, including C++, Java, Python, they do not provide a way to translate the SyGuS synthesized programs from the SMT language back into directly executable code.

PyGuS is a simple tool that makes use of CVC5's python API to specify and solve SMT queries, and contains an SMT interpreter that translates the resulting SMT function back into directly exectuable python code. This allows users to write constraints for their functions in Python, and get the desired functions back in Python, using the state-of-art solvers for end-to-end program synthesis without leaving Python land.

## How to use
The test files in /tests directory provides an example usage of PyGuS. The constraint specification and solving use CVC5's APIs. The `interpret_smt` function translates a SyGuS-synthesized function into a Python function definition. Lastly, the resulting SyGuS functions are written to the `smt_output` directory, and the Python functions are written to the `py_output` output directory.

To see PyGuS at play, first make sure the Python path is set properly:
``` 
export PYTHONPATH="${PYTHONPATH}:path-to-local-pygus-directory"
```

Then, temporarily remove the output files:
```
rm tests/smt_output/*.smt
rm tests/py_output/*.py
```
Now, run the tests and see that they properly re-populate the output files:
```
python tests/test1.py
python tests/test2.py
python tests/test3.py
```
