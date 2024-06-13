CREATE TYPE visibility AS ENUM (
  'Public',
  'Private'
);

CREATE TABLE teacher (
    id serial PRIMARY KEY,
    name varchar(100),
    city varchar(100)
);

CREATE TABLE webinar (
  id serial PRIMARY KEY,
  name varchar(200) NOT NULL,
  teacher_id integer,
  visibility visibility DEFAULT 'Public' NOT NULL,
  starts_on timestamp with time zone,
  ends_on timestamp with time zone,
  FOREIGN KEY (teacher_id) REFERENCES teacher(id)
);

CREATE TABLE student (
  id serial PRIMARY KEY,
  name varchar(100) NOT NULL,
  city varchar(100),
  mentor_id integer,
  FOREIGN KEY (mentor_id) REFERENCES teacher(id)
);

CREATE TABLE registration (
  student_id integer,
  webinar_id integer,
  date timestamp with time zone,
  PRIMARY KEY (student_id, webinar_id),
  FOREIGN KEY (student_id) REFERENCES student(id),
  FOREIGN KEY (webinar_id) REFERENCES webinar(id)
);
