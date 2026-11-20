import random

def generate_minutes():
    return random.randint(30, 180)

def calc_amount(machine_type, minutes):
    hours = minutes / 60
    machine_type = machine_type.upper().strip()
    if machine_type == "A":
        initial = 50.00
        hourly = 30.00
    elif machine_type == "B":
        initial = 62.50
        hourly = 36.25
    else: # C
        initial = 74.87
        hourly = 40.50
    amount = initial + (hourly * hours)
    return amount

def calc_total_amount(amount):
    vat = amount * 0.14
    total = amount + vat
    return vat, total

def display_summary(payments):
    count = len(payments)
    if count == 0:
        print("\nNo customers processed.")
        return

    combined = 0
    highest = payments[0]
    lowest = payments[0]

    for p in payments:
        combined += p
        if p > highest:
            highest = p
        if p < lowest:
            lowest = p

    average = combined / count

    print("\n--- DAILY SUMMARY ---")
    print(f"Number of customers processed: {count}")
    print(f"Combined amount payable: R{combined:.2f}")
    print(f"Average payment per customer: R{average:.2f}")
    print(f"Highest payment: R{highest:.2f}")
    print(f"Lowest payment: R{lowest:.2f}")

def process_payments():
    num = int(input("Enter number of customers to process: "))
    payments = []

    for i in range(num):
        print(f"\nCustomer {i+1}")
        name = input("Enter customer name: ")
        machine_type = input("Enter machine type (A / B / C): ")

        minutes = generate_minutes()
        amount_before_vat = calc_amount(machine_type, minutes)
        vat, total_payable = calc_total_amount(amount_before_vat)

        payments.append(total_payable)

        print("\n--- INVOICE ---")
        print(f"Customer: {name}")
        print(f"Machine type: {machine_type.upper()}")
        print(f"Minutes used: {minutes}")
        print(f"Amount before VAT: R{amount_before_vat:.2f}")
        print(f"VAT (14%): R{vat:.2f}")
        print(f"Total payable: R{total_payable:.2f}")

    display_summary(payments)

process_payments()