import pygetwindow as gw
import time as t

def main():
    try: 
        # Keep recording title and time until tracker stopped
        while True:
            # Getting all windows that are currently running
            all_windows = gw.getAllWindows()
            
            # Getting the time of capture
            current_time = t.ctime()
            
            # Iterate over every window
            for window in all_windows:
                # Get the title for each window
                title_window = window.title
                # If the title exists it is printed
                if title_window.strip():
                    print(f"Found window: {window.title}, at time: {current_time}")
            # Pause for 5 seconds
            t.sleep(5)
    except KeyboardInterrupt:
        print("Tracker Stopped.")


if __name__ == "__main__":
    main()