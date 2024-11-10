import requests

def get_distances_and_times(origin, destinations, api_key, sorted_data_dictionary, batch_size=25):
    errors = []
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    num_destinations = len(destinations)

    # Split destinations into batches of 'batch_size' (maximum allowed is 25 per request)
    for batch_start in range(0, num_destinations, batch_size):
        batch_destinations = destinations[batch_start:batch_start + batch_size]
        
        params = {
            'origins': origin,
            'destinations': '|'.join(batch_destinations),  # Join destinations with '|'
            'mode': 'driving',
            'key': api_key
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for i, element in enumerate(data['rows'][0]['elements']):
                if element['status'] == 'OK':
                    distance = element['distance']['text']
                    duration = element['duration']['text']
                    sorted_data_dictionary[batch_start + i]['distance'] = float(distance.replace('km', ''))
                    sorted_data_dictionary[batch_start + i]['duration'] = get_total_minutes_from_string(duration)
                else:
                    errors.append({
                        'address': sorted_data_dictionary[batch_start + i]['address'],
                        'name': sorted_data_dictionary[batch_start + i]['name'],
                        'price': sorted_data_dictionary[batch_start + i]['price'],
                        'error': element['status']
                    })
        else:
            for i in range(len(batch_destinations)):
                errors.append({
                    'address': sorted_data_dictionary[batch_start + i]['address'],
                    'name': sorted_data_dictionary[batch_start + i]['name'],
                    'price': sorted_data_dictionary[batch_start + i]['price'],
                    'error': 'Request failed'
                })

    return sorted_data_dictionary, errors


def get_total_minutes_from_string(duration_string):
    duration_list = duration_string.split()
    try:
        minutes = int(duration_list[duration_list.index('mins')-1])
        hours = int(duration_list[duration_list.index('hours')-1])
    except:
        hours = 0
    
    total_minutes = (hours * 60) + minutes
    return total_minutes