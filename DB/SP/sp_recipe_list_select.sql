CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_list_select`(
     IN i_offset            INT
    ,IN i_limit             INT
    ,IN i_search_keyword    VARCHAR(50)     -- 검색어(NULL 허용)
    ,IN i_order             SMALLINT        -- 좋아요순 정렬여부(NULL 허용)
    ,OUT `o_out_code`       SMALLINT
)
BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 리스트 조회(ES 구축 전 까지 임시 사용) 필터 X, 좋아요 정렬 기능만 제공
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

    IF (i_search_keyword IS NULL AND i_order IS NULL)
    THEN
        -- 1. recipe 디폴트 조회
        SELECT R.`recipe_id`
             , R.`recipe_name`
             , R.`img`
             , R.`price`
             , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
             , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = R.`recipe_id`) as `like_cnt`
        FROM recipe AS R
        LIMIT i_offset, i_limit;

        SELECT COUNT(*) as cnt
        FROM recipe;

    ELSEIF (i_search_keyword IS NOT NULL)
    THEN
      -- 2. recipe 검색어 조회
      SET @v_sql = CONCAT("
        SELECT M.*
        FROM(
            SELECT R.`recipe_id` 
                 , R.`recipe_name`
                 , R.`img`
                 , R.`price`
                 , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
                 , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = R.`recipe_id`) as `like_cnt`
            FROM recipe AS R
        ) M
        WHERE M.recipe_name LIKE '%",i_search_keyword,"%'
           OR M.tag='",i_search_keyword,"'
        LIMIT ",i_offset,",",i_limit,";");

      PREPARE stmt FROM @v_sql;
      EXECUTE stmt;
      DEALLOCATE PREPARE stmt;

      SET @v_sql = CONCAT("
        SELECT COUNT(*) as cnt
        FROM(
            SELECT R.`recipe_id`
                 , R.`recipe_name`
                 , R.`price`
                 , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
            FROM recipe AS R
        ) M
        WHERE M.recipe_name LIKE '%",i_search_keyword,"%'
           OR M.tag='",i_search_keyword,"';
        ");

      PREPARE stmt FROM @v_sql;
      EXECUTE stmt;
      DEALLOCATE PREPARE stmt;

    ELSEIF (i_order IS NOT NULL)
    THEN
      -- 3. recipe 좋아요순 조회
      SELECT M.*
        FROM(
        SELECT R.`recipe_id`
             , R.`recipe_name`
             , R.`img`
             , R.`price`
             , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
             , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = R.`recipe_id`) as `like_cnt`
        FROM recipe AS R
        ) M
        ORDER BY like_cnt DESC
        LIMIT i_offset, i_limit;

      SELECT COUNT(*) as cnt
      FROM recipe;

    ELSE
        -- 4. recipe 검색어 & 좋아요순 정렬 조회
        SET @v_sql = CONCAT("
        SELECT M.*
        FROM(
            SELECT R.`recipe_name`
                 , R.`img`
                 , R.`price`
                 , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
                 , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = R.`recipe_id`) as `like_cnt`
            FROM recipe AS R
        ) M
        WHERE M.recipe_name LIKE '%",i_search_keyword,"%'
           OR M.tag='",i_search_keyword,"'
        ORDER BY M.like_cnt DESC
        LIMIT ",i_offset,",",i_limit,";
        ");

      PREPARE stmt FROM @v_sql;
      EXECUTE stmt;
      DEALLOCATE PREPARE stmt;

      SET @v_sql = CONCAT("
        SELECT COUNT(*) as cnt
        FROM(
            SELECT R.`recipe_id`
                 , R.`recipe_name`
                 , R.`price`
                 , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=R.`recipe_id`),'') as `tag`
            FROM recipe AS R
        ) M
        WHERE M.recipe_name LIKE '%",i_search_keyword,"%'
           OR M.tag='",i_search_keyword,"';
        ");

      PREPARE stmt FROM @v_sql;
      EXECUTE stmt;
      DEALLOCATE PREPARE stmt;

    END IF;

END