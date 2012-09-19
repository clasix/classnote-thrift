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

    bool sign_up_email(
        1: string email,
        2: string password
    )

    bool sign_up_username(
        1: string username,
        2: string password
    )

    bool sign_out(
        1: string auth_token
    )

/*
    void sign_up (
        1: string mail,
        2: string password
    )

    type.AuthResponse sign_in (
        1: string mail,
        2: string password
    )

    void logout(
        1: string   auth_token
    )
*/

    # User
    type.User user_get(
        1: string       auth_token,
        2: i64          gid
    )

    void user_set(
        1: string   auth_token,
        2: type.User    user
    )
}
