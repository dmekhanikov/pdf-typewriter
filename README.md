# PDF Typewriter

This script simplifies the routine of recurrent PDF forms filling.

It can work in two modes:
1. Writing monospace text into a PDF file.
2. Writing over existing PDF files.

## Usage

To make the script generate some text, you need to compose a YAML file specifying page properties, font and the text
itself. See examples for more information about the configuration file format.

You can run the script by executing the following command:

``` bash
$ python3 typewriter.py <text-config.yml> <pdf-file.pdf>
```

A `pdf` directory will be created with two files in it: 
1. `text.pdf` – generated text. 
2. `output.pdf` – text merged with the input PDF.

If the second argument is not specified, then a PDF file with text will be generated, but it won't be merged with any
existing file, so only `out/text.pdf` will be created.
