USE mazle;

CREATE TABLE drink(
    `drink_id`          INTEGER         NOT NULL    AUTO_INCREMENT  COMMENT '음료ID',
    `drink_name`        VARCHAR(255)    NOT NULL    COMMENT '음료 명',
    `description`       TEXT            NOT NULL    COMMENT '설명',
    `calorie`           INTEGER         NOT NULL    COMMENT '칼로리',
    `manufacture`       VARCHAR(255)    NOT NULL    COMMENT '제조사',
    `price`             INTEGER         NOT NULL    COMMENT '예상가격',
    `large_category`    VARCHAR(50)     NOT NULL    COMMENT '대분류',
    `medium_category`   VARCHAR(50)     NOT NULL    COMMENT '중분류',
    `small_category`    VARCHAR(50)     NOT NULL    COMMENT '소분류',
    `img`               LONGBLOB                    COMMENT '이미지',
    `alchol`            INTEGER         NOT NULL    COMMENT '알콜도수',
    `measure`           INTEGER         NOT NULL    COMMENT '용량(ml)',
    `caffeine`          INTEGER         NOT NULL    COMMENT '카페인(ml)',
    PRIMARY KEY (`drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 테이블';


CREATE TABLE drink_allergy(
    `drink_id`         INTEGER         NOT NULL    COMMENT '음료ID',
    `allergy`          VARCHAR(255)    NOT NULL    COMMENT '알레르기',
    PRIMARY KEY (`drink_id`, `allergy`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 알레르기 테이블';


CREATE TABLE drink_tag(
    `drink_id`          INTEGER         NOT NULL    COMMENT '음료ID',
    `tag`               VARCHAR(50)     NOT NULL    COMMENT '태그',
    PRIMARY KEY (`drink_id`, `tag`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 태그 테이블';


CREATE TABLE drink_comment(
    `comment_id`        INTEGER         NOT NULL    AUTO_INCREMENT  COMMENT '댓글ID',
    `drink_id`          INTEGER         NOT NULL    COMMENT '음료ID',
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `comment`           VARCHAR(255)    NOT NULL    COMMENT '댓글',
    `score`             FLOAT(3,1)                  COMMENT '별점',
    PRIMARY KEY (`comment_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='음료 댓글 테이블';


CREATE TABLE drink_like(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `drink_id`          INTEGER         NOT NULL    COMMENT '음료ID',
    PRIMARY KEY (`customer_uuid`, `drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='좋아요한 음료 테이블';


CREATE TABLE drink_comment_like(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `comment_id`        INTEGER         NOT NULL    COMMENT '댓글ID',
    PRIMARY KEY (`customer_uuid`, `comment_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='좋아요한 음료 댓글 테이블';
