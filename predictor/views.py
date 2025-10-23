import os
import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render

# ============================
# 📂 Cargar modelo y codificadores
# ============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
label_sex = joblib.load(os.path.join(BASE_DIR, 'label_sex.pkl'))
label_embarked = joblib.load(os.path.join(BASE_DIR, 'label_embarked.pkl'))

# ============================
# 🌐 Vista principal
# ============================
def index(request):
    context = {}

    if request.method == 'POST':
        try:
            # Obtener valores del formulario
            pclass = request.POST.get('pclass')
            sex = request.POST.get('sex')
            age_str = request.POST.get('age')
            embarked = request.POST.get('embarked')

            # Validar que la edad sea numérica
            try:
                age = float(age_str)
            except ValueError:
                context['error'] = "⚠️ La edad debe ser un número válido."
                return render(request, 'index.html', context)

            # ✅ Validar rango de edad (solo entre 1 y 99)
            if age < 1 or age > 99:
                context['error'] = "⚠️ La edad debe estar entre 1 y 99 años."
                return render(request, 'index.html', context)

            # Asignar clase y tarifa
            if pclass == 'Primera clase':
                pclass_num, fare = 1, 80
            elif pclass == 'Segunda clase':
                pclass_num, fare = 2, 20
            else:
                pclass_num, fare = 3, 10

            # Codificar variables categóricas
            sex_encoded = label_sex.transform([sex])[0]
            embarked_encoded = label_embarked.transform([embarked])[0]

            # Crear DataFrame con columnas esperadas
            input_data = pd.DataFrame([{
                'Pclass': pclass_num,
                'Sex': sex_encoded,
                'Age': age,
                'Fare': fare,
                'Embarked': embarked_encoded
            }])

            # Calcular probabilidad
            probability = model.predict_proba(input_data)[0][1] * 100

            # ✅ Determinar resultado según la probabilidad
            if probability >= 50:
                result = f"La persona probablemente sobrevivirá ({probability:.1f}% de probabilidad)."
            else:
                result = f"La persona probablemente no sobrevivirá ({probability:.1f}% de probabilidad)."

            context['result'] = result
            context['probability'] = f"{probability:.1f}"

        except Exception as e:
            context['error'] = f"Ocurrió un error: {str(e)}"

    return render(request, 'index.html', context)
