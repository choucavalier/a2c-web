from django import forms
from codemirror2.widgets import CodeMirrorEditor

class ConvertForm(forms.Form):
    code = forms.CharField(widget=CodeMirrorEditor())
