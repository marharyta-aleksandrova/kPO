# *k*-Pareto Optimality-Based Sorting with Maximization of Choice

This directory contains the code in ``Python`` for the paper "*k*-Pareto Optimality-Based 
Sorting with Maximization of Choice", [preprint is available here](https://arxiv.org/abs/2201.08206).

To generate images demonstrating different characteristics of sorting by
*k*-Pareto optimality, check `plots-for-paper.ipynb` notebook.
Alternatively, use the following scripts:

1. `plotting_scripts/selections_40pct.py` - generation of *Figure 5:  Selections of the best 40% according to different sorting criteria*.
2. `plotting_scripts/diversity_vs_area.py` - generation of *Figure 6:  Fraction of the best elements and diversity*.
3. `plotting_scripts/rarification.py` - generation of *Figure 8a* from Annex with rarefication example.
4. `plotting_scripts/trade_off.py` - generation of *Figure 8b* from Annex with trade-off and cone-based relation example.
5. `plotting_scripts/PO_whisker.py` - generation of *Figure 12* from Annex with a selection obtained for sorting by Pareto fronts and $k$-Pareto optimality.
6. `wealthy_countries` - data and analysis for *Figure 16* from Annex (wealthy and non-wealthy states).


To test the proposed genetic optimization algorithms *PO-count* and *PO-prob*, 
use `Knapsack-k_Pareto_optimality.ipynb`.

Check the code in `deap/tools/emo.py` for the implementations 
of *PO-count* (`sortPO()`) and *PO-prob* (`sortPOprob()`).

## Requirements:
- use the version of `deap` from the current repository,
- `numpy`,
- `matplotlib`,
- `jupyter`,
- `pandas`,
- `tikzplotlib`, (required only to generate plots in `tikz` format)
- `scipy`,
- `sklearn`
- `Java` for the efficient calculation of hypervolume, see `Hypervolume.java`.
