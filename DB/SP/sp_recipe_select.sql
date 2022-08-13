CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_select` (
     IN i_recipe_id     VARCHAR(40)     -- 레시피ID
    ,IN i_customer_uuid VARCHAR(40)     -- 유저ID
    ,OUT `o_out_code`   SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_select : 레시피 상세 메뉴 조회
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
         , (SELECT COUNT(*) FROM recipe_like WHERE R.recipe_id = i_recipe_id) as `like_cnt`
    FROM recipe AS R
    LEFT JOIN recipe_tag AS RT
        ON RT.recipe_id=R.recipe_id
    WHERE R.recipe_id = i_recipe_id;

    /* 220807 recipe 메인 재료 조회의 mesure(양)이 레시피 상세 조회 시 필요할 것 같아, 재료 조회, 부재료 조회 SQL을 분리했습니다
    -> 메인 재료에 대한 계량이 필요 없다면 합치겠습니다*/

    -- 3. recipe 메인 재료 조회
    SELECT D.`drink_name`
         , RM.`mesure`
    FROM recipe_main_meterial AS RM
    LEFT JOIN (
        SELECT drink_id
             , drink_name
        FROM drink
    ) D ON R.drink_id = RM.drink_id
    WHERE RM.recipe_id = i_recipe_id;

    -- 4. recipe 부재료 조회
    SELECT M.`meterial_name`
    FROM recipe_sub_meterial AS SM
    LEFT JOIN (
        SELECT meterial_id
             , meterial_name
        FROM recipe_meterial
    ) M ON R.drink_id = RM.drink_id
    WHERE SM.recipe_id = i_recipe_id;


END