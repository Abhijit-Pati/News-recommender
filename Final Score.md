# Final Score







$$\text{if ip(wid) < 20:}$$
    $$\text{then choose 9 random clusters}$$
    $$\text{Choose a random article from each}$$
    $$\text{Choose wildcard}$$
    $$\text{Randomise the ranks}$$
$$\text{else (if ip(iid) }\geq20):$$
	$$\text{Argsort 9 by ucfscore}$$
	$$\text{Choose wilcard}$$
	$$\text{Rank-rand}$$

$$\text{Scoring_list (scored_array), top_n) - Sort it}$$
$$\text{Scored_array has structure (score) original ID}$$
$$\text{Calculate u, $\sigma$ and top-n scores}$$
$$\text{Replace score by (score-u)/$\sigma$ }$$
$$\text{New array has sttructure [(score-u)/$\sigma$] original ID}$$
$$\text{Make a 5000-D vector with scoes}$$

