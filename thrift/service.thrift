include "type.thrift"

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

    # User
    type.User user_get(
        1: string       auth_token,
        2: i64          user_id
    )

    list<type.LessonTable> lessontable_get(
        1: string       auth_token,
        2: i64          user_id
    )

    bool lessontable_set(
        1:string        auth_token,
        2:i64           user_id,
        3:list<type.LessonTable>    lesson_tables
    )

    list<type.Course> courses_get_by_class(
        1: type.Clazz         clazz
    )

    bool course_add(
        1: type.Course   course
    )

    bool course_set(
        1: type.Course course
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
