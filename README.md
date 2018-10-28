## Path-Predictor
Path-Predictor is a tool developed for automatically generating worst-case inputs for programs with loops. Path-Predictor learns the worst-case program 
behaviour by executing the program with smaller inputs exhaustively using symbolic execution. Then it generalizes the worst-case behaviour to unseen larger
input sizes by synthesizing a set of generator models. Given a large input scale these models can be used to automatically generate the worst-case path condition
for that input scale. Worst-case path condition can then be solved using SMT solver to generate a concrete worst-case input.
