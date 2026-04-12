import csv
import datetime as dt
from pathlib import Path
import pygetwindow as gw
import time as t

def main(day_number):
    field_names = ["Window", "Start time", "Duration"] 
    file_path = Path(f"./data/raw/data_day{day_number + 1}.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Initialize state BEFORE the loop
    active_obj = gw.getActiveWindow()
    current_window = active_obj.title if active_obj else "Desktop/None"
    start_time_seconds = t.time() 

    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        if csvfile.tell() == 0:
            writer.writeheader()
    
        try: 
            print(f"Tracker started... logging to {file_path.name}")
            while True:
                t.sleep(1)
                
                check_obj = gw.getActiveWindow()
                new_window_title = check_obj.title if check_obj else "Desktop/None"

                # Detect Change
                if new_window_title != current_window:
                    end_time_seconds = t.time()
                    duration = round(end_time_seconds - start_time_seconds, 2)
                    
                    # Convert start_time_seconds to readable format for the CSV
                    readable_start = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(start_time_seconds))
                    
                    # Log the window we just FINISHED
                    writer.writerow({
                        "Window": current_window, 
                        "Start time": readable_start, 
                        "Duration": duration
                    })
                    csvfile.flush() # Force write to disk
                    
                    print(f"Switched from {current_window} to {new_window_title} (Stayed: {duration}s)")
                    
                    # Update state for the NEXT window
                    current_window = new_window_title
                    start_time_seconds = end_time_seconds
                
        except KeyboardInterrupt:
            # Final log for whatever window was open when you hit Ctrl+C
            duration = round(t.time() - start_time_seconds, 2)
            readable_start = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(start_time_seconds))
            writer.writerow({"Window": current_window, "Start time": readable_start, "Duration": duration})
            print("\nTracker Stopped.")

if __name__ == "__main__":
    main(day_number=1)