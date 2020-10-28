/* REXX */
trace n
x = msg(off)
address ISREDIT
/*

   This edit macro inserts copybook text into COBOL source code.
   It can also reverse the process using UNDO as the first parameter.
   For more information, type GETCOPY HELP and press enter.

   Search copy libraries in the order given below:

*/

copypds.1 = 'SDG.TEST.L.COPYLIB'    /* SAVE puts changed copybooks */
copypds.2 = 'SDG.PROD.L.COPYLIB'
copypds.3 = 'PRS.PROD.L.COPYLIB'
copypds.4 = 'COPYPDS'
/* Up to 16 named pds libraries are supported. Be sure the last */
/* copypds definition (copypds.17) has literal, "COPYPDS".      */

"MACRO (copybook) PROCESS"
/*

                               MAIN PROGRAM

*/
call edit_parm
call initialize
select
 when copybook = 'ALL'  then    /*  bring in all copybooks          */
    call expand_all_copybooks
 when copybook = 'UNDO' then    /*  go back to copybook statements  */
    call undo_all_copybooks
 when copybook = 'SAVE' then    /*  save changed copybooks and UNDO */
    call save_changed_copybooks
 otherwise                      /*  bring in one copybook           */
    call expand_one_copybook
end
call wrap_up
exit(1)
/*

                             SUBROUTINE AREA

*/
initialize:

    upper copybook

    "(ustate) = USER_STATE"
    "(number1, number2) = NUMBER"
    if number1 = 'ON'  then
        "UNNUM"
    "CAPS OFF"
    ddname = 'COBCOPY'
    saverow = 0
    '(insrow,inslst) = DISPLAY_LINES'

    lit_begin_copybook = '*@#$ --------------- BEGIN COPYBOOK '
    lit_end_copybook   = '*@#$ ---------------   END COPYBOOK '
    lit_delim_copybook = '---------------- *@#$'

return


expand_one_copybook:

    call find_copybook_in_code
    call allocate_copylib
    call build_header_and_trailer
    call insert_copybook_in_code
    ZEDSMSG = copybook" expanded"

return


expand_all_copybooks:

    cpyctr = 0
    call next_copybook_in_code
    do while seekcnt > 0
        cpyctr = cpyctr + 1
        call allocate_copylib
        call build_header_and_trailer
        call insert_copybook_in_code
        call next_copybook_in_code
    end
    if cpyctr > 0  then
        ZEDSMSG = cpyctr" copybooks expanded"
    else
        do
        ZEDLMSG = "Error - Cannot find any COPY statement"
        call wrap_up
        exit(12)
        end

return


undo_all_copybooks:

    delctr = 0
    "SEEK '"lit_begin_copybook"' FIRST 7"
    seekrc = rc
    do while seekrc = 0
        delctr = delctr + 1

        "(delrow1,delcol1) = CURSOR"
        "(cmtline) = LINE "delrow1
        copybook = word(substr(cmtline,43,8),1)

        cpylineno = delrow1 - 1
        "(cpyline) = LINE "cpylineno
        copylin2 = overlay(' ', cpyline, 7)
        'LINE 'cpylineno' = "'copylin2'"'

        trailer_arg = lit_end_copybook || copybook
        "SEEK '"trailer_arg"' FIRST 7"
        if rc = 0  then
            do
            "(delrow2,delcol2) = CURSOR"
            "DELETE "delrow1 delrow2
            "SEEK '"lit_begin_copybook"' FIRST 7"
            end
       else
            do
            ZEDLMSG = "Error - Cannot find delimiter for "copybook
            call wrap_up
            exit(12)
            end
       seekrc = rc
    end

    if delctr > 0  then
        ZEDSMSG = delctr" copybooks undone"
    else
        ZEDLMSG = "Error - no copybooks found to undo"

return


save_changed_copybooks:
    savctr = 0
    delctr = 0
    nest   = 0
    call copybook_nest('.ZFIRST .ZLAST')
    if delctr > 0  then
        ZEDSMSG = delctr" undone/ "savctr" saved"
    else
        ZEDLMSG = "Error - no copybooks found"

return

copybook_nest:procedure expose savctr delctr copypds. ustate ddname,
                        number1 number2 saverow nest,
          lit_begin_copybook lit_end_copybook lit_delim_copybook
/*
    This procedure is recursive.  Its purpose is to look for changes
    in copybooks, which may be nested, within a range of lines.  The
    incoming arguments are two labels; the first represents the start
    of the search range, the second the end of the search range.
    Copybooks are searched for only in this range.  Initially, the
    labels are .ZFIRST and .ZLAST .  Each copybook found is in turn
    searched for nested copybooks, by recursively calling this
    prodedure from itself.
*/
    nest = nest + 1
    arg caller_lbls
    alpha    = substr('ABCDEFGHIJKLMNOPQRSTUVWXYZ',nest,1)
    strtlbl  = '.AA'alpha       /* Labels to define copybook text */
    endlbl   = '.BB'alpha
    lbls     = strtlbl' 'endlbl
    del_lbl1 = '.DAA'alpha      /* Labels to delete embedded text */
    del_lbl2 = '.DBB'alpha
    del_lbls = del_lbl1' 'del_lbl2
