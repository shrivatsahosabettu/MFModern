/* REXX */
trace r
do forever
   PARSE upper external INPUT1
   if INPUT1 = 'END' then leave
   interpret INPUT1
end
