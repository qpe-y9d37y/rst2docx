=====================
 PYTHON-DOCX_Edition
=====================
-------------------------
 Technical Documentation
-------------------------

Introduction
============

python-docx is a Python library for creating and updating Microsoft Word
(.docx) files.

Installation
============

To be able to use python-docx, you need to install the module. First,
update pip:

``pip install --upgrade pip setuptools``

If you're using a proxy, then add the option --proxy, for example:

``pip --proxy http://${PROXY_IP}:${PORT} install --upgrade pip``

Now you can install the module:

``pip install python-docx``

If you face an error like the one hereunder, make sure that you updated
the setuptools module.

``error: can't copy 'docx/templates/default-docx-template':
doesn't exist or not a regular file``

Word Style Template
===================

To create a template, open a new blank document in MS Word and in the
"Home" tab, under "Styles", select "Create a Style". The styles that you
will create are the ones that you will use when inserting text, in the
following example "Title".

>>> document.add_paragraph('The Lord of the Rings', 'Title')

You can also add pictures on your cover page.

Usage
=====

Document Creation
-----------------

To create a document, first import the python-docx module:

>>> from docx import Document

To open an existing presentation, do:

>>> document = Document(docx_template)

Or a new one:

>>> document = Document()

Text in a Document
------------------

To insert a text in a document, do:

>>>  document.add_paragraph('Hello World')

Styles and Layout
-----------------

To apply a specific style for a text, do:

>>> document.add_paragraph(text, style)

For example:

>>> document.add_paragraph('The Lord of the Rings', 'Title')
>>> document.add_paragraph('The Fellowship of the Ring', 'Subtitle')
>>> document.add_paragraph('Prologue', 'Heading 1')
>>> document.add_paragraph('Concerning Hobbits', 'Heading 2')
>>> content = """This book is largely concerned with Hobbits, and
... from its pages a reader may discover much of their character and
... a little of their history."""
>>> document.add_paragraph(content, 'Normal')

If you want to create a new style, first import the necessary libraries:

>>> from docx.shared import Pt, RGBColor
>>> from docx.enum.style import WD_STYLE_TYPE

Now you can create the new style, start by declaring it, giving it a
name:

>>> document.styles.add_style('Titulo', WD_STYLE_TYPE.PARAGRAPH)

Then set it the way you want:

>>> title_style = document.styles['Titulo']
>>> title_style.font.name = "Arial"
>>> title_style.font.size = Pt(28)
>>> title_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
>>> title_style.paragraph_format.space_after = Pt(28)

To add a page break, do:

>>> document.add_page_break()

Table in a Document
-------------------

To create a new table, do:

>>> table = document.add_table(r, c, s)

With:

* r the number of rows in the table

* c the number of columns in the table

* s the style of the table (optional)

To add content in a cell, do:

>>> table.cell(row_id, col_id).text = 'Firstname'

For example, if I wanted to create a table like the following one:

+-----------+----------+
| Firstname | Lastname |
+===========+==========+
| Bilbo     | Baggins  |
+-----------+----------+

I would do:

>>> table = document.add_table(2, 2, 'Table Grid')
>>> table.cell(0, 0).text = 'Firstname'
>>> table.cell(0, 1).text = 'Lastname'
>>> table.cell(1, 0).text = "Bilbo"
>>> table.cell(1, 1).text = "Baggins"

To set the background color to a specific cell, import the necessary
libraries:

>>> from docx.oxml.shared import OxmlElement, qn

Add the following function:

>>> def shade_cells(cell, shade):
...     tcPr = cell._tc.get_or_add_tcPr()
...     tcVAlign = OxmlElement("w:shd")
...     tcVAlign.set(qn("w:fill"), shade)
...     tcPr.append(tcVAlign)

Now, you can use the function like:

>>> shade_cells(table.cell(x, y), "FF6666")

Picture in a Document
---------------------

To add a picture in a document, do:

>>> document.add_picture(p, w)

With:

* p the picture file you want to insert

* o  w the width of the picture

You can also add the height of the picture, instead or in addition to
the width of the picture. However, if you add both the width and the
height, the proportions of the picture won't be kept.

If you want to use inches for the width or height of the picture, import
the library:

>>> from docx.shared import Inches

Then you can declare the width like:

>>> graph_width = Inches(6.0)

Save the Document
-----------------

To save the document, do:

>>> document.save(docx_output)

Sources
=======

.. [CAN19] Canny, S. (2019). python-docx. [online]
   Python-docx.readthedocs.io. Available at:
   https://python-docx.readthedocs.io/en/latest/ [Accessed 6 Feb. 2020].
