#   This file is part of the program djaTeX.
#
#   Copyright (C) 2017 by Marc Culler and others. 
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Project homepage: https://bitbucket.org/marc_culler/djatex
#   Author homepage: https://marc-culler.info

import os, tempfile
from subprocess import run, PIPE

class LaTeXFile:
    """
    An object which holds LaTeX and, optionally, BibTeX source strings.  Its
    compile method creates a byte sequence containing a pdf rendering of the
    LaTeX source, as well as strings containing the pdflatex and bibtex logs.
    These are generated by running pdflatex and bibtex in a temporary directory
    which is removed once the results are copied into the LaTeXFile object.  If
    the home_dir argument is not None it should be an absolute path to a
    directory containing auxiliary files needed for compilation, such as inputs,
    images or font .fd files.  These will be symlinked into the temporary
    directory before LaTeX is run.
    """
    rerun = b'Rerun to get cross-references right.'
    latex_args = ['pdflatex', '-file-line-error', '-halt-on-error', 'source']
    
    def __init__(self, latex_source, bibtex_source=None, home_dir=None):
        self.latex_result = self.bib_result = None
        self.latex_source = latex_source
        self.home_dir=home_dir
        if isinstance(latex_source, str):
            self.latex_source = self.latex_source.encode('utf8')
        elif not isinstance(latex_source, bytes):
            raise ValueError('the LaTeX source must be of type str or bytes.')
        self.bibtex_source = bibtex_source
        if bibtex_source is None:
            return
        elif isinstance(bibtex_source, str):
            self.bibtex_source = bibtex_source.encode('utf8')
        elif not isinstance(bibtex_source, bytes):
            raise ValueError('The bibtex source must be of type str or bytes.')
        
    def compile(self):
        with tempfile.TemporaryDirectory(prefix='renderLaTeX') as tempdir:
            tex_path = os.path.join(tempdir, 'source.tex')
            bibtex_path = os.path.join(tempdir, 'source.bib')
            log_path = os.path.join(tempdir, 'source.log')
            pdf_path = os.path.join(tempdir, 'source.pdf')
            if self.home_dir:
                for extra_file in os.listdir(self.home_dir):
                    os.symlink(os.path.join(self.home_dir, extra_file),
                               os.path.join(tempdir, extra_file))
            with open(tex_path, 'wb') as output:
                output.write(self.latex_source)
            latex_result = run(self.latex_args, cwd=tempdir, timeout=30,
                         stdout=PIPE, stderr=PIPE)
            if latex_result.returncode == 0 and self.bibtex_source:
                with open(bibtex_path, 'wb') as output:
                    output.write(self.bibtex_source)
                self.bib_result = run(['bibtex', 'source'], cwd=tempdir, timeout=30,
                                      stdout=PIPE, stderr=PIPE)
                latex_result = run(self.latex_args, cwd=tempdir, timeout=30,
                             stdout=PIPE, stderr=PIPE)
            if latex_result.returncode == 0 and latex_result.stdout.find(self.rerun) >= 0:
                latex_result = run(self.latex_args, cwd=tempdir, timeout=30,
                             stdout=PIPE, stderr=PIPE)
            self.latex_result = latex_result
            with open(log_path, 'r') as log:
                self.log = log.read()
            if latex_result.returncode == 0:
                with open(pdf_path, 'rb') as pdf:
                    self.pdf = pdf.read()
            else:
                self.pdf = None

    def errors(self):
        if self.latex_result.returncode:
            error_dict = {
                'stage': 'latex',
                'source': [line for line in self.latex_source.split(b'\n')],
                'output': [line for line in self.latex_result.stdout.split(b'\n')]
            }
        elif self.bib_result and self.bib_result.returncode:
            error_dict = {
                'stage': 'bibtex',
                'source': [line for line in self.bibtex_source.split(b'\n')],
                'output': [line for line in self.bib_result.stdout.split(b'\n')]
            }
        else:
            error_dict = None
        return error_dict

test_latex = r"""
\documentclass[11pt]{article}
\usepackage{cite}

\begin{document}

\title{My Article}
\author{Nobody Jr.}
\date{Today}
\maketitle

Blablabla said Nobody ~\cite{Nobody06}.

$$X = X$$

\bibliography{source}{}
\bibliographystyle{plain}
\end{document}
"""
test_bibtex = r"""
@misc{ Nobody06,
       author = "Nobody Jr",
       title = "My Article",
       year = "2006" }
"""
