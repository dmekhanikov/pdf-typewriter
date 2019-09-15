#!/usr/bin/env python

from reportlab.pdfgen import canvas
import os
import yaml

out_dir = 'pdf'
text_yml_file = 'text.yml'

point = 1
inch = 72
char_size = 12 * point
spacing = 15 * point


def make_canvas(output_filename):
    c = canvas.Canvas(output_filename, pagesize=(8.5 * inch, 11 * inch))
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Oblique", char_size)
    return c


def write_string(c, x, y, string):
    for sym in string:
        c.drawString(x, y, sym)
        x += spacing


if __name__ == "__main__":
    with open(text_yml_file, 'r') as stream:
        text_desc = yaml.safe_load(stream)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    text_pdf_file = out_dir + '/text.pdf'
    c = make_canvas(text_pdf_file)

    for snippet in text_desc['snippets']:
        x = snippet['x']
        y = snippet['y']
        text = snippet['text']
        write_string(c, x, y, text)

    c.save()
