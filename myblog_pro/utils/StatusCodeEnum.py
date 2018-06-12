from enum import IntEnum


class StatusCode(IntEnum):
    SUCCESS = 200,

    PARAMS_NOT_COMPLETE = 1000,

    # 用户相关
    USERNAME_NOT_EXISTS = 1001,
    USERNAME_EXISTS = 1002,
    PASSWORD_ERROR = 1003,

    # 文章类型相关
    TYPE_EXISTS = 2001,

    # 标签相关
    TAG_EXISTS = 3001,

    # 链接相关
    LINK_EXISTS = 4001,

