# DBMSs
A database is an organized collection of related data that models some aspect
of the real world (e.g., modeling the students in a class, or a digital music store).
A DBMS is a software that allows applications to store and analyze the information
in a database. It allows the definition, creation, querying, updating, and 
administration of databases.

DBMSs have 2 layers - the logical layer and the physical layer. The logical layer
defines which entities and attributes the data stored in the database will have, 
and the physical layer is how those entities are actually stored (like the 
particular data structure used to store the data).

Before relational databases, the physical layer was defined in the application code
itself, which made the database much harder to manage. If the structure of the data
or the requirements of the application changed, the whole physical layer needed
to be rewritten.

# Relational Model
Ted Codd proposed the relational model in 1970. The relational model has 3 key 
points -

1. Store database in simple data structures.
2. Access data through a high-level query language.
3. The physical storage of data is left up to the implementation.

The relational model is an example of a _data model_. A data model is a collection
of concepts for describing the data stored in a database. A _schema_ is a description
of a particular collection of data using a particular data model.

The relational model defines three concepts -
1. Structure - Data is distributed into tables and tables can be related 
   to each other. The structure also describes what kind or type of data each table
   can hold.
2. Integrity - The database's contents always satisfy some constraints, which 
   can either be defined by the designer or the database itself.
3. Manipulation - Describes how the contents of the database can be modified.

