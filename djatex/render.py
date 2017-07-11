from . import LaTeXFile
from django.http import HttpResponse
from django.template.loader import get_template

def render_latex(filename, template_name, bib_template_name=None, context=None):
    template = get_template(template_name)
    source = template.render(context).encode('utf8')
    if bib_template_name:
        bib_template = get_template(bib_template_name)
        bib_source = bib_template.render(context).encode('utf8')
    else:
        bib_source = None
    file = LaTeXFile(source, bibtex_source=bib_source)
    file.compile()
    if not file.errors():
        response = HttpResponse(file.pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response
    else:
        raise RuntimeError
