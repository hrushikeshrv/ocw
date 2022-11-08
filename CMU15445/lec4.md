# Database Storage 2

## Data Representation
This section describes how the DBMS stores the values inside the tuples in memory.
Tuples’ data is essentially just byte arrays. It is up to the DBMS to know how to interpret those bytes to
derive the values for attributes. A data representation scheme is how a DBMS stores the bytes for a value.
There are four main types that can be stored in tuples: integers, variable precision numbers, fixed point
precision numbers, variable length values, and dates/times.

### Integers, Floats, Reals
These are usually just stored in the same way C/C++ store them, as specified by the IEEE-754
standard.

### Fixed Point Precision Numbers
The DBMS defines how it will handle fixed point precision numbers, and implements an API to 
access them itself. It does not rely on CPU instructions, since they have rounding errors.
Instead, the entire precision of the number is stored in the representation, along with
additional metadata telling the DBMS how to interpret the value.

These types are used when rounding errors are unacceptable, for example in scientific or financial 
applications. However, handling these types is much slower than floating point numbers.

## Variable Length Data
These are data types that consist of a varying amount of data that needs to be stored. For example,
`TEXT`, `VARCHAR`, `BLOB`, `VARBINARY`. Has a header that keeps track of the length of the string to make it easy to jump to the next value.
Most DBMSs do not allow a tuple to exceed the size of a single page, so they solve this issue by
writing the value on an overflow page and have the tuple contain a reference to that page.

Some systems will let you store these large values in an external file, and then the tuple will contain
a pointer to that file. For example, if our database is storing photo information, we can store the
photos in the external files rather than having them take up large amounts of space in the DBMS. One
downside of this is that the DBMS cannot manipulate the contents of this file.

### Datetime Data
These are usually just represented as an integer equal to the number of milli or micro seconds passed
since the UNIX epoch.