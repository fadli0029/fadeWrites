+++
title = 'C++ Tips and Tricks'
date = 2024-06-24T12:18:32-07:00
draft = false
tags = ['C++']
[editPost]
    URL = "https://github.com/fadli0029/FadeWrites/edit/main/content/posts/cpp_tips.md"
    Text = "Suggest Changes"
    appendFilePath = false
[params]
    comments = true
    ShowToc = true
    TocOpen = true
+++

In this post, I will share some tips and tricks that I have learned while working with C++. Most of these tips are on optimization and performance improvement. I hope you find them useful. This post is useful to go through every once in a while, especially when you're rusty with C++.

## Dealing with `std::vector`

### Always use `reserve` when you know the size of the vector

```cpp
// Reserve space for 1000 elements.
// v[i] will be an empty object if v[i] has not been assigned a value.
std::vector<T> v;
v.reserve(1000);

// Reserve space for 1000 elements.
// v[i] will be assigned the default value.
std::string default_value = "default";
std::vector<std::string> v_strings(1000, default_value);
```

This is due to the way `std::vector` works. When you push an element into a vector, it checks if the current capacity is enough. If not, it allocates a new memory block, copies the elements, and deallocates the old memory block. This can be very expensive if you are pushing a lot of elements into the vector. By using `reserve`, you can avoid this overhead. Note that the same can be achieved by specifying the size in the constructor: `std::vector<int> v(1000);`.

As you can already tell from the example above, the biggest difference between `reserve` and calling the constructor to specify the vector size at construction is that `reserve` does not initialize the slots in the buffer with anything so you shouldn’t reference indexes where you haven’t already put something because they will be uninitialized. On the other hand, when you specify the size in the constructor, each slot is initialized with an empty object or the default value specified in the second argument of the constructor.

### Put pointers in `std::vector` instead of objects

```cpp
// modern C++

class Foo {
    // ...
};

int main {
    // --------------------------------------------------------------------
    // Vector creation and object insertion.
    std::vector<std::unique_ptr<Foo>> v;
    v.push_back(std::make_unique<Foo>(/* constructor args */));
    v.push_back(std::make_unique<Foo>(/* constructor args */));
    // ...
    // --------------------------------------------------------------------

    // Do something with the objects.

    // The objects will be automatically deleted when the vector goes out of scope.
    return 0;
}

// older C++

int main {
    // --------------------------------------------------------------------
    // Vector creation and object insertion.
    std::vector<Foo*> v;
    v.push_back(new Foo(/* constructor args */));
    v.push_back(new Foo(/* constructor args */));
    // ...
    // --------------------------------------------------------------------

    // Do something with the objects.

    // --------------------------------------------------------------------
    // Typical pipeline to delete the objects when you're done.
    for (std::vector<Foo*>::iterator it = v.begin(); it != v.end(); ++it) {
        delete *it;
    }
    v.clear(); // Purge the contents so no one tries to delete them again.
    // --------------------------------------------------------------------

    return 0;
}
```

Doing this will reduce copy overhead. This is because an `std::vector` or any other standard libary container __do not actually stores the object itself__. Instead, it stores a copy of the object. *This means that each time you put something in a vector, you aren’t really “putting” it anywhere; you’re copying it somewhere else with its copy constructor or assignment operator (C++ Cookbook, Stephens et. al.)*. The same applies to retrieving a value from a vector: __you are copying what is in the vector at that location to your
local variable__. So, if you have a large object, copying it can be expensive.  By using pointers, you can avoid this overhead.

This is because storing pointers require less CPU cycles than storing objects. When you store a pointer in a vector, only the address of the object is stored. This is much faster than copying the object. Also, when you retrieve an object from a vector of pointers, you are just copying the address of the object, not the object itself. This is much faster than copying the object.


> __If you are using older versions of C++__, just remember that if you add pointers to a standard library container, the container doesn’t delete them when it’s destroyed. Containers destroy only the objects they contain, i.e., the variable holding the addresses of the objects pointed to, but a container doesn’t know that what it’s storing is a pointer or an object, all it knows is that it’s some object of type `T` (C++ Cookbook, Stephens et. al.).

### Use `std::list` instead of `std::vector` when you need to insert elements arbitrarily.

```cpp
// ... other includes
#include <iterator>

std::list<int> l = {1, 2, 3, 4, 5};

// Say we want to insert 10 between 2 and 3.
auto it = std::next(l.begin(), 2); // it points to l[2].
l.insert(it, 10); // l = {1, 2, 10, 3, 4, 5}
```

This is because inserting an element in the middle of a vector is expensive. When you insert an element in the middle of a vector, all the elements after the insertion point have to be moved to make space for the new element. This is due to the nature of `std::vector`: it stores item in a contiguous memory space. This is not the case with `std::list`. In a list, each element is stored in a separate node, and each node has a pointer to the next node. So, inserting an element in the middle of a list is just a matter of changing the pointers of the nodes.

### Copying a subset of elements in an `std::vector`

