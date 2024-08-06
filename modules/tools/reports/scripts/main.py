import os
from fpdf import FPDF, Template

class PDF(FPDF):
    figure_number = 0

    def variables(self):
        self.figure_number = 0
        self.table_number = 0

    def header(self):
        # Logo
        # self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 0, 'PDF TITLE', 0, 0, 'C')
        # Line break
        self.ln(2)

    # Page footer
    def footer(self):
        # Position at 2 cm from bottom
        self.set_y(-2)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    
    def section(self, text: str):
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 0, text)
        pdf.ln(1)
    
    def block(self, text: str):
        pdf.set_font('Times', '', 12)
        pdf.cell(
            w=0,
            h=0,
            txt=text
        )
        pdf.ln(1)

    def figure(self, path, caption, ref):
        self.figure_number += self.figure_number 

        pdf.set_font('Times', 'B', 12)

        pdf.cell(0, 0, f'Figure {self.figure_number}: {caption}', 0, 0, 'C')
        pdf.ln(0.1)

        weight = 16
        x = (21 - weight)/2

        pdf.image(path, x=x, w=weight, h=9)

        pdf.cell(0, 0, 'Fonte: '+ref)

        pdf.ln(1)

dirname = os.path.dirname(__file__)

# Instantiation of inherited class
pdf = PDF('P', 'cm', 'A4')

pdf.set_margins(left=3, top=3, right=2)
pdf.alias_nb_pages()

pdf.add_page()

pdf.section('Introdução')
pdf.block('Put some text here')

img = os.path.join(dirname, '../img', 'figure_one.png')
pdf.figure(img, 'Equação linear', 'Autoria própria')

pdf.section('Envios de SMS em janeiro de 2021')
pdf.block('Put another text here')

# output PDF document
docs = os.path.join(dirname, '../docs', 'main.pdf')
pdf.output(docs, 'F')