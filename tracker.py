import pygetwindow as gw
import time as t
import csv

def main():
    # Field names for csv file
    field_names = ["Window", "Time"] 
    # File path
    file_path = "./data/raw/data.csv"
    
    try: 
        print("Tracker started... logging data to data.csv")
        # Keep recording title and time until tracker stopped
        while True:
            # Getting all windows that are currently running
            all_windows = gw.getAllWindows()
            # Getting the time of capture
            current_time = t.ctime()
            
            # Open file to append
            with open(file_path, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                # Iterate over every window
                for window in all_windows:
                    # Get the title for each window
                    title_window = window.title
                    # If the title exists it is printed
                    if title_window.strip():
                        print(f"Found window: {window.title}, at time: {current_time}")
                        # Log to file
                        writer.writerow({"Window" : title_window, "Time" : current_time})
            # Pause for 5 seconds
            t.sleep(5)
    except KeyboardInterrupt:
        print("Tracker Stopped.")


if __name__ == "__main__":
    main()