```cpp
// ... other includes
#include <algorithm>

std::vector<int> v = {1, 2, 3, 4, 5};
std::vector<int> v2;

// assign(first, last) copies elements pointed to by first up
// to but not including last, i.e.: [first, last).
it = std::find(v.begin(), v.end(), 4);
v2.assign(v.begin(), it) // v2 = {1, 2, 3}
```

You can also use a copy constructor but this way is more common.

## TLDR: Functor
A functor, a.k.a. a function object, is a class that defines/overrides the `operator()` method. This allows you to create objects that "look like" functions. Functors are useful when you want to pass a function to another function, or when you want to store a function in a variable.

Conceptually, it is similar to a Python class with the `__call__` method defined. Both allow objects to be used as if they were functions.

I include a minimum-working-example in C++ and Python below.
```cpp
#include <iostream>

class CallCounter {
public:
    CallCounter() : count(0) {}
    void operator()() {
        count++;
        std::cout << "Called " << count << " times" << std::endl;
    }
private:
    int count;
};

int main() {
    CallCounter counter;
    counter();
    counter();
    counter();
    return 0;
}
```

```python
class CallCounter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        print(f"Called {self.count} times")

counter = CallCounter()
counter()
counter()
counter()
```


## TLDR: Predicate
It's just a functor that returns a bool. The name *"predicate"* is derived from the fact that it does not maintain a state and only returns a boolean value, i.e.: it is *pure* in some sense (*pure* ➡ *predicate*). It is used to test a condition.

Below are different ways to define a predicate in C++.

1. Function Pointer Predicate
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

bool is_even(int n) {
    return n % 2 == 0;
}

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6};
    auto it = std::find_if(numbers.begin(), numbers.end(), is_even);
    if (it != numbers.end()) {
        std::cout << "First even number: " << *it << std::endl;
    }
    return 0;
}
```
2. Functor Predicate
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class IsEven {
public:
    bool operator()(int n) const {
        return n % 2 == 0;
    }
};

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6};
    auto it = std::find_if(numbers.begin(), numbers.end(), IsEven());
    if (it != numbers.end()) {
        std::cout << "First even number: " << *it << std::endl;
    }
    return 0;
}
```
3. Lambda Predicate
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6};
    auto it = std::find_if(numbers.begin(), numbers.end(), [](int n) { return n % 2 == 0; });
    if (it != numbers.end()) {
        std::cout << "First even number: " << *it << std::endl;
    }
    return 0;
}
```

Some terminologies:
- Unary predicate: A predicate that takes one argument (and returns a bool).
- Binary predicate: A predicate that takes two arguments (and returns a bool).

## What's actually happening in `std::find_if`
Let's take look at the function pointer predicate example above. What's actually happening when you pass `is_even` to `std::find_if`? When you pass the predicate `is_even()` to `std::find_if`, you're actually passing the address of the function, which the algorithm can then call on elements of the container.

A function pointer is a just variable that stores the address of a function that can be called through it. This allows functions to be passed as arguments to other functions.

To declare a function pointer, for example, you can simply do the following:

```cpp
int foo(int a, int b) {
    return a + b;
}

int (*foo_ptr)(int, int) = foo;

// Now you can call foo through foo_ptr.
int result = foo_ptr(1, 2);
```

Now, let's take a look at what actually happens in `std::find_if`. Before that, let's take a look at the signature of `std::find_if`:
```cpp
template<class ExecutionPolicy, class ForwardIt, class UnaryPred>
ForwardIt find_if(ExecutionPolicy&& policy, ForwardIt first, ForwardIt last, UnaryPred p);
```

For now, don't worry about the `ExecutionPolicy` parameter. The important parameters are `ForwardIt first`, `ForwardIt last`, and `UnaryPred p`. `ForwardIt` is a type that satisfies the requirements of a forward iterator. `UnaryPred` is a type that satisfies the requirements of a unary predicate.

When you pass `is_even` to `std::find_if`, you're actually passing the address of the function `is_even`. The algorithm then calls `is_even` on each element of the container. Let's take a look at what's happening:

```cpp
for ( ; first != last; ++first) {
    if (p(*first)) {
        return first;
    }
}
return last;
```

Here `p` is called wth `*first` as argument. In our case, `p` is a function pointer to `is_even`, so `UnaryPred` is `bool(*)(int)`. So, this translates to:

```cpp
// ...
if (is_even(*first)) {
    return first;
}
// ...
```

## Should I preincrement (`++it`) or postincrement (`it++`) iterators?

Preincrement doesn’t create a temporary value to return each time, so it’s more efficient and is the preferred approach. Postincrement (`it++`) has to create a temporary variable because it returns the value of `it` before the increment. However, it can’t increment the value after it has returned, so it has to make a copy of the current value, increment the current value, then return the temporary value. Creating these temporary variables adds up after a while, __so if you don’t require postincrement behavior, use preincrement__ (C++ Cookbook, Stephens et. al.).

<!-- DRAFT: -->
<!-- ## `std::bind`? What's that? -->
<!-- Read the last prompt and the corresponding response, it's the best and most concise explanation of it: https://chatgpt.com/share/db8c2130-b978-4836-a7d8-d600bb9855af -->
