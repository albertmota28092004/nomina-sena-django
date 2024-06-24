from weasyprint import HTML

html_string = """
<html>
    <head>
        <title>Test PDF</title>
    </head>
    <body>
        <h1>Hello, world!</h1>
    </body>
</html>
"""

html = HTML(string=html_string)
html.write_pdf('test.pdf')
