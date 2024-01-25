import json
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def calculate_da(request):
    if request.method == 'POST':
        data = request.POST
        data = json.loads(request.body.decode('utf-8'))
        print('data:',data)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        pay_grade = data.get('pay_grade')

        print("ssSSSssssssss", start_date,end_date,pay_grade)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT public.get_da_rate_by_grade(%s, %s, %s) as da_amount",
                [start_date, end_date, pay_grade]
            )
            result = cursor.fetchone()
        print("result", result)
        da_amount = result[0] if result else 0

        return JsonResponse({'da_amount': da_amount})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def calculate_ta_da(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print('data:', data)
            
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            v_start_location_id = data.get('v_start_location_id')
            v_end_location_id = data.get('v_end_location_id')
            pay_grade = data.get('pay_grade')
            transport_type = data.get('transport_type')

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT public.calculate_ta_da(%s, %s, %s, %s, %s, %s) as result",
                    [start_date, end_date, v_start_location_id, v_end_location_id, pay_grade, transport_type]
                )
                result = cursor.fetchone()

            return JsonResponse({'result': result[0] if result else ''})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def calculate_ta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print('data:', data)
            
            v_start_location_id = data.get('v_start_location_id')
            v_end_location_id = data.get('v_end_location_id')
            pay_grade = data.get('pay_grade')
            transport_type = data.get('transport_type')

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT public.get_ta_rate_by_grade_distance(%s, %s, %s, %s) as ta_amount",
                    [v_start_location_id, v_end_location_id, pay_grade, transport_type]
                )
                result = cursor.fetchone()

            return JsonResponse({'ta_amount': result[0] if result else ''})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        return JsonResponse({'error': 'Invalid request method'})
