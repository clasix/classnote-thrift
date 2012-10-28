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
    4: optional string  dept_code,
    5: optional i16     year
}

struct Clazz {
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
    5: optional string  school_code,
    6: optional string  dept_code,
    7: optional i16     semester,
    8: optional i16     year,
    9: optional i32     updateSequenceNum
}

struct LessonInfo {
    1: required i64     gid,
    2: optional Course  course,
    3: optional string  room,
    4: optional i16     weekday,
    5: optional i16     start,
    6: optional i16     duration,
    7: optional i32     updateSequenceNum
}

struct LessonTable {
    1: required i64     gid,
    2: required i64     user_id,
    3: optional  i16     semester,
    4: optional i32     updateSequenceNum,
    5: optional  list<LessonInfo> lessoninfos
}

struct LessonTableItem {
    1: required i64     gid,
    2: optional i64     table_id,
    3: optional i64     lesson_info_id,
    4: optional i32     updateSequenceNum
}

