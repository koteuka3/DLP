import openai
import datetime
from .weather import check_weather_conditions
from .models import Work

def generate_event_list():
    openai.api_key = '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'
    prompt = """
     Izveidojiet misiju sarakstu, kas ietver šādu informāciju:
     1. Drone Fly
     2. Lidojuma laiks (minūtēs) katrai misijai.
     3. Uzlādes laiks (minūtēs) starp misijām.

     Piemērs:
     1. Drone Fly: lidojuma laiks - 30, uzlādes laiks - 60.
     2. Drone Fly: lidojuma laiks - 45, uzlādes laiks - 60.

     Izveidojiet sarakstu ar 5 misijām.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=14,
        stop=None,
        temperature=0.7,
        timeout=15,
    )

    event_list = []
    current_time = datetime.datetime.now()
    current_date = current_time.date()

    for choice in response.choices:
        mission = choice.text.strip()
        mission_parts = mission.split(":")
        title = mission_parts[0].strip()
        times = mission_parts[1].split(",")
        flight_time = int(times[0].strip().split("-")[1].strip().replace("minūtes", ""))
        charge_time = int(times[1].strip().split("-")[1].strip().split(".")[0].strip().replace("minūtes", ""))

        if check_weather_conditions():
            start_time = current_time + datetime.timedelta(minutes=charge_time)
            end_time = start_time + datetime.timedelta(minutes=flight_time)

            current_date += datetime.timedelta(days=1)
            current_time = datetime.datetime(current_date.year, current_date.month, current_date.day, start_time.hour,
                                             start_time.minute)
            current_time += datetime.timedelta(hours=2)

        event_data = {
            'title': 'Drona Lidojums',
            'start': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': end_time.strftime('%Y-%m-%dT%H:%M:%S')
        }
        event_list.append(event_data)

    return event_list












