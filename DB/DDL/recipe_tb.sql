USE mazle;

CREATE TABLE recipe(
    `recipe_id`         INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '레시피ID',
    `recipe_name`       VARCHAR(255)    NOT NULL    COMMENT '레시피 명',
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `summary`           VARCHAR(255)    NOT NULL    COMMENT '한 줄 설명',
    `description`       TEXT            NOT NULL    COMMENT '설명',
    `img`               LONGBLOB                    COMMENT '이미지',
    `price`             INTEGER         NOT NULL    COMMENT '예상가격',
    `measure_standard`  VARCHAR(50)     NOT NULL    COMMENT '계량기준',
    `tip`               VARCHAR(255)    NOT NULL    COMMENT '팁',
    `diff_score`        FLOAT(3,1)      NOT NULL    COMMENT '난이도점수',
    `price_score`       FLOAT(3,1)      NOT NULL    COMMENT '가성비점수',
    `sweet_score`       FLOAT(3,1)      NOT NULL    COMMENT '단맛점수',
    `alchol_score`      FLOAT(3,1)      NOT NULL    COMMENT '알콜점수',
    PRIMARY KEY (`recipe_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='레시피 테이블';


CREATE TABLE recipe_main_meterial(
    `recipe_id`         INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '레시피ID',
    `drink_id`          INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '음료ID',
    PRIMARY KEY (`recipe_id`, `drink_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='레시피 메인 재료(음료) 테이블';


CREATE TABLE recipe_sub_meterial(
    `recipe_id`         INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '레시피ID',
    `meterial_id`       INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '재료ID',
    PRIMARY KEY (`recipe_id`, `meterial_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='레시피 부재료 테이블';


CREATE TABLE recipe_meterial(
    `meterial_id`       INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '재료ID',
    `meterial_name`     VARCHAR(255)    NOT NULL    COMMENT '재료명',
    `img`               LONGBLOB                    COMMENT '이미지',
    PRIMARY KEY (`meterial_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='레시피 부재료 테이블';


CREATE TABLE recipe_tag(
    `recipe_id`         INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '레시피ID',
    `tag`               VARCHAR(50)     NOT NULL    COMMENT '태그',
    PRIMARY KEY (`recipe_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='레시피 태그 테이블';


CREATE TABLE recipe_comment(
    `recipe_id`         INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '레시피ID',
    `comment_id`        INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '댓글ID',
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `comment`           VARCHAR(255)    NOT NULL    COMMENT '댓글',
    `score`             FLOAT(3,1)                  COMMENT '별점',
    PRIMARY KEY (`recipe_id`, `comment_id`, `customer_uuid`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='레시피 댓글 테이블';


CREATE TABLE recipe_like(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `recipe_id`         INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '레시피ID',
    PRIMARY KEY (`customer_uuid`, `recipe_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='좋아요한 레시피 테이블';


CREATE TABLE recipe_comment_like(
    `customer_uuid`     VARCHAR(40)     NOT NULL    COMMENT '유저고유ID',
    `comment_id`        INTEGER         NOT NULL    AUTO_INCREMENT    COMMENT '댓글ID',
    PRIMARY KEY (`customer_uuid`, `comment_id`)
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT='좋아요한 레시피 댓글 테이블';
