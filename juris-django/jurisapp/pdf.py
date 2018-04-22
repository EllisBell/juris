from weasyprint import HTML, CSS
from django.template.loader import render_to_string


def get_acordao_pdf(ac, absolute_uri):
    html_template = render_to_string('jurisapp/acordao_pdf.html', {'acordao': ac})
    html = HTML(string=html_template, base_url=absolute_uri)
    pdf = html.write_pdf(stylesheets=[CSS("static\jurisapp\css\pdf_style.css")])
    return pdf
