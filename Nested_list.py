"""There are  students in this class whose names and grades are assembled to build the following list:

python students = [['Harry', 37.21], ['Berry', 37.21], ['Tina', 37.2], ['Akriti', 41], ['Harsh', 39]]

The lowest grade of  belongs to Tina. The second-lowest grade of  belongs to both Harry and Berry, so we order their names alphabetically and print each name on a new line."""


# Read number of students
n = int(input("""Enter a number: """))

# Collect student data in a nested list
students = []
for _ in range(n):
    name = input("""Enter a name: """)
    score = float(input("""Enter a score: """))
    students.append([name, score])

# Get all unique scores, sort them and find the second lowest
scores = sorted(set([s[1] for s in students]))
second_lowest = scores[1]

# Find all students with the second-lowest score
second_lowest_students = [s[0] for s in students if s[1] == second_lowest]

# Sort names alphabetically and print
for name in sorted(second_lowest_students):
    print(name)
