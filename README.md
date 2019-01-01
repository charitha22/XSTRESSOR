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

Add XSTRESSOR directory to `PYTHONPATH` environment variable. 
```
export PYTHONPATH=$PYTHONPATH:<path_to_XSTRESSOR_directory>
```
Then from any benchmark or cases study directory run,
```
python <program_name>_model.py <INPUT_SCALE> 
```
This command generates a worst-case input for the specified `INPUT_SCALE`, also shows the time spent in each stage of the XSTRESSOR prediction algorithm.
For the insertion-sort benchmark the output looks like,
```
~/workspace/path-predictor/benchmarks/isort$ python isort_model.py 100
INFO : This program has 1 symbolic predicates
INFO : Generating a test case for scale 100
INFO : Satisfiability : sat
Model build time =  0.106421947479
Prediction  time =  1.66337919235
```
*Model build time* is the time spent for computing XSTRESSOR's generator models using the small-scale worst-case inputs. Note that this time does not include 
the time spent in exhaustive symbolic execution.

*Prediction time* is the time spent for extrapolating the large-scale worst-case path condition and solving it to generate a concrete worst-case input.


