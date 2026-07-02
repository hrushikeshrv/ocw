# ocw
My notes for all the online courses I have taken.  
CC BY-NC-SA 4.0 License, just like MIT OCW :)

Read the notes on [hrus.in/ocw/](https://hrushikeshrv.github.io/ocw/)

# Building PDFs
1. Clone the repository
2. Run `python build.py` from the project root to build PDF files from every markdown file in each subdirectory

# Testing PDF Generation
Run this command from the project root:

```bash
python build.py --test
```
This should generate corresponding PDF files in the `test/` directory with the expected contents.
