USE mazle;

CREATE TABLE drink(
    `drink_id`          VARCHAR(40)     NOT NULL    COMMENT '음료ID',
    `drink_name`        VARCHAR(255)    NOT NULL    COMMENT '음료 명',
    `description`       TEXT            NOT NULL    COMMENT '설명',
    `calorie`           INTEGER                     COMMENT '칼로리',
    `manufacture`       VARCHAR(255)    NOT NULL    COMMENT '제조사',
    `price`             INTEGER         NOT NULL    COMMENT '예상가격',
    `lagrge_category`   VARCHAR(50)                 COMMENT '대분류',
    `medium_category`   VARCHAR(50)                 COMMENT '중분류',
    `small_category`    VARCHAR(50)                 COMMENT '소분류',
    `img`               LONGBLOB                    COMMENT '이미지',
    `alchol`            FLOAT(5,3)                  COMMENT '알콜도수',
    `caffeine`          FLOAT(5,3)                  COMMENT '카페인(ml)',
    PRIMARY KEY (`drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 테이블';


CREATE TABLE drink_allergy(
    `drink_id`         VARCHAR(40)     NOT NULL    COMMENT '음료ID',
    `allergy`          VARCHAR(255)    NOT NULL    COMMENT '알레르기',
    PRIMARY KEY (`drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 알레르기 테이블';


CREATE TABLE drink_tag(
    `drink_id`          VARCHAR(40)     NOT NULL    COMMENT '음료ID',
    `tag`               VARCHAR(50)     NOT NULL    COMMENT '태그',
    PRIMARY KEY (`drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 태그 테이블';


CREATE TABLE drink_comment(
    `drink_id`          VARCHAR(40)     NOT NULL    COMMENT '음료ID',
    `comment_id`        VARCHAR(40)     NOT NULL    COMMENT '댓글ID',
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `comment`           VARCHAR(255)    NOT NULL    COMMENT '댓글',
    `score`             FLOAT(4,2)                  COMMENT '별점',
    PRIMARY KEY (`drink_id`, `comment_id`, `customer_uuid`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 댓글 테이블';


CREATE TABLE drink_like(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `drink_id`          VARCHAR(40)     NOT NULL    COMMENT '음료ID',
    PRIMARY KEY (`customer_uuid`, `drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='좋아요한 음료 테이블';


CREATE TABLE drink_comment_like(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `comment_id`        VARCHAR(40)     NOT NULL    COMMENT '댓글ID',
    PRIMARY KEY (`customer_uuid`, `comment_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='좋아요한 음료 댓글 테이블';
