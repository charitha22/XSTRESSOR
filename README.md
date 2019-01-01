# XSTRESSOR
XSTRESSOR is a tool developed for automatically generating worst-case inputs for programs with loops. XSTRESSOR learns the worst-case program 
behaviour by executing the program with smaller inputs exhaustively using symbolic execution. Then it generalizes the worst-case behaviour to unseen larger
input sizes by computing a set of generator models. These generator models can be used to extrapolate the worst-case path condition
for a given large input scale. Worst-case path condition can then be solved using SMT solver to generate a concrete worst-case input.

Fore more details have a look at our ICST paper.
C. Saumya, J. Koo, M. Kulkarni, and S. Bagchi, “XSTRESSOR: Automatic Generation of Large-Scale Worst-Case Test Inputs by Inferring Path Conditions,” To Appear at the 12th IEEE International Conference on Software Testing, Verification, and Validation (ICST), Apr. 2019.

# Running the benchmarks
First you need to have follwing programs installed in your system.
1. python
2. NumPy
3. z3

