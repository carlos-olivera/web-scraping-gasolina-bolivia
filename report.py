
import pymongo
from pymongo import MongoClient
import pandas as pd
import json
from datetime import datetime

# Conectar a la base de datos de MongoDB
client = MongoClient('mongodb://admin:Gasolina_defau1_@192.168.50.139:27017')
db = client['gasolina']

# Obtener la colección
surtidores_collection = db['surtidores']

# Cargar los datos en un DataFrame de pandas
data = list(surtidores_collection.find())
df = pd.DataFrame(data)

# Convertir las fechas a formato datetime
df['readdatetime'] = pd.to_datetime(df['readdatetime'])

# Ordenar por 'description' y 'readdatetime'
df = df.sort_values(by=['description', 'readdatetime'])

# Agrupar por 'description'
grouped = df.groupby('description')

results = []

for name, group in grouped:
    group = group.sort_values(by='readdatetime')
    periods = []
    period_start = group.iloc[0]
    current_period = {
        'start_time': period_start['readdatetime'],
        'start_value': period_start['value'],
        'end_time': period_start['readdatetime'],
        'end_value': period_start['value']
    }
    
    for i in range(1, len(group)):
        current_record = group.iloc[i]
        previous_record = group.iloc[i - 1]
        
        if current_record['value'] < previous_record['value']:
            # El combustible se está agotando
            current_period['end_time'] = current_record['readdatetime']
            current_period['end_value'] = current_record['value']
        elif current_record['value'] > previous_record['value']:
            # El combustible se ha recargado
            periods.append(current_period)
            current_period = {
                'start_time': current_record['readdatetime'],
                'start_value': current_record['value'],
                'end_time': current_record['readdatetime'],
                'end_value': current_record['value']
            }
    
    periods.append(current_period)
    
    for period in periods:
        start_time = period['start_time']
        end_time = period['end_time']
        start_value = period['start_value']
        end_value = period['end_value']
        total_liters_sold = start_value - end_value
        time_elapsed_hours = (end_time - start_time).total_seconds() / 3600
        avg_sale_per_hour = total_liters_sold / time_elapsed_hours if time_elapsed_hours > 0 else 0
        
        results.append({
            'name': name,
            'first_time': start_time,
            'last_time': end_time,
            'avg_sale_per_hour': avg_sale_per_hour,
            'time_elapsed_hours': time_elapsed_hours,
            'total_liters_sold': total_liters_sold
        })

# Ordenar de mayor a menor los proveedores que más vendieron combustible
results = sorted(results, key=lambda x: x['total_liters_sold'], reverse=True)

# Imprimir los resultados en formato JSON
print(json.dumps(results, default=str, indent=4))

client.close()
