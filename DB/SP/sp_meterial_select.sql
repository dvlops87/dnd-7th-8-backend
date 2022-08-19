CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_meterial_select` (
     IN `i_meterial_name`     VARCHAR(255)
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_meterial_select : 부재료 데이터 조회
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

    IF (i_meterial_name IS NULL)
    THEN
    
      SELECT meterial_name
      FROM recipe_meterial;

    ELSE

      SET @v_sql = CONCAT("
        SELECT meterial_name
        FROM recipe_meterial
        WHERE meterial_name LIKE '",i_meterial_name,"%';");

      PREPARE stmt FROM @v_sql;
      EXECUTE stmt;
      DEALLOCATE PREPARE stmt;


    END IF;

END