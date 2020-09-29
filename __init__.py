from flask import Flask, render_template, request
import xlwt


app = Flask(__name__)

#style pour excel
def get_style(color_back, color_font):
    style = xlwt.XFStyle()

    #font color
    font = xlwt.Font()
    font.colour_index = xlwt.Style.colour_map[color_font]
    style.font = font

    # Cell centering
    align = xlwt.Alignment()
    align.horz = xlwt.Alignment.HORZ_CENTER  # horizontal direction
    align.vert = xlwt.Alignment.VERT_CENTER  # Vertical direction
    style.alignment = align

    # Background color
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map[color_back]  # Set the cell background color to yellow
    style.pattern = pattern

    # Frame
    border = xlwt.Borders()  # Frame cells
    border.left = xlwt.Borders.THIN  # Left
    border.top = xlwt.Borders.THIN  # upper
    border.right = xlwt.Borders.THIN  # right
    border.bottom = xlwt.Borders.THIN  # lower
    border.left_colour = 0x40  # Border line color
    border.right_colour = 0x40
    border.top_colour = 0x40
    border.bottom_colour = 0x40
    style.borders = border

    return style

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('planning',cell_overwrite_ok=True)
sheet.write_merge(0, 1, 1, 1, 'lundi', get_style('gray80', 'white'))
sheet.write_merge(0, 1, 2, 2, 'mardi', get_style('gray80', 'white'))
sheet.write_merge(0, 1, 3, 3, 'mercredi', get_style('gray80', 'white'))
sheet.write_merge(0, 1, 4, 4, 'jeudi', get_style('gray80', 'white'))
sheet.write_merge(0, 1, 5, 5, 'vendredi', get_style('gray80', 'white'))
sheet.write_merge(0, 1, 6, 6, 'samedi', get_style('gray80', 'white'))
sheet.write_merge(0, 1, 7, 7, 'dimanche', get_style('gray80', 'white'))
sheet.write_merge(2, 3, 0, 0, '6h00')
sheet.write_merge(4, 5, 0, 0, '8h00')
sheet.write_merge(6, 7, 0, 0, '10h00')
sheet.write_merge(8, 9, 0, 0, '12h00')
sheet.write_merge(10, 11, 0, 0, '14h00')
sheet.write_merge(12, 13, 0, 0, '16h00')
sheet.write_merge(14, 15, 0, 0, '18h00')
sheet.write_merge(16, 17, 0, 0, '20h00')
sheet.write_merge(18, 19, 0, 0, '22h00')
sheet.write_merge(2, 3, 1, 7, 'machine occupée', get_style('red', 'white'))
sheet.write_merge(4, 15, 6, 7, 'machine occupée', get_style('red', 'white'))
sheet.write_merge(16, 19, 1, 7, 'machine occupée', get_style('red', 'white'))
sheet.write_merge(0, 1, 0, 0, style=get_style('gray80', 'white'))

workbook.save('/Users/louismorel/Documents/cours/chatbot/chatbot/static/planning.xls')

import chatbot.chat
