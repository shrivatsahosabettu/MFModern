/* ZOS.PUBLIC.ADHOC.CLIST(PJCL) - Original Rexx master member name    */
/* This is a shop wide Clist. Please don't modify for specific appl's */
/* If you are reading this, and you are NOT editing member, PJCL,     */
/* you are most likely editing an alias of PJCL. If you are certain   */
/* that an update to this member is warranted, make changes only to   */
/* PJCL.  Then submit member ALIASBLD to rebuild the alias members.   */
/* trace r */
arg MEM '(' EXEC_NAME
if MEM = '' then do    /* If true, user did not prefix with "TSO".    */
   ADDRESS 'ISREDIT'   /* Capture an argument if entered without      */
  'MACRO (MEM)'        /* the "TSO" prefix.                           */
   RCODE = rc          /* Capture rc - Are we executing as an         */
end                    /* Edit Macro? "0" = Yes.                      */
if EXEC_NAME = '' then ,
   EXEC_NAME = SYSVAR(SYSICMD)
   ENV1      =   left(EXEC_NAME,1)
   REST      = substr(EXEC_NAME,2)
select
   when ENV1 = 'P' then ENV = 'PROD'
   when ENV1 = 'D' then ENV = 'DEVL'
              otherwise ENV = 'TEST'
end
if MEM   = '' & ,      /* If MEM is still blank, and we are         */
   RCODE = 0  then do  /* executing as an Edit Macro, see if cursor */
                       /* is pointing to a mbr name on the screen   */
  '(LINENBR,COL) = CURSOR'
  '(LINEPTR) = LINENUM .ZCSR'
  '(LINEIN) = LINE' LINEPTR
  if COL = 0 then nop        /* If cursor is not on an edit line,   */
  else do                    /* don't continue.                     */
     do i = 1 to 8
        COL2 = COL - i
        if COL2 < 1 then do
           COL2 = 0
           leave
        end
        if substr(LINEIN,COL2,1) < 'a' then leave
     end
     TEMP = substr(LINEIN,COL2+1,8)
     MEM  = word(translate(TEMP,'','(),."'||"'"),1)
   end
end
else RCODE = 99
select
   when EXEC_NAME = 'PCBL'     then DSN = 'ZOS.PUBLIC.CBL'
   when EXEC_NAME = 'PJCL'     then DSN = 'ZOS.PUBLIC.JCL'
   when EXEC_NAME = 'PCBLA'    then DSN = 'ZOS.PUBLIC.ADHOC.CBL'
   when EXEC_NAME = 'PCLIST'   ,
      | EXEC_NAME = 'PCLISTA'  then DSN = 'ZOS.PUBLIC.ADHOC.CLIST'
   when EXEC_NAME = 'PJCLA'    then DSN = 'ZOS.PUBLIC.ADHOC.JCL'
   when EXEC_NAME = 'PDATA'    then DSN = 'ZOS.PUBLIC.DATA'
   when EXEC_NAME = 'PLOAD'    then DSN = 'ZOS.PUBLIC.LOAD'
   when EXEC_NAME = 'PSDATA'   then DSN = 'ZOS.PUBLIC.SEQ.DATA'
   when EXEC_NAME = 'PPROC'    then DSN = 'VENDOR.PROCLIB'
   when EXEC_NAME = 'MYJCL'    then DSN =  userid()'.TEST.JCL'
   when EXEC_NAME = 'MYCLIST'  then DSN =  userid()'.CLIST'
   when EXEC_NAME = 'SCOTTJCL' then DSN = 'Z80027.TEST.JCL'
   when REST      = 'CARD'     then DSN = 'ISD.'ENV'.L.CARDLIB'
   when REST      = 'CBL'      then DSN =  userid()'.CBL'
   WHEN REST      = 'CLIST'    then DSN =  userid()'.CLIST'
   WHEN REST      = 'CLISTV'   then DSN = 'VENDOR.CLIST'
   when REST      = 'CNTL'     then DSN = 'ISD.'ENV'.L.CNTLSTMT'
   when REST      = 'COBOL'    then DSN =  userid()'.TEST.COBOL'
   when REST      = 'COPY'     then DSN =  userid()'.COPYLIB'
   when REST      = 'DATA'     then DSN =  userid()'.DATA'
   when REST      = 'EDW'      then DSN = 'EDW.'ENV'.L.CNTLSTMT'
   when REST      = 'JCL'      then DSN =  userid()'.JCL'
   when REST      = 'JCLT'     then DSN =  userid()'.TEST.JCL'
   when REST      = 'LOAD'     then DSN =  userid()'.LOAD'
   when REST      = 'PARM'     then DSN = 'VENDOR.PARMLIB'
   when REST      = 'PROC'     then DSN =  userid()'.'ENV'.PROCLIB'
   when REST      = 'RUN'      then DSN = 'ISD.'ENV'.L.JCLRUN'
   when REST      = 'SDATA'    then DSN =  userid()'.DATA'
   when REST      = 'SRC'      ,
      | REST      = 'SRCS'     then DSN = 'ISD.'ENV'.L.SRCLIB'
   otherwise                        DSN =  userid()'.JCL'
end
if MEM <> '' then MEMBER = '('MEM')'
             else MEMBER = ''
ADDRESS "ISPEXEC" "EDIT DATASET('"DSN||MEMBER"')"
/*"SELECT PGM(IQIMSL) PARM(V,'"DSN||MEMBER"')"*/
if MEM <> '' & RCODE = 0 then do
   ADDRESS 'ISREDIT'
  'CURSOR =' LINENBR
end
exit
