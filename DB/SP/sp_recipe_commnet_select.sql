CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_comment_select` (
     IN i_recipe_id     VARCHAR(40)     -- 레시피ID
    ,OUT `o_out_code`   SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_comment_select : 레시피 댓글 조회
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

    -- 1. recipe 조회
    SELECT MU.`nickname`
         , RC.`commnet`
         , RC.`score`
         , (SELECT COUNT(*) FROM recipe_comment_like WHERE R.recipe_id = i_recipe_id) as `like_cnt`
    FROM recipe_comment AS RC
    LEFT JOIN (
        SELECT customer_uuid
             , nickname
        FROM mazle_user
    ) AS MU ON MU.customer_uuid=RC.customer_uuid
    WHERE RC.recipe_id = i_recipe_id;

    -- 2. recipe 댓글 총 개수 조회(for 내부 페이지네이션)
    SELECT COUNT(*) as `cnt`
    FROM recipe_comment
    WHERE recipe_id = i_recipe_id;

END