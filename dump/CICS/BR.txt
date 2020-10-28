/* ZOS.PUBLIC.ADHOC.CLIST(ED) - REXX EXEC                             */
/* Browses the dataset the cursor is sitting on (point and shoot).    */
arg DSN
if DSN = '' then do    /* If true, user did not prefix with "TSO".    */
   ADDRESS 'ISREDIT'   /* Capture an argument if entered without      */
  'MACRO (DSN)'        /* the "TSO" prefix.                           */
   RCODE = rc          /* Capture rc - Are we executing as an         */
end                    /* Edit Macro? "0" = Yes.                      */
EXEC_NAME = SYSVAR(SYSICMD)
if DSN   = '' & ,      /* If DSN is still blank, and we are           */
   RCODE = 0  then do  /* executing as an Edit Macro, see if cursor   */
                       /* is pointing to a DSName on the screen       */
  '(LINENBR,COL) = CURSOR'
  '(LINEPTR) = LINENUM .ZCSR'
  '(LINEIN) = LINE' LINEPTR
  if COL = 0 then nop        /* If cursor is not on an edit line,   */
  else do                    /* don't continue.                     */
     TEMP = index(LINEIN,'DSN=')
     if TEMP > 0 then COL = TEMP + 4
     else do
        TEMP = index(LINEIN,'.')
        if TEMP > 0 then do
           COL = max(COL,TEMP)
        end
     end
     do i = 1 to 54
        COL2 = COL - i
        if COL2 < 1 then do
           COL2 = 0
           leave
        end
        TEMP = substr(LINEIN,COL2,1)
        if TEMP < 'a' then do
           if TEMP = ')' ,
            | TEMP = '(' ,
            | TEMP = '.' then nop
           else leave
        end
     end
     DSN = substr(LINEIN,COL2+1,54)
     TEMP = index(LINEIN,'ORDER=(')
     if TEMP > 0 then DSN = word(translate(DSN,,"()"),1)
   end
end
else RCODE = 99
DSN = word(translate(DSN,'',',"'||"'"),1)
if DSN <> '' then do
   PDS = word(translate(DSN," ","("),1)
   x = msg(off)
   if SYSDSN(DSN)  = 'OK' ,
    | SYSDSN(PDS)  = 'OK' then do
      if left(DSN,1) <> "'" then do
         DSN = SYSVAR(SYSPREF)"."DSN
         PDS = SYSVAR(SYSPREF)"."PDS
      end
   end
   x = msg(on)
   ADDRESS 'ISPEXEC'
   if EXEC_NAME = 'ED' & ,
      SYSDSN("'"PDS"'") = 'OK' then do
     "EDIT DATASET('"DSN"')"
   end
   else do
      if EXEC_NAME = 'BR' & ,
         SYSDSN("'"DSN"'") = 'OK' then do
        "BROWSE DATASET('"DSN"')"
      end
      else do
         ZEDSMSG = 'DSN/MBR not found'
         ZEDLMSG = 'Dataset' DSN 'and/or member was not found.'
        'SETMSG MSG(ISRZ001)'
      end
   end
   if RCODE = 0 then do
      ADDRESS 'ISREDIT'
     'CURSOR =' LINENBR
   end
end
exit
