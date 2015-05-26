from django import forms
from codemirror2.widgets import CodeMirrorEditor

DEFAULT_ALGO = '''algorithme fonction add : entier
  parametres locaux
    entier a, b
debut
  retourne a + b
fin algorithme fonction add

variables
  booleen variable_globale
debut
  ecrire(add(5, 5))
fin
'''

class ConvertForm(forms.Form):
    algo_code = forms.CharField(widget=CodeMirrorEditor(),
                                initial=DEFAULT_ALGO)
    c_code = forms.CharField(widget=CodeMirrorEditor(), required=False)
