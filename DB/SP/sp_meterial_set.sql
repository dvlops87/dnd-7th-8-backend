CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_meterial_set` (
     IN `i_meterial_name`     VARCHAR(255)
    ,IN `i_img`               LONGBLOB
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_meterial_set : 부재료 데이터 인서트
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-20
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
    INSERT INTO recipe_meterial (
         `meterial_name`
        ,`img`
    ) VALUES (
         `i_meterial_name`
        ,`i_img`
    );

    COMMIT;

END