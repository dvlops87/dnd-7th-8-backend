CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_drink_set` (
     IN `i_drink_name`        VARCHAR(255)
    ,IN `i_description`       TEXT
    ,IN `i_calorie`           INTEGER
    ,IN `i_manufacture`       VARCHAR(255)
    ,IN `i_price`             INTEGER
    ,IN `i_large_category`    VARCHAR(50)
    ,IN `i_medidum_category`  VARCHAR(50)
    ,IN `i_small_category`    VARCHAR(50)
    ,IN `i_img`               LONGBLOB
    ,IN `i_alcohol`           INTEGER
    ,IN `i_measure`           INTEGER
    ,IN `i_caffeine`          INTEGER
    ,OUT `o_drink_id`         INTEGER
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_drink_set : 음료 데이터 인서트
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-15
---------------------------------------------------------------------------- */ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION, NOT FOUND, SQLWARNING
    BEGIN
        GET DIAGNOSTICS CONDITION 1 @v_sql_state = RETURNED_SQLSTATE
                , @v_error_no = MYSQL_ERRNO
                , @v_error_msg = MESSAGE_TEXT;
                SELECT @v_error_msg ; 
        ROLLBACK;
        SET o_out_code = -99;
    END;

    SET o_out_code = 0;


    START TRANSACTION;

    -- 1. 데이터 인서트
    INSERT INTO drink (
         `drink_name`
        ,`description`
        ,`calorie`
        ,`manufacture`
        ,`price`
        ,`large_category`
        ,`medium_category`
        ,`small_category`
        ,`img`
        ,`alcohol`
        ,`measure`
        ,`caffeine`
    ) VALUES (
         `i_drink_name`
        ,`i_description`
        ,`i_calorie`
        ,`i_manufacture`
        ,`i_price`
        ,`i_large_category`
        ,`i_medidum_category`
        ,`i_small_category`
        ,`i_img`
        ,`i_alcohol`
        ,`i_measure`
        ,`i_caffeine`
    );

    -- 2. drink_id SET
    SET o_drink_id = LAST_INSERT_ID();

    COMMIT;

END