CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_select` (
     IN i_recipe_id     VARCHAR(40)     -- 레시피ID
    ,IN i_customer_uuid VARCHAR(40)     -- 유저ID
    ,OUT `o_out_code`   SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 상세 메뉴 조회
author : dylee
RELEASE : 0.0.2         main_material의 measuer 컬럼 삭제로, 서브쿼리로 한 번에 구현하도록 변경
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

    -- 1. USER 성인 검증

    -- 2. recipe 조회
    SELECT R.`recipe_name`
         , R.`description`
         , R.`img`
         , R.`price`
         , R.`mesure_standard`
         , R.`tip`
         , R.`diff_score`
         , R.`price_score`
         , R.`sweet_score`
         , R.`alcohol_score`
         , (SELECT GROUP_CONCAT(drink_name) FROM recipe_main_meterial WHERE recipe_id=i_recipe_id) as `main_meterial`
         , (SELECT GROUP_CONCAT(meterial_name) FROM recipe_sub_meterial WHERE recipe_id=i_recipe_id) as `sub_meterial`
         , (SELECT COUNT(*) FROM recipe_like WHERE recipe_id = i_recipe_id) as `like_cnt`
    FROM recipe AS R
    LEFT JOIN recipe_tag AS RT
        ON RT.recipe_id=R.recipe_id
    WHERE R.recipe_id = i_recipe_id;

END