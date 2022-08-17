CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_delete` (
     IN i_recipe_id     VARCHAR(40)     -- 레시피ID
    ,IN i_customer_uuid VARCHAR(40)     -- 유저ID
    ,OUT `o_out_code`   SMALLINT
)

MAIN:BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_delete : 레시피 삭제
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


    -- 1. 해당 레시피가 유저가 작성한 레시피가 맞는지 검증
    SET @v_customer_uuid = (
        SELECT customer_uuid
        FROM recipe
        WHERE recipe_id = i_recipe_id
    );

    IF (@v_customer_uuid != i_customer_uuid)
    THEN
        SET o_out_code = -98;
        LEAVE MAIN;
    END IF;    

    -- 2. 레시피 삭제
    DELETE FROM recipe WHERE recipe_id=i_recipe_id;

END