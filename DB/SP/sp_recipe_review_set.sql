CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_review_set` (
     IN `i_recipe_id`       VARCHAR(40)     -- 레시피ID
    ,IN `i_customer_uuid`   VARCHAR(40)     -- 유저ID
    ,IN `i_comment`         VARCHAR(255)    -- 댓글
    ,IN `i_score`           FLOAT(3,1)      -- 별점
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 리뷰 등록
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

    INSERT INTO recipe_comment (
         `recipe_id`
        ,`customer_uuid`
        ,`comment`
        ,`score`
    ) VALUES (
         `i_recipe_id`
        ,`i_customer_uuid`
        ,`i_comment`
        ,`i_score`
    );

    COMMIT;

END