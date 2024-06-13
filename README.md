# Database Performance

## Description

In this exercise, you will practice the optimization of databases and queries.

## Data

The following tasks will be using a data set that you have already seen in previous exercises:

**Teacher** (105,020 rows)
```sql
                                    Table "public.teacher"
 Column |          Type          | Collation | Nullable |               Default               
--------+------------------------+-----------+----------+-------------------------------------
 id     | integer                |           | not null | nextval('teacher_id_seq'::regclass)
 name   | character varying(100) |           |          |
 city   | character varying(100) |           |          |
Indexes:
    "teacher_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "student" CONSTRAINT "student_mentor_id_fkey" FOREIGN KEY (mentor_id) REFERENCES teacher(id)
    TABLE "webinar" CONSTRAINT "webinar_teacher_id_fkey" FOREIGN KEY (teacher_id) REFERENCES teacher(id)
```

**Student** (1,295,840 rows)
```sql
                                     Table "public.student"
  Column   |          Type          | Collation | Nullable |               Default               
-----------+------------------------+-----------+----------+-------------------------------------
 id        | integer                |           | not null | nextval('student_id_seq'::regclass)
 name      | character varying(100) |           | not null |
 city      | character varying(100) |           |          |
 mentor_id | integer                |           |          |
Indexes:
    "student_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "student_mentor_id_fkey" FOREIGN KEY (mentor_id) REFERENCES teacher(id)
Referenced by:
    TABLE "registration" CONSTRAINT "registration_student_id_fkey" FOREIGN KEY (student_id) REFERENCES student(id)
```

**Webinar** (284,310 rows)
```sql
                                       Table "public.webinar"
   Column   |           Type           | Collation | Nullable |               Default               
------------+--------------------------+-----------+----------+-------------------------------------
 id         | integer                  |           | not null | nextval('webinar_id_seq'::regclass)
 name       | character varying(200)   |           | not null |
 teacher_id | integer                  |           |          |
 visibility | visibility               |           | not null | 'Public'::visibility
 starts_on  | timestamp with time zone |           |          |
 ends_on    | timestamp with time zone |           |          |
Indexes:
    "webinar_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "webinar_teacher_id_fkey" FOREIGN KEY (teacher_id) REFERENCES teacher(id)
Referenced by:
    TABLE "registration" CONSTRAINT "registration_webinar_id_fkey" FOREIGN KEY (webinar_id) REFERENCES webinar(id)
```

**Registration** (1,569,746 rows)
```sql
                      Table "public.registration"
   Column   |           Type           | Collation | Nullable | Default
------------+--------------------------+-----------+----------+---------
 student_id | integer                  |           | not null |
 webinar_id | integer                  |           | not null |
 date       | timestamp with time zone |           |          |
Indexes:
    "registration_pkey" PRIMARY KEY, btree (student_id, webinar_id)
Foreign-key constraints:
    "registration_student_id_fkey" FOREIGN KEY (student_id) REFERENCES student(id)
    "registration_webinar_id_fkey" FOREIGN KEY (webinar_id) REFERENCES webinar(id)
```

## Tasks

### Task 1

Create a database named `webinars`, connect to it and execute the file [data/tables.sql](data/tables.sql) in the PostgreSQL console or in DBeaver to create the required tables to start this exercise.

The data is located in the file [data/data.zip](data/data.zip). Unzip it to have access to the `data.sql` file that stores the data as SQL `INSERT` commands, one statement for each table.

> This file has a large amount of data, do not open the entire file. When you run it, do it from the command line.

Before doing anything else, open the PostgreSQL console and connect to the database to run the `\timing` command:

```sql
webinars=# \timing
Timing is on
```

> From now on, every operation you run will be timed and the time spent will be shown in the console.

Now, run the file. When it finishes, write down (or copy/paste in another document) the time spent on each table.

**Your result should look similar to this:**

> The order of the loading is: teacher, student, webinar and registration.
>
> The comments `--` have been added later to help read the output.

```sql
INSERT 0 105020 -- Teacher
Time: 1917.097 ms (00:01.917) -- about 2 seconds
INSERT 0 1295840 -- Student
Time: 52265.649 ms (00:52.266) -- almost 1 minute
INSERT 0 284310 -- Webinar
Time: 12826.275 ms (00:12.826) -- around 10 seconds
INSERT 0 1569746 -- Registration
Time: 153145.552 ms (02:33.146) -- 2.5 minutes
```

> You may experience faster times. These have been recorded on an instance running in an old hardware.


### Task 2

