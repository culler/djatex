from . import LaTeXFile
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

def render_latex(request, filename, template_name,
                 error_template_name=None, bib_template_name=None,
                 context=None):
    template = get_template(template_name)
    source = template.render(context).encode('utf8')
    if bib_template_name:
        bib_template = get_template(bib_template_name)
        bib_source = bib_template.render(context).encode('utf8')
    else:
        bib_source = None
    file = LaTeXFile(source, bibtex_source=bib_source)
    file.compile()
    error_context = file.errors()
    if error_context:
        print(error_context)
        if error_template_name:
            return render(request, error_template_name, context=error_context)
        else:
            return HttpResponseServerError()
    else:
        response = HttpResponse(file.pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response
