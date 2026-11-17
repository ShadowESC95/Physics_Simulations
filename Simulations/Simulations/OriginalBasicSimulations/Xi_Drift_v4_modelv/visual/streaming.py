# visual/streaming.py
from rx import Observable

Observable.interval(1000)  # 1Hz updates
  .map(fetch_live_data)
  .filter(validate_telemetry)
  .subscribe(update_displays)
