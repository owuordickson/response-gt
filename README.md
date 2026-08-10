[![Downloads](https://pepy.tech/badge/rgtlib)](https://pepy.tech/project/rgtlib) [![Downloads](https://pepy.tech/badge/rgtlib/week)](https://pepy.tech/project/rgtlib)
![Dependents](https://badgen.net/github/dependents-repo/owuordickson/response-gt/?icon=github)
![Dependents](https://badgen.net/github/license/owuordickson/response-gt/?icon=github)

# ResponseGT
ResponseGT is a software that computes electrical/mechanical flow within a graph network.

## 1. Prerequisites
This software requires Python version 3.12. Install it from [here](https://www.python.org/downloads/).

## 2 Installation

The software can be installed via ```pip``` or ```Conda```.

### 2a. Install via pip

To install the software via ```pip```:

```bash
pip install rgtlib
```

### 2b. Install via Conda

To install the software via ```Conda```:

```bash
conda install -c conda-forge rgtlib
```

## 3. Usage

To run the GUI application, please follow these steps:

* Open a terminal application such as ```CMD``` and execute the following command:

```bash
ResponseGT
```


## 4. Computations

This library provides computational methods for evaluating **AC Response** and **Mechanical Response** on graph-based network models.

### AC Response

The AC Response computation solves the sparse linear system associated with the graph network to obtain the unknown node responses, denoted by (u_b).

Two sparse linear-system solvers are supported:

* **Direct sparse solver:** `scipy.sparse.linalg.spsolve`
* **Algebraic Multigrid (AMG) solver:** `pyamg.smoothed_aggregation_solver`

The solver can be selected using the `use_amg` option.

When `use_amg=True`, the system is solved using a **Smoothed Aggregation Algebraic Multigrid** hierarchy:

```python
import pyamg

ml = pyamg.smoothed_aggregation_solver(q_mat)
ub_list = ml.solve(p_mat, tol=1e-10)
```

When `use_amg=False`, the system is solved using SciPy's direct sparse solver:

```python
from scipy.sparse.linalg import spsolve

ub_list = spsolve(q_mat, p_mat)
```

Here, `q_mat` represents the sparse system matrix and `p_mat` represents the corresponding right-hand side. The resulting `ub_list` contains the computed node responses.

The AMG solver is particularly useful for large sparse graph networks where iterative multilevel methods can provide improved computational scalability compared with a direct sparse factorization.

### Mechanical Response

The library also provides methods for computing the **Mechanical Response** of the graph network. The mechanical computation evaluates the response of the network based on its graph topology and associated mechanical properties.

Both AC and Mechanical Response computations operate directly on the graph representation, allowing the resulting physical responses to be analyzed in relation to the underlying network structure.


## Contributors ✨

Thanks go to these incredible people:

<a href="https://github.com/owuordickson/response-gt/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=owuordickson/response-gt" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
