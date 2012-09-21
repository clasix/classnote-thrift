# Global
typedef i32 ID
typedef string Guid
typedef i64 timestamp

# Auth

struct AuthResponse {
    1: required string      auth_token,
    2: required timestamp   expire_in,
    3: required i64         user_id
}

# User

enum UserGender {
    Unknown = 0,
    Male = 1,
    Female = 2
}

enum WeekDay {
    Sunday,
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday
}

struct User {
    1: required i64     gid,
    2: required string  name,
    3: required UserGender  gender
}

struct Class {
    1: required i64     gid,
    2: optional string  school,
    3: optional string  dept,
    4: optional string  major,
    5: optional i16     year
}

struct Course {
    1: required i64     gid,
    2: required string  name,
    3: optional string  tearcher,
    4: optional string  book,
    5: optional Class   for_class,
    6: optional i16     for_semster
}

struct LessonInfo {
    1: required i64     gid,
    2: optional Course  course,
    3: optional string  room,
    4: optional i16     weekday,
    5: optional i16     start,
    6: optional i16     duration
}

struct LessonTable {
    1: required i64     gid,
    2: required i64     user_id,
    3: optinal  i16     semester,
    4: optinal  list<LessonInfo> lessoninfos
}
