from django import forms
from .models import Statistics, ShotStatistics

class StatisticsForm(forms.ModelForm):
    class Meta:
        model = Statistics
        exclude = ['id_team', 'id_player', 'id_game', 'id', 'fgm', 'fga', 'fgperc', 'threepm', 'threepa', 'threepperc', 'ftperc', 'pts', 'win']

    mins = forms.IntegerField(label='Minutos', required=False, initial=0)
    ftm = forms.IntegerField(label='Tiros libres anotados', required=False, initial=0)
    fta = forms.IntegerField(label='Tiros libres intenados', required=False, initial=0)
    reb = forms.IntegerField(label='Rebotes', required=False, initial=0)
    ast = forms.IntegerField(label='Asistencias', required=False, initial=0)
    stl = forms.IntegerField(label='Robos', required=False, initial=0)
    blk = forms.IntegerField(label='Tapones', required=False, initial=0)
    turnover = forms.IntegerField(label='Pérdidas', required=False, initial=0)
    pf = forms.IntegerField(label='Faltas personales', required=False, initial=0)
    

class ShotForm(forms.Form):
    WIN_CHOICES = [
        ('', 'Todos'),
        (True, 'Win'),
        (False, 'Lose'),
    ]

    MADE_CHOICES = [
        ('', 'Todos'),
        (True, 'Anotado'),
        (False, 'Fallado'),
    ]

    win = forms.ChoiceField(choices=WIN_CHOICES, required=False, label='Win/Lose', widget=forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm'}))
    made = forms.ChoiceField(choices=MADE_CHOICES, required=False, label='Anotado/Fallado', widget=forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm'}))
