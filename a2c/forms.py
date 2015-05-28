from django import forms
from codemirror2.widgets import CodeMirrorEditor

#DEFAULT_ALGO = '''algorithme fonction add : entier
  #parametres locaux
    #entier a, b
#debut
  #retourne a + b
#fin algorithme fonction add

#variables
  #booleen variable_globale
#debut
  #ecrire(add(5, 5))
#fin
#'''

DEFAULT_ALGO = '''algorithme procedure foo
variables
  t_pile p
debut
  p <- pile_vide()
  empiler(p, 1)
  empiler(p, 2)
  empiler(p, 3)
  ecrire(p^.sommet)
  ecrire(depiler(p))
  empiler(p, 4)
  ecrire(depiler(p))
  ecrire(depiler(p))
  ecrire(depiler(p))

  empiler(p, 1)
  vide_pile(p)
  ecrire(est_vide(p))
fin algorithme procedure foo

debut
  foo()
fin
'''

class ConvertForm(forms.Form):
    algo_code = forms.CharField(widget=CodeMirrorEditor(),
                                initial=DEFAULT_ALGO)
    c_code = forms.CharField(widget=CodeMirrorEditor(), required=False)
