# Newground 3 (Heuristic Splitter)

# Installation

We provide an anaconda and a pypi package, which works for Unix with Python version 3.12.
This is the easiest way to install newground (we presuppose that `conda` is already installed):
```
conda create -n newground-test-arena thinklex::newground
conda activate newground-test-arena
```

Sometimes conda requires you to specify the conda-forge channel for clingo, then try the following:
```
conda create -n newground-test-arena -c conda-forge clingo thinklex::newground
conda activate newground-test-arena
```

## Running a first file:

```
mkdir newground_test
cd newground_test
ln -s $(whereis gringo | cut -d ' ' -f2) ./gringo
```

Then create the `test3.lp` file:
```
a(1).
b(X) :- a(X).
```

By using `newground test3.lp` the output should be:
```
asp 1 0 0
1 0 1 1 0 0
1 0 1 2 0 0
4 4 a(1) 0
4 4 b(1) 0
0
```

## Compile from scratch

1. Clone the repository
2. Goto the src folder
3. Hit `python -m build`
4. Then `pip install .`

If this does not work, try:
```
python start_heuristic_splitter.py
```

If this does not work as well you probably need to compile the Cython and C code by hand:
```
make compile-heuristic-cython-c
make compile-nagg-cython
```
After that using `python start_heuristic_splitter.py` should work.

# Newground3: Advanced Grounding for ASP

**Prototype Status:**  
Newground3 is a prototype developed for alleviating the grounding bottleneck.
It demonstrates new techniques for grounding in Answer Set Programming (ASP).
It is mainly intended for research and testing purposes.
Currently, it works only on Linux systems and may not be fully reliable or polished for other operating systems or production use.

If you don't manage to get it working please open an issue, or write me (alexander.beiser@tuwien.ac.at) an email!

## Overview

Newground3 builds on the Body-Decoupled Grounding (BDG) framework to address the grounding bottleneck in ASP, and is the successor of Newground, and NaGG. It includes:
1. **Hybrid Grounding:** Combines traditional semi-naive grounding with BDG.
2. **Automated Hybrid Grounding:** Uses heuristics to decide when BDG is most effective.
3. **FastFound:** Improves grounding for normal ASP programs (saturation method in prototype).
4. **Lazy-BDG:** Handles cyclic and non-tight rules by shifting some effort to the solving phase (unfound-set method in prototype).

Experiments show that Newground3 performs better than grounders like `gringo` and `idlv` on benchmarks with grounding-heavy scenarios.

---

## Usage

Run Newground3 using:

```bash
python start_heuristic.py [options] [files]
```

### Synopsis:

```
usage: Newground3 [files]

positional arguments:
  files

options:
  -h, --help            show this help message and exit
  --grounding-strategy {full,non-ground-rewrite}
                        Decide whether Newground3 shall be used as a full grounder (full) or in a non-ground rewrite mode (non-ground-rewrite).
  --sota-grounder {gringo,idlv}
                        Decide which state-of-the-art (SOTA) grounder to use ('./gringo' or './idlv.bin' must be present in same directory).
  --output-type {standard-grounder,string,benchmark}
                        For the full grounder output in specific format.
  --debug               Print debug information.
  --enable-logging      Enable additional logging information, e.g., if BDG was used.
  --logging-file LOGGING_FILE
                        Path to the logging file (--enable-logging must be supported as well). Default a file in logs/<FIRST_FILE_NAME>-<CURRENT-DATE-TIME>.log is generated.
  --tw-aware            Use treewidth aware rewritings for rule decomposition (lpopt tool).
  --treewidth-strategy {networkx}
  --cyclic-strategy {use-sota,unfound-set,level-mappings}
  --foundedness-strategy {heuristic,guess,saturation}
                        Decide which BDG version to use - heuristic decides the smalles grounding size automatically, SATURATION prefers FastFound, and GUESS prefers the standard foundedness check.
```



---

## Examples

We provide you with two very small example files: `test.lp` and `test_2.lp`, and the respective output in `test_output.lp` and `test_2_output.lp`:

```
newground --grounding-strategy=non-ground-rewrite test.lp
```


```
newground --grounding-strategy=non-ground-rewrite test_2.lp
```


---

## Known Limitations

- **Linux Only:** This prototype has been tested only on Linux and may not work on other systems.
- **Prototype Status:** The software is experimental and not ready for production.

---


# Acknowledgements

## Relevant Papers

1. V. Besin, M. Hecher, and S. Woltran, “Body-decoupled grounding via solving: A novel approach on the ASP bottleneck”, in IJCAI22, 2022, pp. 2546–2552. DOI: 10.24963/ijcai.2022/353.
2.  A. G. Beiser, M. Hecher, K. Unalan, and S. Woltran, “Bypassing the ASP bottleneck: Hybrid grounding by splitting and rewriting”, in IJCAI24, 2024, pp. 3250–3258. DOI: 10.24963/ijcai.2024/360.

## Relevant Theses

1. V. Besin, “A novel method for grounding in answer-set programming”, Master’s Thesis,
TUWien, 2023.
2. K. Unalan, “Body-decoupled grounding in normal answer set programs”, Bachelor’s
Thesis, TUWien, 2022.
3. A. G. Beiser, “Body-decoupled Grounding for Answer Set Programming extended with
Aggregates”, Bachelor’s Thesis, TUWien, 2023.
4. A. G. Beiser, "Novel Techniques for Circumventing the ASP Bottleneck", Master's Thesis, TUWien, 2025.

## Earlier Versions

Newground (version 1) was the original version, followed by NaGG.
These prototypes can be downloaded from the branches `ijcai22` and `ijcai24-NaGG`.
NaGG is a specialized version of [Newground](https://github.com/alexl4123/newground).
For details and general information about the earlier prototype see the [documentation](https://www.dbai.tuwien.ac.at/proj/hypar/newground/index.html) page of Newground, or the respective documentation folder.
Also check out [Newground](https://github.com/viktorbesin/newground).

