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


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __str__(self):
        """String representation of the linked list starting from this node"""
        result = []
        current = self
        while current:
            result.append(str(current.val))
            current = current.next
        return " -> ".join(result) + " -> None"

# def print_linked_list(head):
#     """Alternative function to print linked list"""
#     current = head
#     values = []
#     while current:
#         values.append(str(current.val))
#         current = current.next
#     print(" -> ".join(values) + " -> None")

head = ListNode(10)
head.next = ListNode(20)
head.next.next = ListNode(30)

# Now this will print the linked list nicely
print(head)

# # Alternative way using the function
# print("Using function:")
# print_linked_list(head)
