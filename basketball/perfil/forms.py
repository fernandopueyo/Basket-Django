from django import forms
from .models import Players
from calendar_basket.models import Teams

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['first_name', 'last_name', 'id_team', 'dorsal']

    first_name = forms.CharField(label='Nombre', max_length=20, initial='')
    last_name = forms.CharField(label='Apellidos', max_length=20, required=False, initial='') 
    id_team = forms.ModelChoiceField(queryset=Teams.objects.all(), label='Equipo', to_field_name='id_team')
    dorsal = forms.IntegerField(label='Dorsal', required=False, initial='')

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm'