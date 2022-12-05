# KTTK
A Python tool to build initial guess from fragments for Gaussian

Imagine the following case: you have a complex A--B--C--..., and you need to generate a UHF/UKS wavefunction in a controllable manner. Just an example, imagine you are facing a system with the formula FeCp2---Cl, and you may want to try if one can converge to both the FeCp2+(radical) Cl- state and the FeCp2 Cl(radical) state. It is a possible way to use the guess=fragment=2 feature in Gaussian, but it will be a disaster if Gaussian cannot handle the fragment correctly. In this case, if you use wB97xD functional, you will find that the wavefunction converged for FeCp2+ fragment using Gaussian is unstable. Because guess=fragment cannot be used along with stable=opt, guess=read, etc., you will have to run stable=opt for the whole system, which is quite annoying when the system is large and/or many similar systems are to be calculated. If you want to calculate FeCp2 Cl, FeCp2 I and FeCp2 I3, you will not want to repeat the workflow (1) generate initial guess (unstable) using guess=fragment=2, (2) stable=opt guess=read for each of them, especially when you have already had the stable wavefunction of FeCp2+.


In this case, a more flexible tool for combining fragment wavefunctions is demanded, and this is how KTTK comes.


KTTK is a Python tool to build wavefunctions from separated fragments. It is composed by two programs: kttk_mixer.py and kttk_separator.py. The core functions are in the kttk_mixer.py. It reads fchks for the fragments, combine them, and output an fchk file for the whole system. If you have already had all of the fragment fchk files, which follow exactly the atomic order in the whole system, it is good and you just need kttk_mixer.py to combine them. If not, kttk_separator.py could help. The geometry recorded in a gjf file for the whole system can be divided into fragments and the corresponding gjf files can be automatically generated.

Here is an example, for an arbitarily constructed FeCp2 Cl system. If we have a gjf file for the whole system, named dd.gjf:

```
%chk=dd_mixed.chk
%mem=24GB
%nprocshared=24
# uwb97xd nosymm guess=read g09default scf=xqc

TC

0 2
 H                 -4.49778100    0.71661800    1.28221500
 C                 -5.31465600    0.03561600    1.04781000
 C                 -5.54736900   -0.59233100   -0.21012500
 C                 -6.30355300   -0.42048600    1.95688900
 C                 -6.68257300   -1.44779300   -0.06983100
 H                 -4.95473500   -0.45583000   -1.11330700
 Fe                -5.16530800   -2.06921600    1.17881100
 C                 -7.14298200   -1.33867000    1.27525600
 H                 -6.36571000   -0.16448200    3.01381400
 H                 -7.11211600   -2.08084700   -0.84501900
 H                 -7.97510600   -1.88770500    1.71480600
 C                 -3.39299100   -2.94799800    0.61681100
 C                 -4.45139900   -3.89480800    0.47859800
 C                 -3.31231500   -2.58327100    1.99432000
 H                 -2.76848700   -2.56194300   -0.18729600
 C                 -5.00888300   -4.11958000    1.76821100
 H                 -4.79012500   -4.34732700   -0.45175100
 C                 -4.30458100   -3.31729600    2.69971200
 H                 -2.62319900   -1.85936300    2.42673500
 H                 -5.86499300   -4.75446900    1.99190800
 Cl                -2.04406600    0.01490100   -1.58085900
 H                 -4.52805800   -3.22843700    3.76207200
```

Then run python3 kttk_separator.py (sto-3g is used for a rapid example):
```
$ python3 kttk_separator.py
Input the gjf file for your whole molecule:
dd.gjf
Input your atom indexes for each fragment. E.g. 1-5,10,12-14
Empty line to end the input, and the unassigned atoms will be automatically assigned into a new fragment.
1-20,22

Input the charge and multiplicity for each fragment, respectively.              Empty line to end the input. E.g. 0 1
1 2
-1 1

Input the kwds. Do not write guess=xxx.
wb97xd sto-3g g09default
Now the gjf files for each fragment is outputted. Modify them to adapt to your task, run,  and use kttk_mixer.py to build the combined fchk.
```

Then you will have three files (of course you can define more fragments if needed): dd_1.gjf (FeCp2+), dd_2.gjf (Cl-), and dd_mixed.gjf (the whole system, with the keywords inputted above, and exactly the same atomic order with the fragments). Have a check on the keywords, add anything you want. For example, if the FeCp2+ has been converged to a stable wavefunction in another calculation, write guess=read to read it in dd_1.gjf. Then run the tasks for each fragment, and you will have dd_1.fchk and dd_2.fchk.

Then run tkkt_mixer.py:

```
$ python3 kttk_mixer.py
Input the fragment fchk files, and an empty line to end the input.
dd_1.fchk
dd_2.fchk

Input the flag (1 or -1) for each fragment, respectively. -1 to flip the spin. E.g. 1 -1 1
1 1
Where to save the output fchk file? dd_mixed.fchk
```

It is done. Now dd_mixed.fchk contains the initial orbitals formed by FeCp2+(radical) and Cl-, based on the fragment orbitals inputted above. It can be unfchked and read by a Gaussian job.

In this case, by changing the two fragments into FeCp2+(radical) / Cl- and FeCp2 / Cl(radical) and using kttk_mixer.py, two different wavefunctions can be converged into. The first one features spin density completely on Fe, and the other one features a Cl atom with a moderate radical nature.

Note: Always be aware of what you are doing. You may want to control what kind of wavefunction is converged to, but it should rely on a good understanding of the electronic structure and the quantum chemical principles.
