#!/usr/bin/python3.6

import subprocess as sp
import os
benches = ["a2time01", "cacheb01", "bitmnp01", "mcf", "libquantum"]
branch_predicts = ["LocalBP", "BiModeBP", "MultiperspectivePerceptron8KB", "MultiperspectivePerceptron64KB", "TournamentBP"]
os.chdir("../gem5")
for bench in benches:
    for branch_predict in branch_predicts:
        command =  f"build/ARM/gem5.opt --stats-file=/home/comparch/Documents/teamgrace562/hw2/benchmarks/{bench}-{branch_predict}-stats configs/example/se.py --caches --l1i_size=32kB --l1i_assoc=4 --l1d_size=32kB --l1d_assoc=4 --cacheline_size=64 --cpu-clock=1.6GHz --cpu-type=O3_ARM_v7a_3 -n 1 --maxinsts=100000000 --bench {bench} --bp-type={branch_predict}"
        print(command)
        print(sp.getoutput(command))

    
