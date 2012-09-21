include "type.thrift"

service ClassNote {
    string login_by_email(
        1: string email,
        2: string password
    ) 

    string login_by_username(
        1: string username,
        2: string password
    )

    type.AuthResponse sign_up_email(
        1: string email,
        2: string password
    )

    type.AuthResponse sign_up_username(
        1: string username,
        2: string password
    )

    bool sign_out(
        1: string auth_token
    )

    # User
    type.User user_get(
        1: string       auth_token,
        2: i64          user_id
    )

    list<type.LessonTable> lessontable_get(
        1: string       auth_token,
        2: i64          user_id
    )

    boolean lessontable_set(
        1:string        auth_token,
        2:i64           user_id,
        3:list<type.LessonTable>    lesson_tables
    )

    list<type.Course> courses_get_by_class(
        1:Class         class
    )

    boolean course_add(
        1: Course   course
    )

    boolean course_set(
        1: Course course
    )
}
