+++
title = 'Data Structures & Algorithms'
date = 2024-06-24T12:18:32-07:00
draft = true
tags = ['C++']
[editPost]
    URL = "https://github.com/fadli0029/fadeWrites/edit/main/content/posts/cpp_tips.md"
    Text = "Suggest Changes"
    appendFilePath = false
[params]
    comments = true
    ShowToc = true
    TocOpen = true
+++

In this post, I talk about algorihtms in general (quick select, quick sort, bucket sort, dp, djikstra, etc.) and data structs (heap, tries, etc.) and how to implement them in C++.

TODOS:

Algorithms:
- Sorting
  - Bubble Sort
  - Bucket Sort
  - Merge Sort
  - Quick Sort
  - Heap Sort
  - Quickselect/Hoare's Selection Algorithm
  - Counting Sort
  - Radix Sort
- Searching
  - Linear Search
  - Binary Search
  - Jump Search
  - Interpolation Search
  - Exponential Search
  - Fibonacci Search
  - Ternary Search
- Graph
- Tree
- Dynamic Programming
- Greedy
- Divide and Conquer
- Backtracking
- Bit Manipulation
- String Matching

Data Structures:
- Heap
- Fibonacci Heap
- Tries
- Linked List
- Stack
- Queue
- Hash Table
- Graph
- Tree
- Binary Search Tree
- AVL Tree
- Red-Black Tree
- B-Tree
- Segment Tree
- Fenwick Tree
- Disjoint Set
- Trie
- Suffix Tree
- Suffix Array
- K-D Tree
- Quad Tree
- Octree
- ...

# Algorithms

## Binary Search
The key or the power that vanilla binary search gives you is that given middle value, it tells you where you should go. For example, if your middle value now is x and target is bigger than x, binary search tells you to search for the answer to the right of the array, and so on.

Other variants of binary search problems where you can't just use vanilla binary search is created by taking away this power from you. How? The problems are created such that when you look at the middle value, you still don't know where you should go. i.e.: the requirement of sorted array is taken away thereby making vanilla binary search powerless and needs some tuning.

How do we still leverage the binary search algorithm then? Well, if you can somehow create an "environment" for the algorithem so that it is able to tell where to go given middle value, then you can run the binary search algo. and it will solve the problem. For example, the rotated array problem where we are given a sorted array that is rotated and we want to find the smallest element.

Before we solve this problem, let's take a look at a slightly simple problem to get used to creating an "environment" to deploy binary search algorithm.

Given an array nums of length n sorted in ascending order and a target x, find the smallest index y such that nums[y]>=x.

Let nums = [2, 3, 5, 6, 8, 10, 12] and x = 4, then we should output y = 2 bcoz 5 is the smallest element in nums that is >= x.

A normal binary search on this problem will work but require some tweaking. Basically, if mid satisfies nums[mid]>=x, keep looking to the left (since it's sorted we surely should look to the left as that will lead to numbers that are smaller than the current mid), in case there's any number that is smallest. The algo. is simple, just keep track of the current smallest value and update it if we found anything better. In the end we return this tracked value.

What we're inherently doing here is creating an "environment" for binary search to work on. What do I mean by that is we're inherently putting a label on each number in nums. Label T (True) for elements that satisfy the condition and F (False) for elements that do not satisfy the condition:

[2, 3, 5, 6, 8, 10, 12]
 F  F  T  T  T  T   T

So now binary search job is to find the first T, that's easy! If mid = T, go left. Else, go right. This is vanilla binary search isn't it!? Let me prove it to you:

Vanilla binary search says if mid > target, go left, else go right. The only difference is we use equality here instead of inequality. The point is, the power of binary search that got taken away is back: given middle value, it knows where to go.

IMPORTANT NOTE: I am not asking you to iterate the array `nums` and put these labels as that would defeat the purpose of binary search since that would make our complexity go to $O(n)$ instead of $O(\log n)$ with binary search. I am just trying to show you how we can create an "environment" for binary search to work on. i.e.: how would you modify the update conditions of the binary search algo. to inherently put these labels on the numbers.

Now, let's solve the rotated array problem again.

Given an array `nums` that may or may not be rotated and is sorted in ascending order, find the smallest element in `nums`.

Let nums = [6, 7, 9, 15, 19, 2, 3], so our output should be 2.

Okay how do we inherently put labels on the numbers in `nums` so that binary search can work on it?

1. The first step is to know what kind of label we want. In this case, we'd want to be able to distinguish the left sorted part of the array from the right sorted part of the array. So, we'd want to put a label T (True) (or LS if you like) on the left sorted part of the array and F (False) (or RS if you like) on the right sorted part of the array.

2. Now that we know what kind of label we want, how do we put it on the numbers? Well, we can put labels on the numbers based on the comparison between `mid` with the first element of the array and the last element of the array. If `mid` is greater than the first element of the array, then it's in the left sorted part of the array, otherwise False. So, we have the following labels:

[6, 7, 9, 15, 19, 2, 3]
 T  T  T   T   T  F  F

3. But is this correct? What about when the array is rotated n times, then the array is equivalent to the original unrotated array. So, for example [2, 3, 7, 9], it is not true anymore that if mid > first element of the array, then it's in the left sorted part of the array. Bcoz if we follow that rule, we'd get:

[2, 3, 7, 9]
 T  T  T  T

4. We can treat this edge case by an if-else condition. But it is better to revise our condition. What if we say the condition is if mid > last element of the array, then it's in the left sorted part of the array, otherwise False. So, we have the following same labels for the first example:

[6, 7, 9, 15, 19, 2, 3]
 T  T  T   T   T  F  F

And this for the second example:

[2, 3, 7, 9]
 F  F  F  F

5. Now with these labels, we can check for the first F in the array, and that's our answer. For sake of completion, let's see if this labelling technique gives the power of binary search back: if mid = T, go right, else go left to see if we can find a better answer. So, we can see that the power of binary search is back.

To sum up, the way of solving any kind of binary search problem, not just vanilla binary search problem, is to create this "environment" for the binary search algorithm to work on. This "environment" is created by putting labels on the numbers in the array based on some condition. The condition is such that given middle value, it knows where to go. This is the key to solving any binary search problem. If we were to summarize the steps to follow:

1. Will vanilla binary search work? If yes, then just run the algo. If not, then go to step 2.
2. We create an "environment" for binary search to work on by putting labels, so in this step we identify what label we want.
3. We put labels on the numbers in the array based on some condition. The condition is such that given middle value, it knows where to go.
3. Check for edge cases and revise the condition if necessary.
4. Run the binary search algorithm on the labelled array bcoz now given mid, we have a direction to tell the algo. where to go.

I wanna conclude this by quoting what Errichto (Competitive Programmer) said: "Think of Binary Search Problems in terms of prefixes of false and suffixes of true or the other way around, then you can find the boundary: the last true or the first false."

!!! The tip he gave is to put labels first and figure out want last true or first false. After putting these labels, then you figure out how to put the labels, i.e.: the condition.





# Data Structures
