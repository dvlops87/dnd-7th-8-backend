CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_main_meterial_set` (
     IN `i_recipe_id`       INTEGER     -- 레시피ID
    ,IN `i_drink_id`        INTEGER     -- 음료ID
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 메인 재료 등록
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

    INSERT INTO recipe_main_meterial (
         `recipe_id`
        ,`drink_id`
    ) VALUES (
         `i_recipe_id`
        ,`i_drink_id`
    );

    COMMIT;

END