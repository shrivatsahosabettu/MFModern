/* XCPY REXX EXEC - EXPDIR and XCPYT are aliases of this EXEC */
parse arg NEWDS BASEDS .
/* trace r */
/*                                                        */
/* SOUND VARADAN COPY TO A NEW DSN ON THE 3.4 LIST SCREEN */
/* ENTER XCPY AND OVERWRITE DSN-NAME WITH NEW DSN NAME    */
/* CONTROL CONLIST SYMLIST                                */
/* 03/26/2012 - Rewritten in REXX by Scott Cosel          */
/* 03/26/2012 - Added PDS library support                 */
/* 03/31/2012 - Added PDS library EXPDIR support          */
/* 10/02/2015 - Created XCPYT to force UNIT=TEST          */
/*                                                        */
EXEC_NAME = SYSVAR(SYSICMD) ; TRUE = 1 ; FALSE = 0
if EXEC_NAME = 'EXPDIR' then EXPDIR = TRUE
                        else EXPDIR = FALSE
if EXPDIR then do
   say 'Expand directory space of' BASEDS
   NEWDS = ''
end
else say 'Copy from' BASEDS 'to' NEWDS
if SYSDSN(BASEDS) = OK then do
   if SYSDSN(NEWDS) = OK then do
      say 'New dataset already exists.'
      say 'Please choose a different name for the new dataset.'
      RCODE = 8
   end
   else do                          /* IF THE BASE DATA SET EXISTS */
      call ALC BASEDS NEWDS         /* CALL SUBPROCEDURE ALC       */
   end
end
else do
   say 'Dataset' BASEDS 'not found.'
   RCODE = 8
end
exit RCODE

/**********************************************************************/
/* PROCEDURE: ALC - ALLOCATES NEW DSN FROM OLD DSN'S ATTRRIB          */
/**********************************************************************/
ALC:                         /* SUBPROCEDURE ALC TO ALLOCATE AND COPY */
/*   call outtrap 'trap.'
    'LISTD' BASEDS
     call outtrap 'off'
     parse var trap.3 . . . DSNTYPE .  */
     x = LISTDSI(BASEDS 'DIR')
     if SYSDSORG = 'PO' then do
        FROMMEM = 'FROMMEM(*)' ; DIR = ''
        if EXPDIR then do
           say 'from' SYSADIRBLK 'to' SYSADIRBLK + 1 'directory blocks'
           DIR = 'DIR('SYSADIRBLK + 1')'
           temp = substr(BASEDS,1,length(BASEDS)-1)
           temp = strip(left(temp,36))
           if right(temp,1) = '.' then temp = left(BASEDS,36-1)
           NEWDS = temp".T"right(random(1,100000),6,"0")"'"
           X = MSG('OFF')
           RENAME BASEDS NEWDS
           RCODE = rc
           X = MSG('ON')
           if RCODE = 0 then RENAME NEWDS BASEDS
           else do
              say BASEDS 'already in use. Free dataset and try later.'
              RCODE = 8
              return
           end
        end
     end
     else do
        if EXPDIR then do
           say 'Dataset is not partitioned. Exiting...'
           RCODE = 8
           return
        end
        FROMMEM = '' ; DIR = ''
     end
     BLK = 'BLKSIZE('SYSBLKSIZE')'
     UNT = ''
     if EXEC_NAME = 'XCPYT' then UNT = 'UNIT(TEST)'
    'ALLOCATE F(OUTDSN) DA('NEWDS') NEW LIKE('BASEDS')' DIR BLK UNT
    'ISPEXEC  LMINIT DATAID(IDSN)  DATASET('BASEDS')'
    'ISPEXEC  LMINIT DATAID(ODSN)  DATASET('NEWDS')'
    'ISPEXEC  LMCOPY FROMID('IDSN')' FROMMEM ,
                    'TODATAID('ODSN')'
     RCODE = rc
     if RCODE > 0 then ,
        say 'Copy failed with return code' RCODE
    'FREE F(OUTDSN)'
/*   FREE F(IDSN)    */
    'ISPEXEC  LMFREE  DATAID('IDSN')'
    'ISPEXEC  LMFREE  DATAID('ODSN')'
     if EXPDIR & RCODE = 0 then do
        X = MSG('OFF')
        DELETE BASEDS
        X = MSG('ON')
        RENAME NEWDS BASEDS
     end
return
