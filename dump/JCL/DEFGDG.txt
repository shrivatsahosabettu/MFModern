//DEFGDGD1 JOB 2,NOTIFY=&SYSUID
/*JOBPARM ROOM=HOME
//S1   EXEC PGM=IDCAMS
//SYSPRINT  DD SYSOUT=*
//SYSIN     DD DATA,DLM='<>'
  DEFINE GDG(NAME(&SYSUID..S.TEST.GDG)             -
                        LIMIT(3)                   -
                        SCRATCH                    -
                        NOEMPTY)
//