/*
    Search for first copybook header in range
*/
    "SEEK '"lit_begin_copybook"' 7 FIRST "caller_lbls
    seekrc = rc
    do while seekrc = 0
/*
        Search for additional copybook headers in range

        Extract name of copybook from header
*/
        "(savrow1,savcol1) = CURSOR"
        "(cmtline) = LINE "savrow1
        copybook = word(substr(cmtline,43,8),1)
/*
        Uncomment the original COPY statement
*/
        cpylineno = savrow1 - 1
        "(cpyline) = LINE "cpylineno
        copylin2 = overlay(' ', cpyline, 7)
        'LINE 'cpylineno' = "'copylin2'"'
/*
        Look for the trailer of the current expanded copybook
*/
        trailer_arg = lit_end_copybook || copybook
        "SEEK '"trailer_arg"' 7 "caller_lbls
        if rc > 0  then
            do
            ZEDLMSG = "Error - Cannot find delimiter for "copybook
            call wrap_up
            exit(12)
            end
/*
        Set labels for the range which include the header/trailer
        and range for copybook text.
*/
        savrow11 = savrow1 + 1
        "LABEL (savrow11) = "strtlbl" 1"
        "LABEL (savrow1) = "del_lbl1" 1"
        "(savrow2,savcol2) = CURSOR"
        savrow21 = savrow2 - 1
        "LABEL (savrow21) = "endlbl" 1"
        "LABEL (savrow2) = "del_lbl2" 1"
/*
        Recursively call this procedure to check for nested copybooks
        in this range.  The lbls argument defines the boundaries of
        the search, and becomes the next range.
*/
        call copybook_nest(lbls)
/*
        Compare the copybook in the source code with the version in
        the copylib.  If the versions are different, save the source
        code version in the first library (copypds.1).
*/
        call source_copybook
        call pds_copybook
        if compare_copybook()  then
            call save_copybook
        address TSO
        "FREE  DSN("pds")"
        address ISREDIT
/*
        Delete the copybook text, leaving only the original uncomment
        COPY statement.
*/
        "DELETE "del_lbls
        delctr = delctr + 1
/*
        Sometimes when deleting the text for a nested copybook, the
        label that defines the end of the container copybook is lost.
        This only can happen at the end of a container copybook; so,
        if the end label is missing, it is considered the end of
        copybooks in this range.  Set the return code (seekrc) to
        exit loop.

        Most of the time, the end label is there.  In this case, search
        for the next copybook header.  If not there, set the return
        code (seekrc) to exit the loop.
*/
        "(lblline) = LINENUM "word(caller_lbls,2)
        if rc = 0  then
            "SEEK '"lit_begin_copybook"' FIRST "caller_lbls
       seekrc = rc
    end

    nest = nest - 1
return


source_copybook:

    drop source_copybook.
    "(strtrow) = LINENUM "strtlbl
    "(endrow)  = LINENUM "endlbl
    if rc = 8  then
        do
        "(endrow1) = LINENUM "del_lbl2
        endrow = endrow1 - 1
        end
    do i = strtrow to endrow

         j = i - strtrow + 1
         "(wline) = LINE "i
         source_copybook.j = wline

    end
    source_copybook.0 = endrow - strtrow + 1

return


pds_copybook:

    drop pds_copybook.
    call allocate_copylib
    address TSO
    "execio * diskr COBCOPY ( stem pds_copybook. finis"
    address ISREDIT

return


compare_copybook:

    if source_copybook.0 ^= pds_copybook.0  then return (1)

    do i = 1 to pds_copybook.0

        if substr(source_copybook.i,7,66) ,
        ^= substr(pds_copybook.i,7,66)  then
            return(1)

    end

return(0)

save_copybook:

    address TSO
    pds = "'"copypds.1"("copybook")'"
    "FREE  DSN("pds")"
    "ALLOC DSN("pds") DDNAME(COBSAVE) SHR REUSE"
    if rc = 12 then
        do
        address ISREDIT
        ZEDLMSG = "Error - Failed to allocate copylib for save"
        call wrap_up
        exit(12)
        end

    "execio * diskw COBSAVE ( stem source_copybook. finis"
    savctr = savctr + 1
/*
    If macro GETCOPY2 is found in the CLIST lib, do a background
    edit session to set STATS ON and NUM ON COB STD for changed
    copylib member.
*/
    trace r
    if sysdsn("CLIST(GETCOPY2)") = 'OK'  then
        do
        address ISPEXEC
        "EDIT DATASET("pds") MACRO(GETCOPY2)"
        address ISREDIT
        end
    address ISREDIT
    trace n

