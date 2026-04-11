import pygetwindow as gw

def main():
    # Getting all windows that are currently running
    all_windows = gw.getAllWindows()
    
    # Iterate over every window
    for window in all_windows:
        # Get the title for each window
        title_window = window.title
        # If the title exists it is printed
        if title_window.strip():
            print(f"Found window: {window.title}")


if __name__ == "__main__":
    main()