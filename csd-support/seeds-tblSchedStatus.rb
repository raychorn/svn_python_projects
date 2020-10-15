status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '5',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '6',:processpay => 'True',:processbilling => 'False',:officeid => '2',:active => 'False',:hold => 'True',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '7',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '9',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '10',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '11',:processpay => 'True',:processbilling => 'True',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '12',:processpay => 'True',:processbilling => 'True',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '13',:processpay => 'True',:processbilling => 'True',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '15',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '16',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'True',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '18',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '19',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '20',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON CONFIRMATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '22',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '25',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '26',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '27',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#990099',:fgcolor => '#FFFFFF',:statusid => '29',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/CM',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '30',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/GM',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '31',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '68',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'False',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '69',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'False',:hold => 'True',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '70',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '71',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'False',:hold => 'True',:schedstatus => 'UNAVAILABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '72',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '73',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '74',:processpay => 'True',:processbilling => 'True',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '75',:processpay => 'True',:processbilling => 'True',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '76',:processpay => 'True',:processbilling => 'True',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '77',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '78',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '79',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '80',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '81',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '82',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'False',:hold => 'False',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '83',:processpay => 'True',:processbilling => 'True',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFE500',:fgcolor => '#000000',:statusid => '86',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0066',:fgcolor => '#FFFFFF',:statusid => '88',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '89',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '90',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '91',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '92',:processpay => 'True',:processbilling => 'True',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '93',:processpay => 'True',:processbilling => 'True',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '94',:processpay => 'True',:processbilling => 'True',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '95',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'False',:schedstatus => 'ADJ-NO BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '96',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL LESS-PB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '97',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'NS PREBILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '98',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '99',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '100',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '101',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'UNAVAILABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '102',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '103',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '104',:processpay => 'True',:processbilling => 'True',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '105',:processpay => 'True',:processbilling => 'True',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '106',:processpay => 'True',:processbilling => 'True',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '107',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATIONS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '108',:processpay => 'True',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '109',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL-NO CHRG',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '110',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'DECLINED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '111',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'INTERP-NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '112',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '113',:processpay => 'True',:processbilling => 'True',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CUA',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '114',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED W/BUS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '115',:processpay => 'True',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'DOUBLE  BOOKED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '116',:processpay => 'True',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'PAY INTERPRETER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '135',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:fgcolor => '#FFFFFF',:statusid => '136',:processpay => 'True',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '137',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '138',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '139',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '140',:processpay => 'True',:processbilling => 'True',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '141',:processpay => 'True',:processbilling => 'True',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '142',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '143',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => 'CUC',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '144',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '145',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => "INTERP/CX'L",:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '146',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '147',:processpay => 'True',:processbilling => 'True',:officeid => '6',:active => 'True',:hold => 'False',:schedstatus => 'CLIENT NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '148',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '149',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '150',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '151',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'UNAVAILABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '152',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '153',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE/24 H',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '154',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS/24 H',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '155',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '156',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '157',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'OBSERVATIONS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '158',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL-WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '159',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL-NO CHRG',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '160',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'DECLINED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '161',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'INTERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '162',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '163',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL UPON ARIV',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '164',:processpay => 'True',:processbilling => 'True',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS/48 H',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '165',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE/48 H',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '166',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'False',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '171',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '172',:processpay => 'True',:processbilling => 'True',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '173',:processpay => 'True',:processbilling => 'True',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '174',:processpay => 'True',:processbilling => 'True',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '176',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '177',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '179',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '180',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'False',:hold => 'False',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '181',:processpay => 'True',:processbilling => 'True',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '182',:processpay => 'True',:processbilling => 'True',:officeid => '5',:active => 'False',:hold => 'False',:schedstatus => 'CANCEL LESS/48 HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '183',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'False',:hold => 'False',:schedstatus => 'CANCEL MORE/48 HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '184',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '185',:processpay => 'True',:processbilling => 'True',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '186',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '187',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'UNAVAILABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '188',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '189',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE/24HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '190',:processpay => 'True',:processbilling => 'True',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS/24 HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '191',:processpay => 'True',:processbilling => 'True',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '192',:processpay => 'True',:processbilling => 'True',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '193',:processpay => 'True',:processbilling => 'True',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'OBSERVATIONS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '194',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL- WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '195',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL-NO CHRG',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '196',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'DECLINED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '197',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'INTERP-NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '198',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '199',:processpay => 'True',:processbilling => 'True',:officeid => '7',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL UPON ARRIVAL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '200',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '201',:processpay => 'False',:processbilling => 'False',:officeid => '7',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '206',:processpay => 'True',:processbilling => 'True',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '207',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '208',:processpay => 'True',:processbilling => 'True',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '209',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '210',:processpay => 'False',:processbilling => 'True',:officeid => '8',:active => 'False',:hold => 'False',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '211',:processpay => 'True',:processbilling => 'True',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '212',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '213',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'False',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '214',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'False',:hold => 'True',:schedstatus => 'UNAVAILABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '215',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '217',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '218',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'ERROR',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#809FFF',:fgcolor => '#000000',:statusid => '219',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/NM',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#FF8000',:fgcolor => '#000000',:statusid => '220',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/SM',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '222',:processpay => 'True',:processbilling => 'True',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'AWAITING INVOICE',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '223',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'CLOSED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '224',:processpay => 'False',:processbilling => 'False',:officeid => '13',:active => 'True',:hold => 'True',:schedstatus => 'DUPLICATE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '225',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'INTRP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '226',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'False',:hold => 'False',:schedstatus => 'CSD NO/SO DAK',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:fgcolor => '#FFFFFF',:statusid => '227',:processpay => 'False',:processbilling => 'False',:officeid => '6',:active => 'True',:hold => 'True',:schedstatus => 'INTERP LATE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '228',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '229',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'False',:statusid => '240',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'False',:schedstatus => 'GAVE BACK',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '241',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'VOLUNTEER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '243',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'SERVICE',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'True',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '244',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'CREDIT',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '245',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '246',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'UNAVAILABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '247',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '248',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE/24HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '249',:processpay => 'True',:processbilling => 'True',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS/24 HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '250',:processpay => 'True',:processbilling => 'True',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '251',:processpay => 'True',:processbilling => 'True',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '252',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATIONS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '253',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL- WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '254',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL-NO CHRG',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '255',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'DECLINED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '256',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'INTERP-NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '257',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'NO SERVICE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '258',:processpay => 'True',:processbilling => 'True',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL UPON ARRIVAL',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '259',:processpay => 'True',:processbilling => 'True',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS/48 HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '260',:processpay => 'False',:processbilling => 'False',:officeid => '15',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE/48 HRS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '263',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'False',:statusid => '264',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'False',:hold => 'False',:schedstatus => 'TEST',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '265',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'COMPLETED NB',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'False',:statusid => '266',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'PTO',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '267',:processpay => 'False',:processbilling => 'True',:officeid => '9',:active => 'False',:hold => 'False',:schedstatus => 'CANCELLED 48',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'OTHER',:credit => 'False',:statusid => '268',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'E-TIME',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '269',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'SAME DAY PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '270',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'SAME DAY ACCEPT',:interpOption => 'False',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '271',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'SAME DAY',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#9966FF',:fgcolor => '#FFFFFF',:statusid => '272',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'VRS CONFIRMED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '273',:processpay => 'True',:processbilling => 'False',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => 'NO SHOW NB',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:statusid => '275',:processpay => 'True',:processbilling => 'True',:officeid => '9',:active => 'False',:hold => 'True',:schedstatus => '< COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '276',:processpay => 'True',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '277',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '279',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '281',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '282',:processpay => 'True',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '283',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '284',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '285',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL LESS-PB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '286',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '287',:processpay => 'False',:processbilling => 'False',:officeid => '10',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL PRE-BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '288',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '289',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:statusid => '290',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '291',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '292',:processpay => 'True',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '293',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '294',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '296',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '297',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON CONFIRMATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '298',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL LESS-PB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '299',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '300',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS-PB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '301',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '302',:processpay => 'True',:processbilling => 'True',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '303',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON CONFIRMATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '304',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:statusid => '305',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '306',:processpay => 'True',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '307',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '308',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '309',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '310',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '311',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#6600CC',:fgcolor => '#FFFFFF',:statusid => '312',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/RC',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#993300',:fgcolor => '#FFFFFF',:statusid => '313',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/AB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '314',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL LESS-PB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:statusid => '315',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '316',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '317',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '318',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON CONFIRMATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:statusid => '319',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '320',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '321',:processpay => 'True',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '322',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '323',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '325',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '326',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/GM',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '327',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '329',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '332',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '333',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'SAME DAY',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '336',:processpay => 'True',:processbilling => 'True',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '337',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '338',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '339',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '340',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'SAME DAY',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '341',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '342',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '343',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'SAME DAY',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '344',:processpay => 'True',:processbilling => 'True',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '345',:processpay => 'True',:processbilling => 'True',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '346',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'True',:isdefault => 'True')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '347',:processpay => 'True',:processbilling => 'True',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '348',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '349',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '350',:processpay => 'True',:processbilling => 'True',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL/ARRIVAL',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '351',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '352',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '353',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:statusid => '354',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '356',:processpay => 'True',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '357',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '358',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '359',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '360',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '361',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '362',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '363',:processpay => 'False',:processbilling => 'False',:officeid => '4',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '364',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '365',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '366',:processpay => 'False',:processbilling => 'False',:officeid => '8',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '367',:processpay => 'False',:processbilling => 'False',:officeid => '2',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '368',:processpay => 'False',:processbilling => 'False',:officeid => '9',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '369',:processpay => 'False',:processbilling => 'False',:officeid => '5',:active => 'True',:hold => 'True',:schedstatus => 'VOLUNTEER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '370',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '371',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '372',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '373',:processpay => 'True',:processbilling => 'True',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '374',:processpay => 'True',:processbilling => 'True',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '375',:processpay => 'True',:processbilling => 'True',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '376',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '377',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '378',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '379',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '380',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '381',:processpay => 'True',:processbilling => 'True',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '382',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '383',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '384',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '385',:processpay => 'True',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '386',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '387',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '388',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL PRE-BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#6600CC',:fgcolor => '#FFFFFF',:statusid => '389',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/RC',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#993300',:fgcolor => '#FFFFFF',:statusid => '390',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/AB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '391',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '392',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '393',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'SAME DAY',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '394',:processpay => 'False',:processbilling => 'False',:officeid => '18',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '395',:processpay => 'True',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL CSD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '396',:processpay => 'True',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL LSS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#CC0000',:fgcolor => '#FFFFFF',:statusid => '397',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'PENDING',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:bgcolor => '#008F00',:fgcolor => '#FFFFFF',:statusid => '398',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'CONFIRMED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '399',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL MORE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '400',:processpay => 'True',:processbilling => 'True',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL LESS',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '401',:processpay => 'True',:processbilling => 'True',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'NO SHOW',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '402',:processpay => 'True',:processbilling => 'True',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'COMPLETED',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'COMPLETED',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '403',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'OBSERVATION',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '404',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL WEATHER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '405',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'CANCEL NO CHARGE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '406',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:bgcolor => '#663300',:fgcolor => '#FFFFFF',:statusid => '407',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'TERP NO SHOW',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:bgcolor => '#000099',:fgcolor => '#FFFFFF',:statusid => '408',:processpay => 'True',:processbilling => 'True',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'CANCELED UPON ARRIVAL',:interpOption => 'True',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#FFCC00',:fgcolor => '#000000',:statusid => '409',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '410',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'FILLED',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '411',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'TERP CANCEL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_BILL',:credit => 'False',:statusid => '412',:processpay => 'True',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'TERP BILL',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '413',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'AGENCY HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '414',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'TERP HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '415',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'CANCEL LESS-PB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#6600CC',:fgcolor => '#FFFFFF',:statusid => '416',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/RC',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:bgcolor => '#993300',:fgcolor => '#FFFFFF',:statusid => '417',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'UNFILLED/AB',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'UNFILLED',:credit => 'False',:statusid => '418',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'UNABLE/ER',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'CANCEL_NC',:credit => 'False',:statusid => '419',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'False',:schedstatus => 'DELETE',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:schedgroup => 'PENDING',:credit => 'False',:statusid => '420',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'SAME DAY',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '421',:processpay => 'False',:processbilling => 'False',:officeid => '17',:active => 'True',:hold => 'True',:schedstatus => 'BILLING HOLD',:interpOption => 'False',:isdefault => 'False')
status.save

status = Tblschedstatus.new(:credit => 'False',:statusid => '422',:processpay => 'False',:processbilling => 'False',:officeid => '16',:active => 'True',:hold => 'True',:schedstatus => '90 DAYS CLOSED',:interpOption => 'False',:isdefault => 'False')
status.save

puts "DB DATA IMPORT SUCCESSFUL for tblSchedStatus"
