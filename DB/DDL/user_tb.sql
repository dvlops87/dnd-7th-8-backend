USE mazle;

CREATE TABLE mazle_user(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `email`             VARCHAR(255)    NOT NULL    COMMENT '이메일',
    `nickname`          VARCHAR(50)     NOT NULL    COMMENT '닉네임',
    `passwd`            VARCHAR(255)    NOT NULL    COMMENT '비밀번호',
    `birth`             DATE            NOT NULL    COMMENT '생년월일',
    `profile`           LONGBLOB                    COMMENT '프로필이미지',
    `platform`          ENUM('not_social', 'kakao')     NOT NULL    COMMENT '가입 플랫폼',
    PRIMARY KEY (`customer_uuid`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='유저 테이블';


CREATE TABLE mazle_user_consent(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `consent`           TINYINT(1)      NOT NULL    COMMENT '이용약관',
    `update_dtime`      DATETIME        NOT NULL    COMMENT '갱신일',
    PRIMARY KEY (`customer_uuid`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='이용약관 체크 여부 테이블';
