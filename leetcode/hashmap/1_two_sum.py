from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for i, num in enumerate(nums):
          cut=target-num
          if cut in hashmap:
              return [hashmap[cut],i]
          hashmap[num]=i

