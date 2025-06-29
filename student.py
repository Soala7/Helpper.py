import csv

# Load student scores from CSV
def load_students():
    students = {}
    try:
        with open('students_score.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2 and row[1].isdigit():
                    students[row[0]] = int(row[1])
    except FileNotFoundError:
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

def rank_students(data):
    return sorted(data.items(), key=lambda x: x[1], reverse=True)

def show_histogram(students_score):
    scores = students_score.values()
    bins = {0:0, 50:0, 70:0, 90:0}
    for score in scores:
        if score >= 90: bins[90] += 1
        elif score >= 70: bins[70] += 1
        elif score >= 50: bins[50] += 1
        else: bins[0] += 1
    print("\nScore Distribution:")
    for threshold, count in sorted(bins.items()):
        bar = "■" * count
        print(f"{threshold}+: {bar} ({count})")

def display_student_names(students_score):
    print("\nAll student names (sorted):")
    for name in sorted(students_score.keys()):
        print(name)

def calculate_statistics(students_score):
    scores = students_score.values()
    max_score = max(scores)
    min_score = min(scores)
    average = sum(scores) / len(scores)
    print(f"\nClass Statistics:")
    print(f"Total students: {len(students_score)}")
    print(f"Highest score: {max_score}")
    print(f"Lowest score: {min_score}")
    print(f"Average score: {average:.2f}")

def main():
    students_score = load_students()
    print("Please enter the name of the student you want to check their score:")
    first = input("First name: ").capitalize()
    last = input("Last name: ").capitalize()
    name = first + "_" + last
    name2 = last + "_" + first

    if name in students_score:
        score = students_score[name]
        print(f"{name}: {score}\n")
        ranking = rank_students(students_score)
        for pos, (student, _) in enumerate(ranking, start=1):
            if student == name:
                suffix = "th"
                if pos == 1: suffix = "st"
                elif pos == 2: suffix = "nd"
                elif pos == 3: suffix = "rd"
                print(f"{name} is in position {pos}{suffix}")
                break

        if input("See all scores? (yes/no): ").lower() == "yes":
            for student, score in students_score.items():
                print(f"{student}: {score}")

        if input("See student average? (yes/no): ").lower() == "yes":
            calculate_statistics(students_score)
            show_histogram(students_score)

        if input("See student names? (yes/no): ").lower() == "yes":
            display_student_names(students_score)

    elif name2 in students_score:
        print(f"Did you mean {last}_{first}?")

    else:
        if input("Student not found. Add student? (yes/no): ").lower() == "yes":
            try:
                new_score = int(input(f"Enter score for {name}: "))
                students_score[name] = new_score
                save_students(students_score)
                ranking = rank_students(students_score)
                for pos, (student, _) in enumerate(ranking, start=1):
                    if student == name:
                        suffix = "th"
                        if pos == 1: suffix = "st"
                        elif pos == 2: suffix = "nd"
                        elif pos == 3: suffix = "rd"
                        print(f"{name} is in position {pos}{suffix}")
                        break
            except ValueError:
                print("Invalid score. Please enter a number.")

            if input("See everyone's scores? (yes/no): ").lower() == "yes":
                for student, score in students_score.items():
                    print(f"{student}: {score}")

            if input("See other student names? (yes/no): ").lower() == "yes":
                display_student_names(students_score)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Ensure correct name format with capital letters. Contact support for help.")
