-- 제출자 파일을 받으면 ORIGIN_DSF로 저장

DELIMITER //

CREATE PROCEDURE InsertOriginDSF
            (IN newOriginFile               LONGTEXT,
             IN newDateTime                 Varchar(45),
             IN newPeriod                   Varchar(45),
             IN newFK_TaskName              Varchar(45),
             IN newFK_idUSER                Int(11),
             IN newFK_idORIGIN_DATA_TYPE    Int(11))

checkexist:BEGIN

    DECLARE varSubmitNum    Int(11);

    -- check if Participation exists
    IF (SELECT Status
    FROM PARTICIPATION
    WHERE FK_TaskName = newFK_TaskName and FK_idUSER = newFK_idUSER) != 'ongoing'
    THEN SELECT 'Participation does not exist'
            AS ParticipationErrorMessage;
            ROLLBACK;
        Leave checkexist;
    END IF;


    SELECT COUNT(*) INTO varSubmitNum
    FROM ORIGIN_DSF
    WHERE FK_TaskName = newFK_TaskName AND FK_idUSER = newFK_idUSER;

    IF (varSubmitNum = 0) THEN
        INSERT INTO ORIGIN_DSF (OriginFile, SubmitNum, DateTime, Period, FK_TaskName, FK_idORIGIN_DATA_TYPE)
        VALUES (newOriginFile, 1, newDateTime, newPeriod, newFK_TaskName, newFK_idORIGIN_DATA_TYPE);
    ELSE
        INSERT INTO ORIGIN_DSF (OriginFile, SubmitNum, DateTime, Period, FK_TaskName, FK_idORIGIN_DATA_TYPE)
        VALUES (newOriginFile, varSubmitNum+1, newDateTime, newPeriod, newFK_TaskName, newFK_idORIGIN_DATA_TYPE);
    END IF;

-- END checkexist
END checkexist
//

DELIMITER ;
