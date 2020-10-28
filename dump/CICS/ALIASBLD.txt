//Z80027A JOB 1,NOTIFY=&SYSUID
/*JOBPARM ROOM=BIN1
//*********************************************************************
//* RUN THIS JOB TO UPDATE THE ALIAS MEMBERS IN SDG.TEST.L.CLIST      *
//* WHEN THE PJCL MEMBER IS CHANGED.                                  *
//*********************************************************************
//*SET DSN=&SYSUID..CLIST
// SET DSN=ZOS.PUBLIC.ADHOC.CLIST
//STEP010 EXEC PGM=IEBUPDTE,PARM='MOD'
//SYSPRINT  DD SYSOUT=*
//SYSUT1    DD DSN=&DSN,DISP=SHR
//SYSUT2    DD DSN=&DSN,DISP=SHR
//SYSIN     DD *              UP TO 16 ALIASES CAN BE ASSIGNED TO 1 MBR
./          REPRO NAME=PJCL       0
./          ALIAS NAME=PJCLA      1
./          ALIAS NAME=TJCLA      2
./          ALIAS NAME=PJCLT      3
./          ALIAS NAME=TJCLT      4
./          ALIAS NAME=PCOPY      5
./          ALIAS NAME=TCOPY      6
./          ALIAS NAME=PPROC      7
./          ALIAS NAME=TPROC      8
./          REPRO NAME=TCLIST     0
./          ALIAS NAME=PCLIST     1
./          ALIAS NAME=PCLISTA    2
./          ALIAS NAME=PCLISTV    3
./          ALIAS NAME=TCLISTV    4
./          ALIAS NAME=PCBL       5
./          ALIAS NAME=PCBLA      6
./          ALIAS NAME=TCBL       7
./          ALIAS NAME=PDATA      8
./          ALIAS NAME=TDATA      9
./          ALIAS NAME=PLOAD     10
./          ALIAS NAME=TLOAD     11
./          ALIAS NAME=PCOBOL    12
./          ALIAS NAME=TCOBOL    13
./          ALIAS NAME=PPARM     14
./          ALIAS NAME=TPARM     15
./          ALIAS NAME=PDEMO     16
./          REPRO NAME=TJCL       0
./          ALIAS NAME=PSDATA     1
./          ALIAS NAME=TSDATA     2
./          ALIAS NAME=MYJCL      3
./          ALIAS NAME=MYCLIST    4
./          ALIAS NAME=SCOTTJCL   5
./          ALIAS NAME=TDEMO      6
//
//  ANYTHING FOLLOWING THIS LINE IS IGNORED
./          REPRO NAME=TPROC
./          ALIAS NAME=TCNTL
./          ALIAS NAME=TDBD
./          ALIAS NAME=TDCLGEN
./          ALIAS NAME=TDOC
./          ALIAS NAME=TJCL
./          ALIAS NAME=TPARM
./          ALIAS NAME=TPSB
./          ALIAS NAME=TSEG
./          ALIAS NAME=TSRC
./          ALIAS NAME=SJCL
./          REPRO NAME=DPROC
./          ALIAS NAME=DCNTL
./          ALIAS NAME=DDBD
./          ALIAS NAME=DDCLGEN
./          ALIAS NAME=DDOC
./          ALIAS NAME=DJCL
./          ALIAS NAME=DPARM
./          ALIAS NAME=DPSB
./          ALIAS NAME=DSEG
./          ALIAS NAME=DSRC
./          REPRO NAME=PMSAPROC
./          ALIAS NAME=PMSAPARM
./          ALIAS NAME=PAPPJCL
./          ALIAS NAME=PAPSCNTL
./          ALIAS NAME=PAPSJCL
./          ALIAS NAME=PAPSPARM
./          ALIAS NAME=PUSPJCL
./          ALIAS NAME=PUSPPARM
./          ALIAS NAME=PARM
./          ALIAS NAME=PCLOAD
./          ALIAS NAME=IPROC
./          ALIAS NAME=PUSPPROC
./          REPRO NAME=TMSAPROC
./          ALIAS NAME=TMSAPARM
./          ALIAS NAME=TAPPJCL
./          ALIAS NAME=TAPSCNTL
./          ALIAS NAME=TAPSJCL
./          ALIAS NAME=TAPSPARM
./          ALIAS NAME=TUSPJCL
./          ALIAS NAME=TUSPPARM
./          ALIAS NAME=TUSPPROC
./          REPRO NAME=DMSAPROC
./          ALIAS NAME=DMSAPARM
./          ALIAS NAME=DAPPJCL
./          ALIAS NAME=DAPSCNTL
./          ALIAS NAME=DAPSJCL
./          ALIAS NAME=DAPSPARM
./          ALIAS NAME=DUSPJCL
./          ALIAS NAME=DUSPPARM
./          REPRO NAME=SDH
./          ALIAS NAME=SDSFH
./          REPRO NAME=SDI
./          ALIAS NAME=SDSFI
./          REPRO NAME=SDO
./          ALIAS NAME=SDSFO
//