Your aim will be to rebuild the initial data, so that the previous task can be done  faster. Instead of using `INSERT` commands you will convert the `data.sql` file into `COPY` commands.

> Read about the [SQL COPY](https://www.postgresql.org/docs/current/sql-copy.html) command.

The `COPY` command can be very simple. It only requires the data to be stored in a text file with no header, with each row separated by a new line character and the values separated by tabulations.

Producing these files can be done also with the same `COPY` command.

Create a new file named `backup.sql` that uses `COPY` statements to create a data file for each table containing the entire data of that table (`teacher.csv`, `student.csv`, `webinar.csv` and `registration.csv`).

> The `COPY` command will create files on the server's file system. If you installed PostgreSQL in your local computer, it will create them in your local computer. If you are using a PostgreSQL instance in a server, it will create them in the server.

Then execute `backup.sql` to produce the 4 `.csv` files.

**Your result should look similar this:**

```sql
COPY 105020 -- Teacher
Time: 109.447 ms
COPY 1295840 -- Student
Time: 1332.641 ms (00:01.333) -- around 1.5 seconds
COPY 284310 -- Webinar
Time: 1375.702 ms (00:01.376) -- around 1.5 seconds
COPY 1569746 -- Registration
Time: 3569.617 ms (00:03.570) -- around 3.5 seconds
```

Check the first rows of each file to make sure it worked.

**Your result should look like this:**

```bash
user@computer:/home/user/$ head teachers.csv
1       Liam Griesebner Adelaide
2       Mia Lee Melbourne
3       Amelia McDonald Girona
4       Araceli Young   Cardiff
5       Yussef Green    Mildura
6       Olivia Karnasiotti      Las Vegas
7       Lucas Smith     Porto Alegre
8       Zain Brown      Porto Alegre
9       Benjamin Ali    Dortmund
10      Camila Schumacher       Moscow
user@computer:/home/user/$ head student.csv
1       Emma Anniston   Hallein 11260
2       Arturo Miller   Antwerp 47807
3       Julia Wright    Hallein 8783
4       Olivia Williams Budapest        4688
5       Aaliyah Garcia  Graz    76804
6       Evelyn McDonald Donetsk 41494
7       Aarya Brown     New York        96227
8       Aaliyah Hutticher       Vancouver       55108
9       Keith Hutticher Tubingen        87780
10      Penelope Garcia Guangzhou       64486
user@computer:/home/user/$ head webinar.csv
1       Hands on Web Mapping    34114   Private 2007-01-17 09:57:09+01  2007-01-17 08:40:16+01
2       Use case:  Vue.js       9663    Public  2019-06-13 11:06:15+02  2019-05-19 06:11:43+02
3       Hands on Java   19271   Private 2005-12-05 19:23:55+01  2005-01-30 14:26:22+01
4       Advanced Django ORM     99394   Public  2018-03-25 10:24:44+02  2018-02-05 13:00:33+01
5       Hands on Bash Scripting 77338   Private 2005-06-25 03:08:43+02  2005-05-20 17:40:57+02
6       Hands on Django Templates       103481  Private 2013-03-12 12:21:34+01  2013-02-07 19:59:08+01
7       Hands on Python OOP     93640   Private 2012-10-05 05:22:58+02  2012-09-03 07:28:19+02
8       Advanced Python OOP     68727   Private 2021-04-19 21:08:52+02  2021-03-22 02:10:00+01
9       Introduction to Django ORM      41629   Private 2021-10-11 18:49:10+02  2021-08-20 08:16:41+02
10      Advanced React  17507   Private 2012-01-16 07:39:16+01  2012-01-16 08:59:22+01
user@computer:/home/user/$ head registration.csv
350495  132769  2010-04-28 09:46:48+02
1162966 197473  2010-01-02 08:25:05+01
539829  34470   2012-01-14 15:40:46+01
60952   117160  2008-10-25 06:23:33+02
131647  276168  2017-06-03 03:28:14+02
835150  33106   2007-09-13 09:04:31+02
1112061 236890  2018-04-19 18:31:05+02
496639  11669   2011-07-14 20:32:41+02
771827  187989  2017-02-27 22:36:34+01
83584   283295  2010-07-29 16:27:34+02
```

> The `head` command works in Linux and Mac. In Windows, you can use the `type` command:
>
> ```
> type teachers.csv -Head 10
> ```

### Task 3

Now, create a new script named `reload.sql` using `COPY` statements to load those files into the tables again. As the name suggests, the script should clear up the tables first (remove all rows), and then load the `.csv` files again.

> Hint: Now, the order of the `COPY` statements is important. You cannot load a row that uses a foreign key that does not exist in the referenced table.

Execute the script `reload.sql`.

**Your result should look similar to this:**

```sql
COPY 105020 -- Teacher
Time: 439.540 ms -- more than 75% reduction
COPY 1295840 -- Student
Time: 32995.703 ms (00:32.996) -- almost 40% reduction
COPY 284310 -- Webinar
Time: 7694.004 ms (00:07.694) -- about 40% reduction
COPY 1569746 -- Registration
Time: 153250.587 ms (02:33.251) -- about 0% reduction
```

Compare your reported times with the ones you got on task 1.

### Task 4

Now, improve the `reload.sql` script even further.

> Hint: You just exported the data and the database has not changed, so you know the data is consistent.

**Your result should look similar to this:**

```sql
...
COPY 105020 -- Teacher
Time: 144.334 ms -- more than 90% reduction
COPY 1295840 -- Student
Time: 3393.400 ms (00:03.393) -- almost 95% reduction
COPY 284310 -- Webinar
Time: 1419.558 ms (00:01.420) -- almost 90% reduction
COPY 1569746 -- Registration
Time: 4340.091 ms (00:04.340) -- more than 95% reduction
...
```

> The output will contain more rows, and the overall reloading time is more than just the `COPY` statements, but it is still noticeably faster than any other test so far.

### Task 5

Look at the following query:

```
SELECT * FROM student, teacher
WHERE student.mentor_id = teacher.id
AND student.city = 'Berlin' OR teacher.city = 'Berlin';
```

Write an SQL query to estimate how much time this query could take.

> Hint: Do not execute it.

#### Questions

1. **How much time is the query estimated to take? how many rows will it return?**

2. **What is the query doing and what do you think it was meant to do?**

Fix the query so it does what it was supposed to do and find out how much time PostgreSQL estimates it could take now.

**Your result should look similar to this:**

```
                                             QUERY PLAN                                              
-----------------------------------------------------------------------------------------------------
 Hash Join  (cost=3745.95..72094.95 rows=39562 width=54)
   Hash Cond: (student.mentor_id = teacher.id)
   Join Filter: (((student.city)::text = 'Berlin'::text) OR ((teacher.city)::text = 'Berlin'::text))
   ->  Seq Scan on student  (cost=0.00..22427.40 rows=1295840 width=29)
   ->  Hash  (cost=1766.20..1766.20 rows=105020 width=25)
         ->  Seq Scan on teacher  (cost=0.00..1766.20 rows=105020 width=25)
(6 rows)
```


### Task 6

The following statement returns the list of registrations since 2019 to webinars from students living in Berlin.

```
SELECT * FROM registration
    JOIN student
    ON student.id = registration.student_id
WHERE city = 'Berlin' AND date > '2019-01-01';
```

Analyze the query to check the actual time it takes to execute the query.

**Your result should look similar to this:**

```
 ...
 Planning time: 0.472 ms
 Execution time: 693.793 ms
 ...
```

Then, find a way to cut the time in half.

**Your result should look similar to this:**

```
 ...
 Planning time: 0.753 ms
 Execution time: 326.102 ms
 ...
```

### Task 7

Now look at this other query. The query returns the list of students who live in a city where at least one teacher lives.

```
SELECT * FROM student
WHERE city IN (SELECT DISTINCT city FROM teacher);
```

Analyze it to write down the current execution time.

**Your result should look similar to this:**

```
 ...
 Planning time: 0.357 ms
 Execution time: 1603.506 ms
 ...
```

Now, find a way to reduce the execution time around 50% (anywhere around 45% should be enough).

**Your result should look similar to this:**

```
 ...
 Planning time: 0.179 ms
 Execution time: 858.846 ms
 ...
```

858.846 is a 53.6% of 1603.506, this is a **46.4% reduction** time over the initial one. It can be considered close to 50%.

### Task 8

Now look at the file [data/task8.py](data/task8.py). This Python file is connecting to the database to extract the list of students (and their mentors) who have been registered in a Django related webinar in 2021. Then it saves this list in a file named `students_query.csv` on the hard disk.

Test it by running it on the console:

```shell
user@computer:/home/DCI/$ python3 data/task8.py
It took 0:00:06.738656
```

> You will need to have the **psycopg2-binary** Python package in your virtual environment.

The script takes a few seconds to produce the result.

Improve the performance so it executes under one second.

**Your result should look similar to this:**

```shell
user@computer:/home/DCI/$ python3 data/task8.py
It took 0:00:00.553723
```
