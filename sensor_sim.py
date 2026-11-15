import random

def simulate_trip_summary(style):
    # يولّد ملخص قيادة محاكى: [avg_speed, max_speed, hard_brakes, sharp_turns]
    if style == 'reckless':
        avg_speed = random.randint(80, 130)
        max_speed = avg_speed + random.randint(10, 30)
        hard_brakes = random.randint(1, 6)
        sharp_turns = random.randint(1, 5)
    else:
        avg_speed = random.randint(50, 95)
        max_speed = avg_speed + random.randint(5, 20)
        hard_brakes = random.randint(0, 2)
        sharp_turns = random.randint(0, 2)
    return [avg_speed, max_speed, hard_brakes, sharp_turns]