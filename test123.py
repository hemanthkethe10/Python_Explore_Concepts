s = "pwwkew"

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pairs = []
        for index,val in enumerate(s):
            temp = []
            temp.append(val)
            for index2,val2 in enumerate(s[index+1:]):
                if val2 not in temp:
                    temp.append(val2)
                else:
                    pairs.append(temp)
                    break
            pairs.append(temp)
                
        max_length = 0
        for pair in pairs:
            if len(pair) > max_length:
                max_length = len(pair)

        return max_length

def longest_substring_sliding_window(s):
    """Find longest substring without repeating characters using sliding window."""
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If char is already in window, shrink from left until it's removed
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current char to window
        char_set.add(s[right])
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length

print(longest_substring_sliding_window(s))
