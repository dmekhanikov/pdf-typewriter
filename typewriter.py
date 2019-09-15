#!/usr/bin/env python

import os
from sys import argv

import yaml
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

out_dir = 'pdf'
text_pdf_file = out_dir + '/text.pdf'
out_pdf_file = out_dir + '/output.pdf'

inch = 72


def make_canvas(output_filename, font_conf):
    c = canvas.Canvas(output_filename, pagesize=(8.5 * inch, 11 * inch))
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont(font_conf['name'], font_conf['size'])
    return c


def write_string(c, x, y, string, spacing):
    for sym in string:
        c.drawString(x, y, sym)
        x += spacing


def register_font(name, file):
    pdfmetrics.registerFont(TTFont(name, file))


def create_text_pdf(text_pdf_file, text_desc):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    font_conf = text_desc['font']

    if font_conf['file']:
        register_font(font_conf['name'], font_conf['file'])

    c = make_canvas(text_pdf_file, font_conf)
    spacing = font_conf['spacing']

    for snippet in text_desc['snippets']:
        x = snippet['x']
        y = snippet['y']
        text = snippet['text']
        write_string(c, x, y, text, spacing)

    c.save()


def merge_pdfs(file1, file2, out_file):
    input1 = PdfFileReader(file1)
    input2 = PdfFileReader(file2)
    output = PdfFileWriter()

    for i, page in enumerate(input1.pages):
        if i < input2.numPages:
            page.mergePage(input2.getPage(i))
        output.addPage(page)

    output_stream = open(out_file, "wb")
    output.write(output_stream)
    output_stream.close()


if __name__ == "__main__":
    text_yml_file = argv[1]
    input_pdf_file = argv[2] if len(argv) > 1 else None

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(text_yml_file, 'r') as stream:
        text_desc = yaml.safe_load(stream)

    create_text_pdf(text_pdf_file, text_desc)

    if input_pdf_file:
        merge_pdfs(input_pdf_file, text_pdf_file, out_pdf_file)
