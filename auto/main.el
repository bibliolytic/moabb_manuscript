(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("IEEEtran" "journal")))
   (TeX-run-style-hooks
    "latex2e"
    "abstract"
    "introduction"
    "methods"
    "results"
    "discussion"
    "IEEEtran"
    "IEEEtran10"
    "amsmath"
    "graphicx"
    "tikz"
    "color"
    "cite"
    "subcaption")
   (TeX-add-symbols
    '("vj" 1)
    '("ab" 1)
    '("blfootnote" 1))
   (LaTeX-add-bibliographies
    "library.bib"))
 :latex)

