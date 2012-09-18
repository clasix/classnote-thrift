include "type.thrift"

service ClassNote {
    # Ping Test
    string ping(
        1: string   input
    )

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
