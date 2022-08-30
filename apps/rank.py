# %%
import numpy as np

# %% 52WEEK HIGH LOW RANGE PERCENTAGE
def percent_rank(arr, score, sig_digits=5):
    arr = np.asarray(arr)
    arr = np.round(arr, sig_digits)
    score = np.round(score, sig_digits)
    if score in arr:
        small = (arr < score).sum()
        return small / (len(arr) - 1)
    else:
        if score < arr.min():
            return 0
        elif score > arr.max():
            return 1
        else:
            arr = np.sort(arr)
            position = np.searchsorted(arr, score)
            small = arr[position - 1]
            large = arr[position]
            small_rank = ((arr < score).sum() - 1) / (len(arr) - 1)
            large_rank = ((arr < large).sum()) / (len(arr) - 1)
            step = (score - small) / (large - small)
            rank = small_rank + step * (large_rank - small_rank)
            return rank

# %%
if __name__ == '__main__':
    percent_rank()