return


edit_parm:

    upper copybook
    select
     when copybook = 'HELP'  then
        call help
     when copybook = '?'  then
        call help
     when copybook = ''  then
        do
       ZEDLMSG = "Error - Copybook name is required as first parameter"
        call wrap_up
        exit(12)
        end
     otherwise
        nop
    end

return


find_copybook_in_code:

    "EXCLUDE ' COPY ' 7 72 ALL"
    "FIND '*' 7 ALL"
    "SEEK ' COPY ' 7 72 ALL X"
    "(,seekcnt) = SEEK_COUNTS"
    if seekcnt > 0  then
        do
        "FIND '"copybook"' FIRST WORD 13 72 X"
        if rc > 0  then
            do
       ZEDLMSG = "Error - Cannot find reference to copybook "copybook
            call wrap_up
            exit(12)
            end
        end
    else
        do
        ZEDLMSG = "Error - Cannot find any COPY statement"
        call wrap_up
        exit(12)
        end
    "(insrow,inscol) = CURSOR"
    saverow = insrow

return


next_copybook_in_code:

    "EXCLUDE ' COPY ' 7 72 ALL"
    "FIND '*' 7 ALL"
    "SEEK ' COPY ' 7 72 ALL X"
    "(,seekcnt) = SEEK_COUNTS"
    if seekcnt > 0  then
        do
        "(insrow,inscol) = CURSOR"
        "(cpyline) = LINE "insrow
        cpyline = '      'substr(cpyline, 7)
        cpyline_t1 = substr(cpyline, inscol + 1)
        parse var cpyline_t1    word_copy copybook dontcare
        copybook = strip(copybook,'T','.')
        end
    if saverow = 0 then
        saverow = insrow

return


allocate_copylib:

    do i = 1 to 17
        if i > 16 | substr(copypds.i, 1, 7) = 'COPYPDS' then
            do
            ZEDLMSG = "Error - Cannot find "copybook" in any PDS"
            call wrap_up
            exit(12)
            end
        pds = "'"copypds.i"("copybook")'"
        resp = sysdsn(pds)
        if resp = 'OK'  then
            leave
    end

    address TSO
    "FREE  DSN("pds")"
    "ALLOC DSN("pds") DDNAME("ddname") SHR REUSE"
    address ISREDIT
    if rc = 12 then
        do
        ZEDLMSG = "Error - Failed to allocate copylib"
        call wrap_up
        exit(12)
        end

return


build_header_and_trailer:

    copyname = substr(copybook,1)
    header  = '     ' lit_begin_copybook || copyname lit_delim_copybook
    trailer = '     ' lit_end_copybook   || copyname lit_delim_copybook

return


insert_copybook_in_code:

    "(copyline) = LINE "insrow
    copylin2 = overlay('*', copyline, 7)
    'LINE (insrow) = "'copylin2'"'
    'LINE_AFTER 'insrow' = (header)'
    insrow = insrow + 1
    address TSO
    delstack
    "execio * diskr COBCOPY ( finis"
    n = queued()
    address ISREDIT
    do i = 1 to n
        pull copyrec
       'LINE_AFTER 'insrow' = (copyrec)'
        insrow = insrow + 1
    end
    address TSO
    delstack
    address ISREDIT
    'LINE_AFTER 'insrow' = (trailer)'

return


wrap_up:

    if saverow = 0 then
        saverow = 1
    "USER_STATE = (ustate)"
    "NUMBER = (number1, number2)"
    "RESET EXCLUDED"
    address ISPEXEC
    "SETMSG MSG(ISRZ001)"
    address ISREDIT

return


help:

    say " "
    say "GETCOPY - This edit macro replaces COPY cobol statements with"
    say "          the actual copybook text.  It also can UNDO the"
    say "          latter if none of the embedded comment lines are"
    say "          disturbed.  Set-up the library names at the"
    say "          beginning of the macro before using."
    say " "
    say "          If a copybook in the COBOL program is changed,"
    say "          it can be saved using the SAVE option.  The copybook"
    say "          is saved in the first library."
    say " "
    say "          Nested copybooks are fully supported, including the"
    say "          save function."
    say " "
    say "format:"
    say " "
    say "Command ===> GETCOPY copybook-name"
    say "The above replaces one copybook named in the parameter"
    say " "
    say "Command ===> GETCOPY ALL"
    say "The above replaces all copybooks, included nested ones"
    say " "
    say "Command ===> GETCOPY UNDO"
    say "Deletes copybook text and restores copy statement"
    say " "
    say "Command ===> GETCOPY SAVE"
    say "Saves program's changed version of copybook in first"
    say "copylib defined to macro.  Deletes copybook text"
    say "and restores copy statement."
    say " "
    say "Press enter to continue"
    exit
