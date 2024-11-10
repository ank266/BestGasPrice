def apply_pc_optimum_rewards(price):
    base_pts = price - 0.035
    more_pts = price * 10
    more_pts = more_pts / 1000
    total_points = base_pts - more_pts
    adjusted_price = total_points - 0.035
    return round(adjusted_price, 2)

def apply_points(locations_dictionary):
    for loc in locations_dictionary:
        if loc['name'] == 'Mobil' or loc['name'] == 'Esso':
            loc['price'] = apply_pc_optimum_rewards(loc['price'])

    return locations_dictionary
