# water_billing.py
# PROJECT 2 | COMMUNITY WATER CONSUMPTION AND BILLING MANAGEMENT SYSTEM
# Input: water_readings.txt | Format: MeterNumber,HouseholdName,PreviousReading,CurrentReading,Area
# Example: M001,Lerato Molefe,3173,3178,Soshanguve
# Consumption = CurrentReading - PreviousReading (in kL)

# ============================================================
# SECTION 1: VALIDATION FUNCTIONS
# ============================================================

def is_valid_meter(meter_no):
    # Must be M + 3 digits, e.g. M001, M044
    if len(meter_no) != 4:
        return False
    if meter_no[0] != "M":
        return False
    index = 1
    while index < len(meter_no):
        if not meter_no[index].isdigit():
            return False
        index += 1
    return True

def is_valid_reading(reading_str):
    # Must be a number and not negative
    try:
        reading = float(reading_str)
    except ValueError:
        return False
    if reading < 0:
        return False
    return True

# ============================================================
# SECTION 2: CALCULATION FUNCTIONS
# ============================================================

def calculate_consumption(previous, current):
    # Monthly consumption in kL
    return current - previous

def calculate_bill(consumption):
    # Progressive tariff - NOT flat rate
    # First 6 kL = Free
    # Next 14 kL (6 to 20) = R8.50 per kL
    # Above 20 kL = R12.00 per additional kL
    # Example: 25 kL = (14 x 8.50) + (5 x 12.00) = R179.00
    bill = 0.0
    if consumption <= 6:
        bill = 0.0
    elif consumption <= 20:
        bill = (consumption - 6) * 8.50
    else:
        bill = (14 * 8.50) + (consumption - 20) * 12.00
    return bill

def classify_consumption(consumption):
    # LOW = 0-20 kL, MODERATE = >20 to 50 kL, HIGH = >50 kL
    if consumption <= 20:
        return "LOW"
    elif consumption <= 50:
        return "MODERATE"
    else:
        return "HIGH"

# ============================================================
# SECTION 3: MANUAL RANKING - TOP 5 HIGHEST CONSUMERS
# ============================================================
# Do NOT use sorted(), max() or min() - manual Selection Sort
# We sort by consumption, highest to lowest

def get_top_five(records):
    # Make a copy so we don't destroy the original list
    temp = []
    i = 0
    while i < len(records):
        temp.append(records[i])
        i += 1

    # Selection Sort - full sort, then take first 5
    index = 0
    while index < len(temp):
        best = index
        other = index + 1
        while other < len(temp):
            if temp[other]["consumption"] > temp[best]["consumption"]:
                best = other
            other += 1
        temp[index], temp[best] = temp[best], temp[index]
        index += 1

    # Take top 5 using a loop
    top_five = []
    i = 0
    while i < len(temp) and i < 5:
        top_five.append(temp[i])
        i += 1
    return top_five

# ============================================================
# SECTION 4: READ INPUT, CHECK RECORDS AND BUILD THE REGISTER
# ============================================================

