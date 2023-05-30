from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

def check_weather_conditions():
    owm = OWM('f4e14cce42f4c85c35947174bb078afd')
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place('Riga,LV')
    w = observation.weather

    wind = w.wind()['speed']
    rain = w.rain

    if wind < 5 and not rain:
        return True
    else:
        return False