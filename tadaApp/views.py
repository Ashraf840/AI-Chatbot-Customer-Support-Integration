import json
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

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
            print('sth')
            with connection.cursor() as cursor:
                print('sth2')
                cursor.execute(
                    "SELECT public.get_ta_da(%s, %s, %s, %s, %s, %s) as result",
                    [start_date, end_date, v_start_location_id, v_end_location_id, pay_grade, transport_type]
                )
                result = cursor.fetchone()
                print("result:",result)

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

@csrf_exempt
@api_view(['GET', 'POST'])
def get_location_list(request):
    if request.method == "GET":
        try:
            location_state = request.query_params.get('location_state', '')
            language = request.query_params.get('language', '')
            print('location state:', location_state, language)
            if location_state == 'start_location' or location_state == 'end_location':
                if language == 'en' or language == 'bn':
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT DISTINCT {location_state}_id, {location_state}_name_{language} FROM distance_matrix")
                        rows = cursor.fetchall()
                        print("rows:", rows)
                        location_list = [{f'{location_state}_id': row[0], f'{location_state}_name_{language}': row[1]} for row in rows]

                    return JsonResponse({f'{location_state}s': location_list})

        except Exception as e:
            return JsonResponse({'error': str(e)})
# from django.http import JsonResponse
# from django.db import connection

# def get_start_locations(request):
#     try:
#         # Execute raw SQL query to retrieve distinct start locations
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT DISTINCT start_location_id, start_location_name_en FROM distance_matrix")

#             # Fetch all rows from the cursor
#             rows = cursor.fetchall()

#         # Format the rows into a list of dictionaries
#         start_location_list = [{'start_location_id': row[0], 'start_location_name_en': row[1]} for row in rows]

#         return JsonResponse({'start_locations': start_location_list})

#     except Exception as e:
#         return JsonResponse({'error': str(e)})
