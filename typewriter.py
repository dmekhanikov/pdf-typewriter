#!/usr/bin/env python

from reportlab.pdfgen import canvas

import os

out_dir = 'pdf'

point = 1
inch = 72


def make_canvas(output_filename):
    c = canvas.Canvas(output_filename, pagesize=(8.5 * inch, 11 * inch))
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Oblique", 12 * point)
    return c


if __name__ == "__main__":
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    text_file = out_dir + '/text.pdf'
    c = make_canvas(text_file)
    c.drawString(1 * inch, 10 * inch, 'Hello, World!')
    c.save()
