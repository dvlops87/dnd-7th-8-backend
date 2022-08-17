CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_sect` (
     IN `i_customer_uuid`     VARCHAR(40)      -- 유저ID
    ,IN `i_recipe_name`       VARCHAR(255)     -- 레시피명
    ,IN `i_summary`           VARCHAR(255)
    ,IN `i_description`       TEXT
    ,IN `i_img`               LONGBLOB
    ,IN `i_price`             INTEGER
    ,IN `i_measure_standard`  VARCHAR(50)
    ,IN `i_tip`               VARCHAR(255)
    ,IN `i_diff_score`        FLOAT(3,1)
    ,IN `i_price_score`       FLOAT(3,1)
    ,IN `i_sweet_score`       FLOAT(3,1)
    ,IN `i_alcohol_score`     FLOAT(3,1)
    ,OUT `o_recipe_id`        INTEGER
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_set : 레시피 등록
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-16
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
    INSERT INTO recipe(
     `customer_uuid`
    ,`recipe_name`
    ,`summary`    
    ,`description`
    ,`img`
    ,`price`
    ,`measure_standard`
    ,`tip`
    ,`diff_score`
    ,`price_score`
    ,`sweet_score`
    ,`alcohol_score`
    ) VALUES (
     `i_customer_uuid`
    ,`i_recipe_name`
    ,`i_summary`    
    ,`i_description`
    ,`i_img`
    ,`i_price`
    ,`i_measure_standard`
    ,`i_tip`
    ,`i_diff_score`
    ,`i_price_score`
    ,`i_sweet_score`
    ,`i_alcohol_score`
    );

    -- 2. recipe_id SET
    SET o_recipe_id = LAST_INSERT_ID();

    COMMIT;

END