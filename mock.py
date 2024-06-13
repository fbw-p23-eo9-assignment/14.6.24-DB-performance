from random import random, randrange
from progressbar import ProgressBar
from datetime import datetime, timedelta

OUTPUT_FILE = "data.sql"

NAME_PREFIX = ('Hands on', 'Introduction to', 'Advanced', 'Use case: ', 'Expert talk: ')

NAME_MAIN = ('Python', 'Computer', 'Django', 'Databases', 'Django Admin', 'Django ORM',
             'Django Templates', 'Python OOP', 'Python Algorithms', 'Bash Scripting',
             'Java', 'JavaScript', 'C#', 'Ruby', 'Vue.js', 'React', 'Web Mapping')


def rand(options):
    """Pick an item randomly."""
    index = int(random() * len(options))
    return options[index]


def composed_name(prefix=NAME_PREFIX, suffix=NAME_MAIN):
    """Return a random name."""
    return rand(prefix) + ' ' + rand(suffix)


def date(start=None, end=None):
    """Return a random date after start."""
    start_date = datetime.strptime(start, '%Y-%M-%d')
    if not end:
        end_date = datetime.now()
    else:
        end_date = end
    time_between_dates = end_date - start_date
    days_between_dates = int(time_between_dates.total_seconds())
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + timedelta(seconds=random_number_of_days)
    return random_date


def rand_integer(min=0, max=10000):
    """Return a random integer."""
    return randrange(max - min) + min


def fk(total, null=True):
    """Return a random foreign key."""
    _id = randrange(total)
    if _id == 0:
        if null:
            return "NULL"
        return _id + 1
    return _id


bar = ProgressBar(width=100)
# teachers
table = 'teacher'
# sql = "BEGIN;\n"
sql = f"INSERT INTO {table}(name, city) VALUES\n"
num_teachers = 105020

FIRST_NAMES = ('Abdul', 'David', 'Julia', 'Arnold', 'Bernhard', 'Gerald', 'Anna', 'Yussef', 'Itziar', 'Olivia', 'Emma', 'Amelia', 'Mia', 'Chloe', 'Penelope', 'Grace', 'Layla', 'Ella', 'Abigail', 'Camila', 'Gianna', 'Evelyn', 'Aaliyah', 'Naomi', 'Aarya', 'Araceli', 'Yamileth', 'Loretta', 'Liam', 'Noah', 'William', 'Lucas', 'Benjamin', 'Marc', 'Oriol', 'Arturo', 'Keith', 'Zain', 'Johann', 'Nikolas', 'Ahmed', 'Albert', 'Mathew', 'Gemma', 'Ester', 'Carmen', 'Abdel')

LAST_NAMES = ('Smith', 'Blanc', 'Müller', 'Miller', 'Muller', 'Griesebner', 'Hutticher', 'Karnasiotti', 'Martí', 'Vidal', 'Masferrer', 'Doe', 'Adams', 'Anniston', 'Hunter', 'Swcharzenegger', 'White', 'Black', 'Green', 'Schumacher', 'Perez', 'Fiedler', "O''Connor", "McDonald", 'Johnson', 'Williams', 'Brown', 'Garcia', 'Jones', 'Davis', 'Wilson', 'Moore', 'Jackson', 'Lee', 'Ali', 'Ahmas', 'Sanhchez', 'Clark', 'Hill', 'Young', 'Wright', 'Lewis', 'Nguyen', 'Allen', 'Köpfen', 'Strobl')

