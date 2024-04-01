from django import forms
from .models import Teams, Calendar

class FilterForm(forms.Form):
    equipos = Teams.objects.all()
    equipo = forms.ModelChoiceField(queryset=equipos, empty_label="Todos los equipos", required=False, label="Equipo", widget=forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm'}))

    jornada = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm'}))

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        jornada_choices = Calendar.objects.values_list('num_jornada', flat=True).distinct().order_by('num_jornada')
        self.fields['jornada'].choices = [('', 'Todas las jornadas')] + [(j, j) for j in jornada_choices]