from django import forms

class PassengerForm(forms.Form):
    pclass = forms.ChoiceField(choices=[(1, 'Primera'), (2, 'Segunda'), (3, 'Tercera')])
    sex = forms.ChoiceField(choices=[('male', 'Hombre'), ('female', 'Mujer')])
    age = forms.FloatField(label='Edad')
    sibsp = forms.IntegerField(label='Hermanos / Cónyuge a bordo')
    parch = forms.IntegerField(label='Padres / Hijos a bordo')
    fare = forms.FloatField(label='Tarifa')
    embarked = forms.ChoiceField(choices=[('C', 'Cherbourg'), ('Q', 'Queenstown'), ('S', 'Southampton')])