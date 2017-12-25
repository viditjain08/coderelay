from django import forms
import re
from djangocodemirror.fields import CodeMirrorField

class codeform(forms.Form):
    code = CodeMirrorField(label="Code", required=True,config_name="restructuredtext")
    lang = forms.IntegerField()
    #testcases = forms.CharField(widget=CodeMirrorEditor(options={'mode': 'python'}))


