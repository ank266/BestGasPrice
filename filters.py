from collections import defaultdict
import numpy as np

def filter_get_best_locations_by_duration(locations):
    duration_groups = defaultdict(list)
    for loc in locations:
        duration_groups[loc['duration']].append(loc)

    best_locations = []
    for duration, group in duration_groups.items():
        best_location = min(group, key=lambda x: (x['price'], x['distance']))
        best_locations.append(best_location)

    return best_locations



def filter_eliminate_high_price_repeats_that_are_far_away(locations):
    filtered_locations = []
    max_price = 0
    duration = 0
    for loc in locations:
        if loc['price'] > max_price:
            max_price = loc['price']
            duration = loc['duration']
    
    found = 0
    for loc in locations:
        if loc['price'] == max_price:
            if found == 0:
                found = 1
                filtered_locations.append(loc)
            else:
                pass
        else:
            filtered_locations.append(loc)
            
    return filtered_locations



def filter_out_exceeding_distance():
    pass



def filter_out_exceeding_duration():
    pass


def sort_based_on_weights(weight_price, weight_distance, weight_time, locations):
    max_price = max(location['price'] for location in locations)
    min_price = min(location['price'] for location in locations)
    max_distance = max(location['distance'] for location in locations)
    min_distance = min(location['distance'] for location in locations)
    max_time = max(location['duration'] for location in locations)
    min_time = min(location['duration'] for location in locations)

    # Calculate score for each location
    for location in locations:
        # Normalize each factor (higher values are better after normalization)
        normalized_price = (max_price - location['price']) / (max_price - min_price)
        normalized_distance = (max_distance - location['distance']) / (max_distance - min_distance)
        normalized_time = (max_time - location['duration']) / (max_time - min_time)
        
        # Calculate weighted score
        score = (
            (normalized_price * weight_price) +
            (normalized_distance * weight_distance) +
            (normalized_time * weight_time)
        )
        
        # Add score to each location dictionary
        location['score'] = score

    # Sort locations by score (higher score is better)
    locations = sorted(locations, key=lambda x: x['score'], reverse=True)
    return locations


def filter_by_quartile_values(locations, percentile, title):
    filtered_locations = []

    prices = [location[title] for location in locations]
    percentile = np.percentile(prices, percentile)

    for loc in locations:
        if loc[title] <= percentile:
            filtered_locations.append(loc)

    return filtered_locations