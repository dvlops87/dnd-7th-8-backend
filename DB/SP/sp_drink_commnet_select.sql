CREATE DEFINER=`adminadmin`@`%` PROCEDURE `sp_drink_comment_select` (
     IN i_drink_id      VARCHAR(40)     -- 음료ID
    ,OUT `o_out_code`   SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_drink_comment_select : 음료 댓글 조회
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

    -- 1. drink 댓글 조회
    SELECT MU.`nickname`
         , DC.`comment`
         , DC.`score`
         , (SELECT COUNT(*) FROM drink_comment_like WHERE R.drink_id = i_drink_id) as `like_cnt`
    FROM drink_comment AS DC
    LEFT JOIN (
        SELECT customer_uuid
             , nickname
        FROM mazle_user
    ) AS MU ON MU.customer_uuid=DC.customer_uuid
    WHERE DC.drink_id = i_drink_id;

    -- 2. drink 댓글 총 개수 조회(for 내부 페이지네이션)
    SELECT COUNT(*) as `cnt`
    FROM drink_comment
    WHERE drink_id = i_drink_id;

END