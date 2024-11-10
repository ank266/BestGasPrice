def rough_estimate_of_trip_fuel_cost(distance, duration, price):
    speed = distance / (duration / 60)
    gasUsed = -0.0954 * speed + 10.6732
    x = (gasUsed * distance)/ 100
    cost_of_gas_trip = x * price
    return cost_of_gas_trip