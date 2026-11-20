# Maxwell Fitness Centre - PoE Activity 6 (with match)

def amount_due(facility_code, hours):
    match facility_code:
        case "squa":
            rate = 13.00
        case "swim":
            rate = 12.00
        case "gym":
            rate = 11.00
        case "wei":
            rate = 8.00
        case _:
            rate = 0
    return rate * hours

def final_amount_due(amount):
    return amount * 1.14

def display(name, final_amount):
    print(f"\n{name}, your final amount payable is R{final_amount:.2f}")

def process_payment():
    name = input("Enter customer name: ")
    facility_code = input("Enter facility code (squa / swim / gym / wei): ")
    hours = float(input("Enter number of hours: "))

    due = amount_due(facility_code, hours)
    final = final_amount_due(due)
    display(name, final)

process_payment()