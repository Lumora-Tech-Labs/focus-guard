import csv
from pathlib import Path

def main(day_number):
    input_path = Path(f"./data/raw/data_day{day_number + 1}.csv")
    output_path = Path(f"./data/processed/cleaned_day{day_number + 1}.csv")
    
    # 1. FIX: Overwrite the file on start so we don't duplicate data
    if output_path.exists():
        output_path.unlink() 

    try:
        with open(input_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Process row-by-row directly (Efficient)
            for row in reader:
                # 2. FIX: Convert duration to float immediately
                try:
                    duration_val = float(row["Duration"])
                except ValueError:
                    duration_val = 0.0
                
                # Extract hour
                hour_val = int(row["Start time"][11:13])
                
                process_and_save(output_path, row["Window"], duration_val, hour_val)
                
        print(f"✅ Processed Day {day_number + 1} into {output_path}")
            
    except FileNotFoundError:
        print(f"❌ Input file {input_path} not found.")

def classify_activity(title):
    title = title.lower()
    
    # Priority Keywords
    study = ["caie", "past papers", "papacambridge", ".pdf"]
    coding = ["visual studio code", ".py", "github"]
    social = ["instagram", "discord", "whatsapp"]
    ai = ["google gemini", "chatgpt", "claude"]
    
    # 3. FIX: Refined Media Logic (The Dash Bug)
    # Only flag as media if it HAS a dash but NOT VS Code or Chrome system tabs
    is_media_candidate = " - " in title
    is_work_app = "visual studio code" in title or "google chrome" in title
    
    # Waterfall Classification
    if any(w in title for w in study): return 1, 0, 0, 0, 0
    if any(w in title for w in coding): return 0, 1, 0, 0, 0
    if any(w in title for w in social): return 0, 0, 1, 0, 0
    if any(w in title for w in ai):     return 0, 0, 0, 1, 0
    if is_media_candidate and not is_work_app: return 0, 0, 0, 0, 1
    
    return 0, 0, 0, 0, 0 # Default (Browsing/System)

def process_and_save(output_path, window, duration, hour):
    field_names = ["is_study", "is_coding", "is_social", "is_ai", "is_media", "duration", "hour", "label"]
    
    # Get features
    res = classify_activity(window)
    is_study, is_coding, is_social, is_ai, is_media = res
    
    # 4. FIX: Smarter Labeling
    # We only label as 'Focused' if it's study/coding/ai AND duration isn't tiny
    is_productive_type = (is_study or is_coding or is_ai)
    is_long_enough = duration > 10.0 # Ignore micro-switches
    label = 1 if (is_productive_type and is_long_enough) else 0

    # Save logic
    file_exists = output_path.exists()
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "is_study": is_study,
            "is_coding": is_coding,
            "is_social": is_social,
            "is_ai": is_ai,
            "is_media": is_media,
            "duration": duration, 
            "hour": hour, "label": label
        })

if __name__ == "__main__":
    main(day_number=0)