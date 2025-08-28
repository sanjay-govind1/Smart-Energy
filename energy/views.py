from django.shortcuts import render
from django.http import JsonResponse
from .models import EnergyReading
from energy.tapo_client.utils import collect_reading_sync 
from .ml_utils import predict_tomorrow_energy

def collect_data_view(request):
    try:
        reading = collect_reading()
        return JsonResponse({
            "device": reading.device_name,
            "power": reading.current_power,
            "today_energy": reading.today_energy,
            "month_energy": reading.month_energy,
            "runtime_minutes": reading.runtime_minutes,
            "timestamp": reading.timestamp,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def readings_list(request):
    readings = EnergyReading.objects.all().order_by("-timestamp")[:10]
    data = [
        {
            "device": r.device_name,
            "power": r.current_power,
            "today_energy": r.today_energy,
            "month_energy": r.month_energy,
            "runtime_minutes": r.runtime_minutes,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for r in readings
    ]
    return JsonResponse(data, safe=False)


def home_view(request):
    try:
        latest = collect_reading_sync()
    except Exception as e:
        print(f"Error fetching live reading: {e}")
        latest = EnergyReading.objects.first()

    # Default: no forecast
    forecast = None
    if latest:
        try:
            forecast = predict_tomorrow_energy(latest)
        except Exception as e:
            print(f"Prediction error: {e}")

    return render(request, "energy/home.html", {
        "latest": latest,
        "forecast": forecast
    })
