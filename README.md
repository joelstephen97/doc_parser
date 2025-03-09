# Document Parser

A powerful document parser package for parsing resumes and general documents.
I noticed there isn't much open source packages to do document parsing and CV parsing in general,
This lead me to create this as I needed it for a project to parse CV data.
The package provides features for cleaning text, splitting text into sections (with support for custom sections), 
keyword searching, and resume-specific extraction functions (emails, phone numbers, names, skills).

## Installation

You can install the package locally by running:

``` pip install . ```

## Unit Tests 

You can run tests like this

``` python -m unittest discover -s tests ```