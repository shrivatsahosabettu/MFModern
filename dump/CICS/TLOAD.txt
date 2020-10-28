/* REXX - ZOS.PUBLIC.ADHOC.CLIST(TCLIST) */
/* Before modifying, please see comments in ZOS.PUBLIC.ADHOC.CLIST(PJCL) */
parse upper arg MEM .
"EXEC 'ZOS.PUBLIC.ADHOC.CLIST(PJCL)'" "'"MEM"("SYSVAR(SYSICMD)"'"
EXIT
