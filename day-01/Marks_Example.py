marks = []
text = input("Enter a mark (0-100) or x to finish: ")
while text != "x":
    text = input("Enter a mark (0-100) or x to finish: ")
    if text.isdigit() and int(text) <= 100:
        marks.append(int(text))
    else:
        print("Invalid mark ignored.")
    text = input("Enter a mark (0-100) or x to finish: ")

if len(marks) == 0:
    print("No marks captured.")
else:
    # Step 3: total and average
    total = 0
    for m in marks:
        total = total + m
    average = total / len(marks)
    
# Step 4: highest and lowest
highest = marks[0]
lowest = marks[0]
for m in marks:
    if m > highest:
        highest = m
    if m < lowest:
        lowest = m