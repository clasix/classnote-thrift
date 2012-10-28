include "type.thrift"

struct SyncState {
    1: required type.timestamp currentTime,
    2: required type.timestamp fullSyncBefore,
    3: required i32     updateCount,
}

# missing lessontableitem
struct SyncChunk {
    1: required type.timestamp currentTime,
    2: optional i32 chunkHighUSN,
    3: optional i32 updateCount,
    4: optional list<type.Course> courses,
    5: optional list<type.LessonInfo> lessonInfos,
    6: optional list<type.LessonTable> lessonTables
}

/**
 * this structure is used with the 'getFilteredSyncChunk' call to provide
 * fine-grained control over the data that's returned when a client needs to synchronize with the service.
 */
struct SyncChunkFilter {
    1: optional bool includeCourses,
    2: optional bool includeLessonInfos,
    3: optional bool includeLessonTables
}

service ClassNote {
    # Already used

    type.AuthResponse login_by_email(
        1: string email,
        2: string password
    ) 

    bool sign_up_email(
        1: string email,
        2: string password
    )

    bool sign_out(
        1: string auth_token
    )

    list<type.LessonTable> get_lessontables(
        1: string   auth_token
    )

    bool create_lessontable(
        1: string   auth_token
    )

    list<string> dept_provinces(
        1: string   auth_token
    )

    list<string> dept_schools(
        1: string   auth_token,
        2: string   province
    )

    list<string> dept_departments(
        1: string   auth_token,
        2: string   province,
        3: string   school
    )

    string dept_code(
        1: string   auth_token,
        2: string   province,
        3: string   school,
        4: string   dept
    )

    /*===== Synchronization functions for caching clients ====*/
    SyncState getSyncState(
        1: string auth_token
    )

    SyncChunk getSyncChunk(
        1: string auth_token,
        2: i32  afterUSN,
        3: i32  maxEntries,
        4: bool fullSyncOnly
    )

    SyncChunk getFilteredSyncChunk(
        1: string auth_token,
        2: i32  afterUSN,
        3: i32  maxEntries,
        4: SyncChunkFilter  filter
    )

    SyncState getSchoolLessonSyncState(
        1: string auth_token,
        2: string school_code
    )

    SyncChunk getSchoolLessonSyncChunk(
        1: string auth_token,
        2: string school_code,
        3: i32  afterUSN,
        4: i32  maxEntries,
        5: bool fullSyncOnly
    )

    # return the newly created course, with server-side guid
    type.Course createCourse(
        1: string auth_token,
        2: type.Course  course
    )

    # return USN
    i32 updateCourse(
        1: string auth_token,
        2: type.Course  course
    )

    # return USN
    i32 expungeCourse(
        1: string   auth_token,
        2: type.Guid    guid
    )

    # User
    type.User user_get(
        1: string       auth_token,
        2: i64          user_id
    )

    bool lessontable_set(
        1:string        auth_token,
        2:i64           user_id,
        3:list<type.LessonTable>    lesson_tables
    )

    type.AuthResponse login_by_username(
        1: string username,
        2: string password
    )

    bool sign_up_username(
        1: string username,
        2: string password
    )
}