CITIES = ("Marseille", "Barcelona", "Paris", "Berlin", "Brussels", "New York", "Chicago", "Madrid", "Munich", "Girona", "Toulouse", "Prague", "Salzburg", "Leipzig", "Dresden", "Stuttgart", "Tubingen", "Frankfurt", "Dortmund", "Antwerp", "Metz", "Dijon", "Sheffield", "Leeds", "Cardiff", "Dublin", "Seattle", "Los Angeles", "San Diego", "Vancouver", "Ottawa", "Porto Alegre", "Rosario", "Johannesburg", "Muscat", "Bilbao", "Malmö", "Guangzhou", "Xiamen", "Kunimng", "Melbourne", "Sydney", "Adelaide", "Mildura", "Auckalnd", "Moscow", "Donetsk", "Kiev", "Sarajevo", "Budapest", "Graz", "Viena", "Roma", "San Marino", "Venice", "Naples", "Bern", "Lausanne", "Basel", "Hallein", 'Lyon', "Stockholm", "Salt", "Las Vegas")

bar.start(title=f"Producing {num_teachers} records for table <{table}>", total=num_teachers)
for i in range(0, num_teachers):
    bar.tick(i)
    name = composed_name(FIRST_NAMES, LAST_NAMES)
    sql = sql + f"\t('{name}', '{rand(CITIES)}')"
    if i < num_teachers - 1:
        sql = sql + ",\n"
    else:
        sql = sql + ";"
bar.end()
# sql += "\nCOMMIT;"
with open(OUTPUT_FILE, "w") as file:
    file.write(sql)

# students
table = 'student'
# sql = "BEGIN;\n"
sql = f"INSERT INTO {table}(name, city, mentor_id) VALUES\n"
num_students = 1295840
bar.start(title=f"Producing {num_students} records for table <{table}>", total=num_students)
for i in range(0, num_students):
    bar.tick(i)
    name = composed_name(FIRST_NAMES, LAST_NAMES)
    teacher_id = fk(num_teachers)
    sql = sql + f"\t('{name}', '{rand(CITIES)}', {teacher_id})"
    if i < num_students - 1:
        sql = sql + ",\n"
    else:
        sql = sql + ";"
bar.end()
# sql += "\nCOMMIT;"
with open(OUTPUT_FILE, "a") as file:
    file.write("\n\n")
    file.write(sql)


# webinars
table = 'webinar'
# sql = "BEGIN;\n"
sql = f"INSERT INTO {table}(name, teacher_id, visibility, starts_on, ends_on) VALUES\n"
num_webinars = 284310
bar.start(title=f"Producing {num_webinars} records for table <{table}>", total=num_webinars)
for i in range(0, num_webinars):
    bar.tick(i)
    option = rand(['Public', 'Private'])
    start = date(start='2005-08-10')
    end = date(start=datetime.strftime(start, '%Y-%m-%d'),
               end=start + timedelta(hours=8))
    teacher = fk(num_teachers)
    sql = sql + f"\t('{composed_name()}', {teacher}, '{option}', '{start}', '{end}')"
    if i < num_webinars - 1:
        sql = sql + ",\n"
    else:
        sql = sql + ";"
bar.end()
# sql += "\nCOMMIT;"
with open(OUTPUT_FILE, "a") as file:
    file.write("\n\n")
    file.write(sql)


# registration
table = 'registration'
# sql = "BEGIN;\n"
sql = f"INSERT INTO {table}(student_id, webinar_id, date) VALUES\n"
num_registrations = 1569750
bar.start(title=f"Producing {num_registrations} records for table <{table}>", total=num_registrations)
done = []
for i in range(0, num_registrations):
    bar.tick(i)
    # name = composed_name(FIRST_NAMES, LAST_NAMES)
    student_id = fk(num_students, null=False)
    webinar_id = fk(num_webinars, null=False)
    if (student_id, webinar_id) not in done:
        done.append((student_id, webinar_id))
    else:
        continue
    reg_date = date(start='2005-08-10')
    sql = sql + f"\t({student_id}, {webinar_id}, '{reg_date}')"
    if i < num_registrations - 1:
        sql = sql + ",\n"
    else:
        sql = sql + ";"
bar.end()
# sql += "\nCOMMIT;"
with open(OUTPUT_FILE, "a") as file:
    file.write("\n\n")
    file.write(sql)
