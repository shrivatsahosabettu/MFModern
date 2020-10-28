/* REXX */
arg TOK
TIM = ' '
if TOK = '?' then do
   say 'JULIAN  FORMAT : DATE J90123'
   say 'GREGORIAN  "   : DATE MMDDYY, MM/DD/YY OR MMDDYYYY'
   exit
end
if TOK = '' then do
   TOK = date('USA')
   TIM = time()
end
TOK  = strip(TOK)
DLEN = length(TOK)
NDAY.01=31
NDAY.02=28
NDAY.03=31
NDAY.04=30
NDAY.05=31
NDAY.06=30
NDAY.07=31
NDAY.08=31
NDAY.09=30
NDAY.10=31
NDAY.11=30
NDAY.12=31
if left(TOK,1) = 'J' then call JULIAN
                     else call GREGOR
if YY = 0 then do
   say 'Invalid year' YY
   exit
end
call GET_DATE MM DD YY
WEEK = NUMBER // 7
NDAYS   = abs(NUMBER - COMMON)
NDAYS   = right(NDAYS,3,'0')
JULIE   = SUBSTR(YY,3,2) || '.' || NDAYS
WEEKN.0 = SUN
WEEKN.1 = MON
WEEKN.2 = TUE
WEEKN.3 = WED
WEEKN.4 = THU
WEEKN.5 = FRI
WEEKN.6 = SAT
say MM'/'DD'/'YY '=' JULIE '('WEEKN.WEEK')' TIM
exit
GREGOR:
   select
      when DLEN = 6 then call FORMAT1
      when DLEN = 8 then call FORMAT2
      otherwise          call BADFRMG
   end
   call CHK_LEAP_YEAR
   call CHK_MM_DD
return
JULIAN:
   select
      when DLEN = 6 then call FORMAT3
      when DLEN = 8 then call FORMAT4
      otherwise          call BADFRMJ
   end
   call CHK_LEAP_YEAR
   call CHK_DDD
   IDX  = 01
   JDAY = JD
   do while (JDAY > NDAY.IDX)
      JDAY = JDAY - NDAY.IDX
      IDX  = IDX + 1
      IDX  = RIGHT(IDX,2,'0')
   end
   DD = right(JDAY,2,'0')
   MM = right(IDX,2,'0')
return
FORMAT1:
   MM = substr(TOK,1,2)
   DD = substr(TOK,3,2)
   YY = substr(TOK,5,2)
   call DETERMINE_CC
   YY = CC || YY
return
FORMAT2:
   if substr(TOK,3,1) = '/' then do
      MM = substr(TOK,1,2)
      DD = substr(TOK,4,2)
      YY = substr(TOK,7,2)
      call DETERMINE_CC
      YY = CC || YY
   end
   else do
      MM = substr(TOK,1,2)
      DD = substr(TOK,3,2)
      YY = substr(TOK,5,4)
   end
return
FORMAT3:
      JD = substr(TOK,4,3)
      YY = substr(TOK,2,2)
      call DETERMINE_CC
      YY = CC || YY
return
FORMAT4:
      JD = substr(TOK,6,3)
      YY = substr(TOK,2,4)
return
DETERMINE_CC:
   if YY < '80' then CC = '20'
                else CC = '19'
return
BADFRMG:
      say 'Enter a valid date (MMDDYY OR MM/DD/YY OR MMDDYYYY).'
exit
BADFRMJ:
      say 'Enter a valid julian date (JYYDDD OR JYYYYDDD).'
exit
CHK_LEAP_YEAR:
   if (YY//4) = 0 then
      if (YY//100) = 0 then
         if (YY//400) = 0 then NDAY.02 = 29
                          else NDAY.02 = 28
      else NDAY.02 = 29
   else NDAY.02 = 28
return
CHK_MM_DD:
   if MM < 1 | MM > 12 then do
      say 'Invalid month' MM
      exit
   end
   if DD < 1 | DD > NDAY.MM then do
      say 'Invalid day' DD
      exit
   end
return
CHK_DDD:
   if NDAY.02 = 28 then YR_DDD_LIMIT = 365
                   else YR_DDD_LIMIT = 366
   if JD < 1 | JD > YR_DDD_LIMIT then do
      say 'Invalid julian day' JD
      exit
   end
return
GET_DATE:
   PYEAR = YY - 1
   COMMON = 365 * PYEAR + (PYEAR%4) - (PYEAR%100) + (PYEAR%400)
   PMON = MM - 1
   TOTD = 0
   do while PMON > 0
      PMON = right(PMON,2,'0')
      TOTD = TOTD + NDAY.PMON
      PMON = PMON - 1
   end
   NUMBER = COMMON + TOTD + DD
return
