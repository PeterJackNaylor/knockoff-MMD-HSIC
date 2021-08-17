* * *

## Data simulations:

$X\in\mathbb{R}^{n\times p}$ where the sample size $n \in \left\{100, 500\right\}$ and feature size $p \in \left\{500, 5 .10^3\right\}$.
$X \sim \mathcal{N}(0_n, \Sigma)$ where $0_n$ is a zero vector of size $n$ and $\Sigma_{ij} = \frac{1}{2^{|i-j|}}$

## Building Y:

* * *

- Model 2.a: $Y=5 X_{1}+2 \sin \left(\pi X_{2} / 2\right)+2 X_{3} \mathbf{1}\left\{X_{3}>0\right\}+2 \exp \left\{5 X_{4}\right\}+\varepsilon$
- Model 2.b: $Y=3 X_{1}+3 X_{2}^{3}+3 X_{3}^{-1}+5 \mathbf{1}\left\{X_{4}>0\right\}+\varepsilon$
- Model 2.c: $Y=1-5 \left(X_{2}+X_{3}\right)^{3} \exp \left\{-5\left(X_{1}+X_{4}^{2}\right)\right\}+\varepsilon$
- Model 2.d: $Y=1-5\left(X_{2}+X_{3}\right)^{-3} \exp \left\{1+10 \sin \left(\pi X_{1} / 2\right)+5 X_{4}\right\}+\varepsilon$
    With $\varepsilon \sim \mathcal{N}(0, 1)$

* * *

## Knock off algorithm:

- if $n \in [1, 2, 3]$ do nothing.
- if $p < n /2$ no need for the screening step, we can construct the exact knock-off directly.
    In the other situations:
- if $d$ is incorrectly set, $d= n_2 / 2 - 1$

### Algorithm:

Input:

- $(X, y) \in \mathbb{R}^{n\times p} \times \mathbb{R}^{n\times q}$
- $\alpha \in [0, 1]$
- $p_1 \in [0, 1]$, relative percentage of the data set to be in fold 1. (algorithm parameter instead of $n_1$ directly)
- $n_1 = \text{int}(n \times p_1)$ ($p_1$ is given instead of $n_1$)
- $d$ such that $d < n_2 / 2$
- An associative measure $\mathcal{T}$, that can be $PC^2$ (taken from [authors code](https://github.com/TwoLittle/PC_Screen/blob/master/PC_screen.py)), $HSIC$ or $MMD$.

**Checks before starting:**

- if $n$ is large enough no need for splitting or screening, jump to knockoff step.
- Else, split data randomly into two according to $n_1$ and $n_2 = n - n_1$, use $(X^{(1)}, y^{(1)})$ in the screening step and $(X^{(2)}, y^{(2)})$ in the knockoff step.

#### Screening step

1.  $\forall j \in [1:p], \hat{\omega_j}^{(1)} = \mathcal{T}(X_j^{(1)}, y^{(1)})$
2.  Select top $d$ features, $\widehat{\mathcal{A}}_{1}= \left\{ j: \widehat{\omega}_{j}^{(1)} \text{is among the largest} \ d \right\}$

#### Knockoff step

1.  Keep $\widehat{\mathcal{A}}_{1}$ features from $X^{(2)}$, named $X^{(2)}_{\widehat{\mathcal{A}}_{1}}$, build exact knock off with *equicorrelated construction*, code taken from [authors code](https://github.com/TwoLittle/PC_Screen/blob/master/PC_screen.py).
2.  $\forall j \in \widehat{\mathcal{A}}_{1}$, $\widehat{W_j} = \mathcal{T}(X^{(2)}_{\widehat{\mathcal{A}}_{1}, j}, y^{(2)}) - \mathcal{T}(X^{(2)}_{\widehat{\mathcal{A}}_{1}, j}, y^{(2)})$
3.  $T_{\alpha}=\min \left\{t \in \mathcal{W}: \frac{1+\#\left\{j: \widehat{W}_{j} \leq-t\right\}}{\#\left\{j: \widehat{W}_{j} \geq t\right\}} \leq \alpha\right\}$ where $\mathcal{W}=\left\{\left|\widehat{W}_{j}\right|: 1 \leq j \leq p\right\} /\{0\}$
4.  $\widehat{\mathcal{A}}\left(T_{\alpha}\right)=\left\{j: \widehat{W}_{j} \geq T_{\alpha}, 1 \leq j \leq p\right\}$
5.  If $\widehat{\mathcal{A}}\left(T_{\alpha}\right)$ is empty we return the empty set        $\widehat{\mathcal{A}}_{1}$ ~~or the full set of features.~~

* * *

## Questions & remarks

1.  In the [authors code](https://github.com/TwoLittle/PC_Screen/blob/master/PC_screen.py), we notice that the $PC$ function allows to take in input $X$ a matrix and not a feature column as we expected, is there a situation where we would feed multiple feature columns to the association measures $\mathcal{T}$?
2.  In 5. of the knockoff step, $\widehat{\mathcal{A}}\left(T_{\alpha}\right)$ could be empty, if all knockoff variables are better then the originals. Should we return an empty set or the full set?
3.  Should we use a "recall" metric? To compare methods and checks if the good features are correctly selected? In the simulation case, this would be to count how many times the first 4 features are selected.
4.  How should we control the FDR? After using the procedure to select the appropriate features should we use a classifier, such as a random forest to compute the FDR and estimate it? How does this work in the regression setting?
    \-\-\- > $\mathrm{FDR}=\mathbb{E}\left[\frac{\#\left\{j: \beta_{j}=0 \text { and } j \in \hat{S}\right\}}{\#\{j: j \in \hat{S}\} \vee 1}\right]$
5.  Is it ok to remove the screening step if $n$ is large enough? Even tho we might not be dealing with this case, it is a possible situation, and scikit learn test's this situation.

* * *

## TODOs:

- [ ] Implement associative measure *HSIC* and *MMD*.
- [ ] Implement the follow up for controlling the FDR rate
- [ ] Find a correct database from [UCI](https://archive-beta.ics.uci.edu/)