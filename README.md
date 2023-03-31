# PyGuS
Simple interpreter for SyGuS-based program synthesis in Python

## Motivation
SyGuS is a popular standard for formulating and solving constraints in the SMT language, and there are many state-of-art open source SMT solvers, such as CVC5. Although many solvers do provide APIs to facilitate specifying constraints in popular programming langauges, including C++, Java, Python, they do not provide a way to translate the SyGuS synthesized programs from the SMT language back into directly executable code.

PyGuS is a simple tool that makes use of CVC5's python API to specify and solve SMT queries, and contains an SMT interpreter that translates the resulting SMT function back into directly exectuable python code. This allows users to write constraints for their functions in Python, and get the desired functions back in Python, using the state-of-art solvers for end-to-end program synthesis without leaving Python land.
