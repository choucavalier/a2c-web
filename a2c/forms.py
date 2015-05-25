from django import forms
from codemirror2.widgets import CodeMirrorEditor

class ConvertForm(forms.Form):
    code = forms.Charfield(widget=CodeMirrorEditor(options={'mode': 'algo'}))
