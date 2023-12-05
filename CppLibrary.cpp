// C++ File Template

/*
Why would we do this?

1. Large, tested stable library written in c++
- Such as communication library or a library to talk to a specific piece of hardware

2. You want to speed up a particular section of your python code by converting it to C

3. Want to use Python Test tools to do large-scale testing of their testing of their systems.


Terms:
Marshalling:
- The process of transforming the memory representation of an object to a data format suitable for starge or transmission.

Types to convert:
- Integers: Python stores with arbitrary precision. C needs exact sizes, be careful when moving between languages so overflow in C doesn't occur

- Floating-point numbers: Python is more flexible, careful in C and C++ to stay in range

- Complex numbers: C has complex numbers, need a struct or class in the C code to manage them

- Strings: Tricky when creating Python bindings

- Boolean Variables: Supported in C, straight-forward


Mutable and Immutable Values:
- 

*/