import csv

#1 Load initial student scores from CSV
def load_students():
    students = {}
    try:
        with open('students_score.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2 and row[1].isdigit():
                    students[row[0]] = int(row[1])

    except FileNotFoundError:
        # If file doesn't exist, create it with default data
        default_students = {
            "Soala_Amachree": 97, "Desmond_Ozondu": 91, "Obasi_Princewill": 99,
            "Joshua_Eze-ochia": 90, "Christopher_Egere": 65, "Amadi_Greatman": 65,
            "Havilah_Oghenejivwe": 85, "Grace_Chitchuga": 95, "Redeemer_Messiah": 46,
            "Nwandike_Darlington": 75, "Aguma_Michelle": 60, "Jensen_Ogu": 45,
            "Nora_Messiah": 38, "Sarima_Ozondu": 40, "Onyesiuwe_Ella": 43,
            "Flourish_Obasi": 78, "Ibeya_Tekena": 50, "Lilian_Messiah": 64,
            "Melvin_Nick": 20, "Delight_Justice": 0, "Morenike_Abioye": 0, "Prasie_Ogu": 62,
            "Olayinka_Oghenejivwe": 87, "Chatem_Julia": 80, "Sarah_Ozondu": 67,
            "Francis_John": 74, "David_Ernsest": 72
        }
        save_students(default_students)
        return default_students
    return students

def save_students(students):
    with open('students_score.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for name, score in students.items():
            writer.writerow([name, score])

students_score = load_students()

#2 Append a new student to the CSV
students_score["Chiamaka_Eze"] = 40
save_students(students_score)


#3 Function to rank students based on scores (highest first)
def rank_students(data):
    return sorted(data.items(), key=lambda x: x[1], reverse=True)

def show_histogram():
    scores = students_score.values()
    bins = {0:0, 50:0, 70:0, 90:0}  # Score ranges
    
    for score in scores:
        if score >= 90: bins[90] += 1
        elif score >= 70: bins[70] += 1
        elif score >= 50: bins[50] += 1
        else: bins[0] += 1
    
    print("\nScore Distribution:")
    for threshold, count in sorted(bins.items()):
        bar = "■" * count
        print(f"{threshold}+: {bar} ({count})")

#4 Function to display all student names alphabetically
def display_student_names():
    print("\nAll student names (sorted):")
    for name in sorted(students_score.keys()):
        print(name)

#5 Password for admin access
ADMIN_PASSWORD = "$0@/@.com#"
def is_admin():
    attempt = input("Enter admin password: ")
    return attempt == ADMIN_PASSWORD

#6 Function to calculate and print class statistics
def calculate_statistics():
    scores = students_score.values()
    max_score = max(scores)
    min_score = min(scores)
    average = sum(scores) / len(scores)
    print(f"\nClass Statistics:")
    print(f"Total students: {len(students_score)}")
    print(f"Highest score: {max_score}")
    print(f"Lowest score: {min_score}")
    print(f"Average score: {average:.2f}")

#7 Convert dictionary to a list of tuples (name, score)
students_list = list(students_score.items())

#8 Find the student with the highest score
top_student = max(students_list, key=lambda x: x[1])

#9 Print top student info
ranking = rank_students(students_score)
print(f"\nThe top student is {top_student[0]} with a grade of {top_student[1]}\n")

#10 Prompt user for student name to check score
print("Please enter the name of the student you want to check their score:")
first = input("First name: ").capitalize()
last = input("Last name: ").capitalize()
name = first + "_" + last
name2 = last + "_" + first

#11 Main program logic
def main():
    #12 If student name exists
    if name in students_score:
        score = students_score.get(name)
        print(f"{name}: {score}")
        print()

        #13 Get and print ranking of the student
        ranking = rank_students(students_score)
        for position, (student, _) in enumerate(ranking, start=1):
            if student == name:
                suffix = "th"
                if position == 1:
                    suffix = "st"
                elif position == 2:
                    suffix = "nd"
                elif position == 3:
                    suffix = "rd"
                print(f"{name} is in position {position}{suffix}")
                break

        #14 Ask if user wants to see all scores
        reply = input("Would you like to see the scores of the other students (yes/no): ").lower()
        if reply == "yes":
            print("Here are the scores of the other students:")
            for student, score in students_score.items():
                print(f"{student}: {score}")
        else:
            print("Okay")

        #15 Ask if user wants class statistics
        names = input("Would you like to see student average? (yes/no): ").lower()
        if names == "yes":
            calculate_statistics()
            show_histogram()
        elif names == "no":
            print("Okay")
        else:
            print("Invalid input")

        #16 Ask if user wants to see all student names
        reply5 = input("Would you like to see other students' names? (yes/no): ").lower()
        if reply5 == "yes":
            display_student_names()
        elif reply5 == "no":
            print("Okay")
        else:
            print("Invalid input")

    #17 If the reversed name exists
    elif name2 in students_score:
        print(f"Sorry, not found. Did you mean {last}_{first}?")
        return

    #18 If neither format is found
    else:
        reply6 = input("Sorry, not found. Would you like to add the student? (yes/no): ").lower()
        if reply6 == "no":
            print("Please try again with the correct name format.")
            return
        elif reply6 == "yes":
            pass
        else:
            print("Invalid input")

        if reply6 == "yes": 
            try:
                new_score = int(input(f"Enter score for {name}: "))
                students_score[name] = new_score
                save_students(students_score)  # Save to CSV
                ranking = rank_students(students_score)
                for position, (student, _) in enumerate(ranking, start=1):
                    if student == name:
                        suffix = "th"
                        if position == 1:
                            suffix = "st"
                        elif position == 2:
                            suffix = "nd"
                        elif position == 3:
                            suffix = "rd"
                        print(f"{name} has been added and is in position {position}{suffix}")
                        break
            except ValueError:
                print("Invalid score. Please enter a number.")

            #20 Ask if user wants to see all scores after adding
            reply3 = input("Would you like to see everyone's scores? (yes/no): ").lower()
            if reply3 == "yes":
                for student, score in students_score.items():
                    print(f"{student}: {score}")
            elif reply3 == "no":
                print("Okay")
            else:
                print("Invalid input")

        elif reply6 == "no":
            print("Okay")
        else:
            print("Invalid input")

        #21 Ask if user wants to view names or delete data
        reply5 = input("Would you like to see other students' names? (yes/no): ").lower()
        if reply5 == "yes":
            display_student_names()
        elif reply5 == "no":
            reply4 = input("Would you like to delete the data? (yes/no): ").lower()
            while len(reply4) > 2:
                if reply4 == "yes":
                    if is_admin():
                        students_score.clear()
                        save_students(students_score)  # Save empty dictionary to CSV
                        print("All student data has been deleted.")
                        break
                    else:
                        print("Access denied!")
                elif reply4 == "no":
                    print("Okay")
                    break
                else:
                    print("Invalid input")
        else:
            print("Invalid input")

# Run the main function with error handling
try:
    main()
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you entered the names correctly with capital letters at the beginning.")
    print("If you need help, please contact support.")