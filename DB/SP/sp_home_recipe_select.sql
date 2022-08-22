CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_home_recipe_select` (
     IN  `i_limit`       INT
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_home_recipe_select : 인기 레시피 조회
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

      -- 3. recipe 좋아요순 조회
      SELECT M.*
        FROM(
        SELECT R.`recipe_id`
             , U.`nickname`
             , R.`recipe_name`
             , R.`img`
             , R.`price`
             , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
             , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = R.`recipe_id`) as `like_cnt`
        FROM recipe AS R
        LEFT JOIN mazle_user U ON U.customer_uuid = R.customer_uuid
        ) M
      ORDER BY like_cnt DESC
      LIMIT i_limit;

END