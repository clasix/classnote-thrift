include "type.thrift"

service ClassNote {
    # Auth

    type.AuthResponse login_by_mail(
        1: i64      client_id,  # what the use of this?
        2: string   client_secret,
        3: string   mail,
        4: string   password
    )

    void logout(
        1: string   access_token
    )

    # User
    type.User user_get(
        1: string       access_token,
        2: i64          gid
    )

    void user_set(
        1: string   access_token,
        2: type.User    user
    )
}
