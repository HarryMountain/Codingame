import numpy as np
nums = np.zeros((2, 2), dtype=int)
def bla(nums):
    nums[0, 0] += 1
bla(nums)
print(nums)
