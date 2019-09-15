#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from sys import argv
import os
import yaml

out_dir = 'pdf'

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


if __name__ == "__main__":
    text_yml_file = argv[1]

    with open(text_yml_file, 'r') as stream:
        text_desc = yaml.safe_load(stream)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    text_pdf_file = out_dir + '/text.pdf'

    font_conf = text_desc['font']
    
    if font_conf['file']:
        register_font(font_conf['name'], font_conf['file'])
        
    c = make_canvas(text_pdf_file, font_conf)
    spacing = font_conf['spacing']

    for snippet in text_desc['snippets']:
        x = snippet['x']
        y = snippet['y']
        text = snippet['text']
        write_string(c, x, y, text, font_conf['spacing'])

    c.save()
