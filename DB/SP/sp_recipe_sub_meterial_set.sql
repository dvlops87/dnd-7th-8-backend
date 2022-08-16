CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_sub_meterial_set` (
     IN `i_recipe_id`       INTEGER     -- 레시피ID
    ,IN `i_meterial_id`     INTEGER     -- 재료ID
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 부재료 등록
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

    INSERT INTO recipe_sub_meterial (
         `recipe_id`
        ,`meterial_id`
    ) VALUES (
         `i_recipe_id`
        ,`i_meterial_id`
    );

    COMMIT;

END