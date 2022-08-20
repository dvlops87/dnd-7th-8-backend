CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_like_delete` (
     IN `i_customer_uuid`     VARCHAR(40)      -- 유저ID
    ,IN `i_recipe_id`         INTEGER          -- 레시피ID
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_like_set : 레시피 좋아요 삭제
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-19
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

    -- 1. 데이터 삭제
    DELETE FROM recipe_like
    WHERE customer_uuid=i_customer_uuid
      AND recipe_id=i_recipe_id;

    COMMIT;

END