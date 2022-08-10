CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_drink_select` (
     IN i_drink_id      VARCHAR(40)     -- 음료ID
    ,IN i_customer_uuid VARCHAR(40)     -- 유저ID
    ,OUT `o_out_code`   SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_drink_select : 음료 상세 메뉴 조회
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

    -- 2. Drink 조회
    SELECT D.`drink_name`
         , D.`description`
         , D.`calorie`
         , D.`manufacture`
         , D.`price`
         , D.`large_category`
         , D.`medidum_category`
         , D.`small_category`
         , D.`img`
         , D.`alcohol`
         , D.`mesure`
         , D.`caffeine`
         , (SELECT GROUP_CONCAT(allergy) FROM drink_allergy WHERE drink_id=i_drink_id) as `allergy`
         , (SELECT GROUP_CONCAT(tag) FROM drink_tag WHERE drink_id=i_drink_id) as `tag`
         , (SELECT COUNT(*) FROM drink_like WHERE drink_id=i_drink_id) as `like_cnt`
    FROM drink AS D
    WHERE D.drink_id = i_drink_id;

END