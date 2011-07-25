:mod:`bbos.kernel.schedulers.fcfs` --- FCFS
=======================================================

.. automodule:: bbos.kernel.schedulers.fcfs

First-Come-First-Served algorithm is the simplest scheduling algorithm is the 
simplest scheduling algorithm. Processes are dispatched according to their 
arrival time on the ready queue. Being a nonpreemptive discipline, once a 
process has a CPU, it runs to completion. The FCFS scheduling is fair in the 
formal sense or human sense of fairness but it is unfair in the sense that 
long jobs make short jobs wait and unimportant jobs make important jobs wait.

.. autoclass:: FCFS
   :members:

