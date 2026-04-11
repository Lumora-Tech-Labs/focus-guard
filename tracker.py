import pygetwindow as gw
import time as t
import csv

def main():
    # Field names for csv file
    field_names = ["Window", "Time"] 
    # File path
    file_path = "./data/raw/data_day1.csv"

    # Open file to append
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
    
    try: 
        print("Tracker started... logging data to data.csv")
        # Keep recording title and time until tracker stopped
        while True:
            # Getting all windows that are currently running
            active_window = gw.getActiveWindow()
            # Getting the time of capture
            current_time = t.ctime()
            # Get the title for each window
            title_window = active_window.title
            # If the title exists it is printed
            if title_window.strip():
                print(f"Active window: {title_window}, at time: {current_time}")
                # Log to file
                writer.writerow({"Window" : title_window, "Time" : current_time})
            # Pause for 5 seconds
            t.sleep(5)
    except KeyboardInterrupt:
        print("Tracker Stopped.")


if __name__ == "__main__":
    main()