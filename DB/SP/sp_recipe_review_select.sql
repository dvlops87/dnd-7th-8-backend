CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_review_select` (
     IN i_recipe_id     VARCHAR(40)     -- 레시피ID
    ,IN i_offset        INTEGER         -- 스킵 개수
    ,IN i_limit         INTEGER         -- 노출 개수
    ,OUT `o_out_code`   SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 리뷰 조회
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


    SELECT U.nickname
         , RC.comment
         , RC.score
    FROM recipe_comment RC
    LEFT JOIN (
        SELECT customer_uuid
             , nickname
        FROM mazle_user
    ) U ON U.customer_uuid=RC.customer_uuid
    WHERE RC.recipe_id = i_recipe_id
    LIMIT i_offset, i_limit;


    SELECT COUNT(*) AS `cnt`
    FROM recipe_comment RC
    WHERE RC.recipe_id = i_recipe_id;


END