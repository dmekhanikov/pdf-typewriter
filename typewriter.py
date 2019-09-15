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


def make_canvas(output_filename, page_conf):
    width = page_conf['width']
    height = page_conf['height']
    c = canvas.Canvas(output_filename, pagesize=(width, height))
    return c


def write_string(c, x, y, string, spacing):
    for sym in str(string):
        c.drawString(x, y, sym)
        x += spacing


def register_font(name, file):
    pdfmetrics.registerFont(TTFont(name, file))


def create_text_pdf(text_pdf_file, text_desc):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    font_conf = text_desc['font']

    if 'file' in font_conf:
        register_font(font_conf['name'], font_conf['file'])

    page_conf = text_desc['page']

    c = make_canvas(text_pdf_file, page_conf)
    global_spacing = font_conf['spacing']

    for page_desc in text_desc['pages']:
        set_font(c, font_conf)
        for snippet in page_desc['snippets']:
            x = snippet['x']
            y = snippet['y']
            text = snippet['text']
            spacing = snippet['spacing'] \
                if 'spacing' in snippet \
                else global_spacing
            write_string(c, x, y, text, spacing)

        c.showPage()

    c.save()


def set_font(c, font_conf):
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont(font_conf['name'], font_conf['size'])


def merge_pdfs(file1, file2, out_file):
    input1 = PdfFileReader(file1)
    input2 = PdfFileReader(file2)
    output = PdfFileWriter()

    for i, page in enumerate(input1.pages):
        if i < input2.numPages:
            page.mergePage(input2.getPage(i))
        output.addPage(page)

    with open(out_file, "wb") as output_stream:
        output.write(output_stream)


if __name__ == "__main__":
    text_yml_file = argv[1]
    input_pdf_file = argv[2] if len(argv) > 2 else None

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(text_yml_file, 'r') as stream:
        text_desc = yaml.safe_load(stream)

    create_text_pdf(text_pdf_file, text_desc)

    if input_pdf_file:
        merge_pdfs(input_pdf_file, text_pdf_file, out_pdf_file)
