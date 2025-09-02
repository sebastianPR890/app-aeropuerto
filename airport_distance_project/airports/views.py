from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.

def airport_distance_view(request):
    return render(request, 'airport_distance.html')

@csrf_exempt

def calculate_distance(request):
    if request.method == 'POST':
        try:
            aeropuerto_origen = request.POST.get('aeropuerto_origen','').strip().upper()
            aeropuerto_destino = request.POST.get('aeropuerto_destino','').strip().upper()
            if not aeropuerto_origen or not aeropuerto_destino:
                return JsonResponse({'error': 'Ambos Campos deben ser rellenados.'})
            
            if len(aeropuerto_origen) != 3 or len(aeropuerto_destino) != 3:
                return JsonResponse({'error': 'Los códigos de aeropuerto deben tener 3 caracteres.'})
            
            if aeropuerto_destino == aeropuerto_origen:
                return JsonResponse({'error': 'Los códigos de aeropuerto no pueden ser iguales.'})
            
            url = "https://airportgap.com/api/airports/distance"
            
            airports_data = {
                'from': aeropuerto_origen,
                'to': aeropuerto_destino
            }
            
            response_post = requests.post(url, json=airports_data)
            
            if response_post.status_code == 200:
                datos = response_post.json()
                
                result_data = {
                    'success': True,
                    'codigo': datos['data']['id'],
                    'aeropuerto_origen': {
                        'nombre': datos['data']['attributes']['from_airport']['name'],
                        'ciudad': datos['data']['attributes']['from_airport']['city'],
                        'codigo': aeropuerto_origen
                    },
                    'aeropuerto_destino': {
                        'nombre': datos['data']['attributes']['to_airport']['name'],
                        'ciudad': datos['data']['attributes']['to_airport']['city'],
                        'codigo': aeropuerto_destino
                    },
                    'distancia_km': datos['data']['attributes']['kilometers'],
                    'distancia_millas': datos['data']['attributes']['miles'],
                    'distancia_millas_nauticas': datos['data']['attributes']['nautical_miles']
                }

                return JsonResponse(result_data)
            
            elif response_post.status_code == 422:
                return JsonResponse({
                    'success': False,
                    'error': 'Los códigos de aeropuerto no son válidos.'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error en la API error: {response_post.status_code}.'
                    })
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'La solicitud ha tardado demasiado tiempo en responder.'
            })
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'success': False,
                'error': 'Error de conexión. Por favor, verifica tu conexión a Internet.'
            })
        except requests.exceptions as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la solicitud: {str(e)}'
            })
    return JsonResponse({
        'success': False,
        'error': 'Metodo no permitido.'
    })