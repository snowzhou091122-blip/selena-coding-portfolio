class SolutionTwoHashmaps:
    def isAnagram(self, s: str, t: str) -> bool:
        countS = {}
        countT = {}
        for c in s:
          if c in countS:
            countS[c]=countS[c]+1
          else:
            countS[c]=1
        for c in t:
          if c in countT:
            countT[c]=countT[c]+1
          else:
            countT[c]=1
        return countT==countS

class SolutionOneHashmap:
    def isAnagram(self, s: str, t: str) -> bool:
        countS = {}
        for c in s:
          if c in countS:
            countS[c]=countS[c]+1
          else:
            countS[c]=1
            
        for c in t:
          if c in countS:
            countS[c]=countS[c]-1
          else: 
            return False
          if countS[c]<0:
            return False
            
        for value in countS.values():
          if value != 0:
            return False
        return True
