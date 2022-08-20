CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_select`(
     IN i_recipe_id     VARCHAR(40)     -- 레시피ID
    ,IN i_customer_uuid VARCHAR(40)     -- 유저ID
    ,OUT `o_out_code`   SMALLINT
)
BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 상세 메뉴 조회
author : dylee
RELEASE : 0.0.3
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

    -- 1. USER 성인 검증

    -- 2. recipe 조회
    SELECT R.`recipe_name`
         , R.`description`
         , R.`img`
         , R.`price`
         , R.`measure_standard`
         , R.`tip`
         , R.`diff_score`
         , R.`price_score`
         , R.`sweet_score`
         , R.`alcohol_score`
         , IFNULL((SELECT GROUP_CONCAT(tag) FROM recipe_tag WHERE recipe_id=i_recipe_id),'') as `tag`
         , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = i_recipe_id) as `like_cnt`
    FROM recipe AS R
    WHERE R.recipe_id = i_recipe_id;

    -- 3. 음료 조회
    SELECT D.drink_id
         , D.drink_name
         , D.img
    FROM (
        SELECT drink_id
        FROM recipe_main_meterial
        WHERE recipe_id=i_recipe_id
    ) M
    LEFT JOIN drink AS D ON D.drink_id=M.drink_id;

    -- 4. 부재료 조회
    SELECT M.meterial_id
         , M.meterial_name
         , M.img
    FROM (
        SELECT meterial_id
        FROM recipe_sub_meterial
        WHERE recipe_id=i_recipe_id
    ) S
    LEFT JOIN recipe_meterial AS M ON M.meterial_id=S.meterial_id;

END