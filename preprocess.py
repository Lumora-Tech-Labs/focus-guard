import csv
from pathlib import Path
from datetime import datetime

def main(day_number):
    input_path = Path(f"./data/raw/data_day{day_number + 1}.csv")
    output_path = Path(f"./data/processed/cleaned_day{day_number + 1.1}.csv")

    # Clear old file
    if output_path.exists():
        output_path.unlink()

    try:
        with open(input_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                window = row.get("Window", "").strip()

                # --- duration fix ---
                try:
                    duration = float(row.get("Duration", 0))
                except ValueError:
                    duration = 0.0

                # --- hour fix (safe parsing) ---
                try:
                    hour = datetime.strptime(
                        row.get("Start time", ""),
                        "%Y-%m-%d %H:%M:%S"
                    ).hour
                except Exception:
                    hour = 0

                # DEBUG (uncomment if needed)
                # print(window, duration, hour)

                process_and_save(output_path, window, duration, hour)

        print(f"✅ Processed Day {day_number + 1} → {output_path}")

    except FileNotFoundError:
        print(f"❌ Input file not found: {input_path}")

def classify_activity(title):
    title = title.lower()

    study_keywords = [
        "physics", "mathematics", "math", "caie", "9702",
        "past paper", "pdf", "syllabus", "economics",
        "further maths", "mechanics"
    ]

    coding_keywords = [
        "visual studio code", "vscode", ".py", "github",
        "code", "tracker", "focus-guard"
    ]

    social_keywords = [
        "instagram", "discord", "whatsapp", "reddit",
        "facebook", "twitter"
    ]

    ai_keywords = [
        "chatgpt", "gemini", "claude"
    ]

    media_keywords = [
        "youtube", "spotify", "netflix", "music"
    ]

    if any(k in title for k in study_keywords):
        return 1, 0, 0, 0, 0

    if any(k in title for k in coding_keywords):
        return 0, 1, 0, 0, 0

    if any(k in title for k in social_keywords):
        return 0, 0, 1, 0, 0

    if any(k in title for k in ai_keywords):
        return 0, 0, 0, 1, 0

    if any(k in title for k in media_keywords):
        return 0, 0, 0, 0, 1

    return 0, 0, 0, 0, 0

def process_and_save(output_path, window, duration, hour):
    field_names = [
        "is_study", "is_coding", "is_social",
        "is_ai", "is_media",
        "duration_bucket", "hour_sin", "hour_cos",
        "label"
    ]

    is_study, is_coding, is_social, is_ai, is_media = classify_activity(window)
    
    if duration < 1:
        duration_bucket = 0
    elif duration < 5:
        duration_bucket = 1
    elif duration < 15:
        duration_bucket = 2
    else:
        duration_bucket = 3

    is_productive = (is_study or is_coding or is_ai)

    # lowered threshold (was 10.0 → too strict)
    is_long_enough = duration >= 2.0

    label = 1 if (is_productive and is_long_enough) else 0

    import math

    hour_rad = (hour / 24) * 2 * math.pi
    hour_sin = math.sin(hour_rad)
    hour_cos = math.cos(hour_rad)

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
            "duration_bucket": duration_bucket,
            "hour_sin": hour_sin,
            "hour_cos": hour_cos,
            "label": label
        })

if __name__ == "__main__":
    main(day_number=1)