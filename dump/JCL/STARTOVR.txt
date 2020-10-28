//STRTOVER JOB 1,NOTIFY=&SYSUID ,TYPRUN=SCAN
//*****************************************************/
//*                                                   */
//*  DELETE ALL EXISTING COBOL COURSE DATASETS AND    */
//*  GET FRESH COPIES OF ALL OF THEM. USE WITH CARE!  */
//*                                                   */
//*****************************************************/
//*  DELETE ALL EXISTING COBOL COURSE DATASETS        */
//*****************************************************/
// SET ID=&SYSUID
//STEP010 EXEC PGM=IEFBR14
//DD1     DD DSN=&ID..S0W1.ISPF.ISPPROF,DISP=(MOD,DELETE),
//           SPACE=(TRK,0),UNIT=SYSALLDA
//DD2     DD DSN=&ID..JCL,DISP=(MOD,DELETE),
//           SPACE=(TRK,0),UNIT=SYSALLDA
//DD3     DD DSN=&ID..CBL,DISP=(MOD,DELETE),
//           SPACE=(TRK,0),UNIT=SYSALLDA
//DD4     DD DSN=&ID..LOAD,DISP=(MOD,DELETE),
//           SPACE=(TRK,0),UNIT=SYSALLDA
//DD5     DD DSN=&ID..DATA,DISP=(MOD,DELETE),
//           SPACE=(TRK,0),UNIT=SYSALLDA
//*
//*****************************************************/
//*  GET FRESH COPIES OF ALL CBL COURSE DATASETS      */
//*****************************************************/
//STEP020 EXEC PROC=PCOB,ID=&ID
//
