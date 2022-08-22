CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_recipe_tag_set` (
     IN `i_recipe_id`       INTEGER         -- 레시피ID
    ,IN `i_tag`             VARCHAR(50)     -- 태그명
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_recipe_tag_set : 레시피 태그 등록
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-22
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

    INSERT INTO recipe_tag (
         `recipe_id`
        ,`tag`
    ) VALUES (
         `i_recipe_id`
        ,`i_tag`
    );

    COMMIT;

END