def main():
    households = {}  # Dictionary: MeterNumber -> record
    errors = []      # List of rejected lines and reasons
    line_count = 0

    # Q1: Read all lines, handle missing file
    try:
        with open("water_readings.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("water_readings.txt not found!")
        return

    # Q2 + Q3: Loop, split, clean, validate
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        line_count += 1

        if line == "":
            continue

        # Split and clean fields
        parts = line.split(",")

        # Q3a: Reject missing fields - must be exactly 5 fields
        if len(parts) != 5:
            errors.append(f"INVALID FORMAT: {line} -> Expected 5 fields, got {len(parts)}")
            continue

        meter_no = parts[0].strip()
        name = parts[1].strip()
        prev_str = parts[2].strip()
        curr_str = parts[3].strip()
        area = parts[4].strip()

        # Q3b: Reject missing name / area
        if name == "":
            errors.append(f"INVALID NAME: {line} -> Household name is empty")
            continue

        if area == "":
            errors.append(f"INVALID AREA: {line} -> Area is empty")
            continue

        # Q3c: Reject invalid meter number
        if not is_valid_meter(meter_no):
            errors.append(f"INVALID METER: {line} -> Meter must be M + 3 digits, e.g. M001")
            continue

        # Q3d: Reject duplicate meter numbers
        if meter_no in households:
            errors.append(f"DUPLICATE METER: {line} -> Meter {meter_no} already exists")
            continue

        # Q3e: Reject non-numeric / negative readings
        if not is_valid_reading(prev_str):
            errors.append(f"INVALID READING: {line} -> Previous reading '{prev_str}' must be a number >= 0")
            continue

        if not is_valid_reading(curr_str):
            errors.append(f"INVALID READING: {line} -> Current reading '{curr_str}' must be a number >= 0")
            continue

        previous = float(prev_str)
        current = float(curr_str)

        # Q3f: Reject current below previous - reversed readings
        if current < previous:
            errors.append(f"REVERSED READING: {line} -> Current {curr_str} is below Previous {prev_str}")
            continue

        # Q4: Calculate consumption
        consumption = calculate_consumption(previous, current)

        # Q5: Calculate bill using progressive tariff
        bill = calculate_bill(consumption)

        # Q6: Classify
        category = classify_consumption(consumption)

        # Q2: Store valid record in dictionary
        households[meter_no] = {
            "meter": meter_no,
            "name": name,
            "previous": previous,
            "current": current,
            "area": area,
            "consumption": consumption,
            "bill": bill,
            "category": category
        }

    # ============================================================
    # SECTION 5: CALCULATE SUMMARY TOTALS USING LOOPS
    # ============================================================
    records = list(households.values())

    total_consumption = 0.0
    total_billed = 0.0
    low_count = 0
    moderate_count = 0
    high_count = 0

    i = 0
    while i < len(records):
        total_consumption = total_consumption + records[i]["consumption"]
        total_billed = total_billed + records[i]["bill"]
        if records[i]["category"] == "LOW":
            low_count += 1
        elif records[i]["category"] == "MODERATE":
            moderate_count += 1
        else:
            high_count += 1
        i += 1

    # Q7: Get Top 5 manually
    top_five = get_top_five(records)

    # ============================================================
    # SECTION 6: WRITE OUTPUT FILES
    # ============================================================

    # Q8a: Write billing_report.txt
    with open("billing_report.txt", "w") as f:
        f.write("COMMUNITY WATER CONSUMPTION AND BILLING REPORT\n")
        f.write("==============================================\n")
        f.write(f"Total records: {line_count}\n")
        f.write(f"Accepted: {len(records)}\n")
        f.write(f"Rejected: {len(errors)}\n\n")

        f.write("HOUSEHOLD BILLING DETAILS\n")
        f.write("-------------------------\n")
        f.write("METER | NAME | AREA | PREV | CURR | CONSUMPTION (kL) | CATEGORY | BILL (R)\n")
        f.write("--------------------------------------------------------------------------------\n")
        i = 0
        while i < len(records):
            r = records[i]
            f.write(f"{r['meter']} | {r['name']} | {r['area']} | {r['previous']:.0f} | {r['current']:.0f} | {r['consumption']:.0f} | {r['category']} | R{r['bill']:.2f}\n")
            i += 1

        f.write("\nTOP 5 HIGHEST CONSUMING HOUSEHOLDS\n")
        f.write("------------------------------------\n")
        rank = 1
        i = 0
        while i < len(top_five):
            r = top_five[i]
            f.write(f"{rank}. {r['meter']} | {r['name']} | {r['area']} | {r['consumption']:.0f} kL | {r['category']} | R{r['bill']:.2f}\n")
            rank += 1
            i += 1

        f.write("\nSUMMARY\n")
        f.write("-------\n")
        f.write(f"Total consumption: {total_consumption:.0f} kL\n")
        f.write(f"Total amount billed: R{total_billed:.2f}\n")
        f.write(f"LOW (0-20 kL): {low_count}\n")
        f.write(f"MODERATE (21-50 kL): {moderate_count}\n")
        f.write(f"HIGH (above 50 kL): {high_count}\n")

    # Q8b: Write errors.log
    with open("errors.log", "w") as f:
        i = 0
        while i < len(errors):
            f.write(errors[i] + "\n")
            i += 1

    # Q8c: Display totals
    print("WATER BILLING PROCESSOR")
    print(f"Accepted: {len(records)} Rejected: {len(errors)}")
    print(f"Total consumption: {total_consumption:.0f} kL")
    print(f"Total billed: R{total_billed:.2f}")
    print("Files created: billing_report.txt, errors.log")

if __name__ == "__main__":
    main()