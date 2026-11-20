# race_qualifiers.py

total = 0
qualified = 0
winner_name = ""
winner_time_str = ""
winner_seconds = 0

while True:
    name = input("Enter athlete name (x to end): ")
    if name.lower() == "x":
        break

    time_str = input("Enter time (mm:ss): ")

    # Validate: must contain :, both parts digits, seconds 0-59
    if ":" not in time_str:
        print("Invalid time, ignored.")
        continue

    parts = time_str.split(":")
    if len(parts) != 2:
        print("Invalid time, ignored.")
        continue

    if not parts[0].isdigit() or not parts[1].isdigit():
        print("Invalid time, ignored.")
        continue

    minutes = int(parts[0])
    seconds = int(parts[1])

    if seconds < 0 or seconds > 59:
        print("Invalid time, ignored.")
        continue

    # Valid entry
    total_seconds = minutes * 60 + seconds
    total += 1

    if total_seconds <= 25 * 60:
        qualified += 1

    # Find winner (lowest time, keep first on tie)
    if winner_name == "" or total_seconds < winner_seconds:
        winner_name = name
        winner_time_str = time_str
        winner_seconds = total_seconds

# Output
if total == 0:
    print("No valid entries.")
else:
    print(f"\nWinner: {winner_name} ({winner_time_str})")
    print(f"Qualified: {qualified} of {total}")