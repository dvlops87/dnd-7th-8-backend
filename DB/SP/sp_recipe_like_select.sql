CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_like_select` (
     IN i_customer_uuid     VARCHAR(40)     -- 유저ID, NOT NULL
    ,IN i_recipe_id         VARCHAR(40)     -- 레시피ID
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_like_select : 레시피 좋아요 조회
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-07
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

    IF (i_recipe_id IS NOT NULL)
    THEN
        -- 1. 해당 RECIPE에 대해 좋아요 여부
        SELECT recipe_id
        FROM recipe_like
        WHERE customer_uuid=i_customer_uuid
          AND recipe=i_recipe_id;

    ELSE
        -- 2. 유저 전제 레시피 좋아요 여부
        SELECT recipe_id
        FROM recipe_like
        WHERE customer_uuid=i_customer_uuid;

    END IF;

END