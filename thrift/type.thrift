# Global

typedef i64 timestamp

# Auth

struct AuthResponse {
    1: required string      access_token,
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

struct Lesson {
    1: required i64     gid,
    2: required string  name,
    3: optional string  room
}

struct Class {
    1: required Lesson lesson,
    2: required WeekDay weekday,
    3: required i16     start,
    4: required i16     duration
}
