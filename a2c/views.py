from django.shortcuts import render
from a2c.forms import ConvertForm

def convert_code(code):
    pass

def convert(request):
    context = {}
    if request.method == 'POST':
        form = ConvertForm(request.POST)
        context['form'] = form

        if form.is_valid():
            code = form.cleaned_data['code']
            context['code'] = code
        return render(request, 'convert.html', context)
    context['form'] = ConvertForm()
    return render(request, 'convert.html', context)
