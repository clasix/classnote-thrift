enum ExceptionCode {
    PERMISSION_DENIED = 101,
    INNER_ERROR = 102,
    NOT_FOUND = 103
}

exception Exception {
    1: optional ExceptionCode code,
    2: optional string message
}
