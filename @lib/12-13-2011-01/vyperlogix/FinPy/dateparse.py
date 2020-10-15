from pyparsing import *

month1 = Literal("01") | Literal("1")
month2 = Literal("02") | Literal("2")
month3 = Literal("03") | Literal("3")
month4 = Literal("04") | Literal("4")
month5 = Literal("05") | Literal("5")
month6 = Literal("06") | Literal("6")
month7 = Literal("07") | Literal("7")
month8 = Literal("08") | Literal("8")
month9 = Literal("09") | Literal("9")
month10 = Literal("10")
month11 = Literal("11")
month12 = Literal("12")

monthstring1 = Literal("JAN") | Literal("JANUARY")
monthstring2 = Literal("FEB") | Literal("FEBRUARY")
monthstring3 = Literal("MAR") | Literal("MARCH")
monthstring4 = Literal("APR") | Literal("APRIL")
monthstring5 = Literal("MAY") | Literal("MAY")
monthstring6 = Literal("JUN") | Literal("JUNE")
monthstring7 = Literal("JUL") | Literal("JULY")
monthstring8 = Literal("AUG") | Literal("AUGUST")
monthstring9 = Literal("SEP") | Literal("SEPTEMBER")
monthstring10 = Literal("OCT") | Literal("OCTOBER")
monthstring11 = Literal("NOV") | Literal("NOVEMBER")
monthstring12 = Literal("DEC") | Literal("DECEMBER")

day1 = Literal("01") | Literal("1")
day2 = Literal("02") | Literal("2")
day3 = Literal("03") | Literal("3")
day4 = Literal("04") | Literal("4")
day5 = Literal("05") | Literal("5")
day6 = Literal("06") | Literal("6")
day7 = Literal("07") | Literal("7")
day8 = Literal("08") | Literal("8")
day9 = Literal("09") | Literal("9")
day10 = Literal("10")
day11 = Literal("11")
day12 = Literal("12")
day13 = Literal("13")
day14 = Literal("14")
day15 = Literal("15")
day16 = Literal("16")
day17 = Literal("17")
day18 = Literal("18")
day19 = Literal("19")
day20 = Literal("20")
day21 = Literal("21")
day22 = Literal("22")
day23 = Literal("23")
day24 = Literal("24")
day25 = Literal("25")
day26 = Literal("26")
day27 = Literal("27")
day28 = Literal("28")
day29 = Literal("29")
day30 = Literal("30")
day31 = Literal("31")

month = month10|month11|month12|month1|month2|month3|month4|month5|month6|month7|month8|month9

monthstring = monthstring10|monthstring11|monthstring12|monthstring1|monthstring2|monthstring3|\
				monthstring4|monthstring5|monthstring6|monthstring7|monthstring8|monthstring9

day = day31|day30|day29|day28|day27|day26|day25|day24|day23|day22|day21|day20|day19|day18|day17|\
		day16|day15|day14|day13|day12|day11|day10|day9|day8|day7|day6|day5|day4|day3|day2|day1

number = Literal("0")|Literal("1")|Literal("2")|Literal("3")|Literal("4")|Literal("5")|\
			Literal("6")|Literal("7")|Literal("8")|Literal("9")

year2d = number + number
year4d = number + number + number + number

year = year4d | year2d

dateseprator = Literal("/") | Literal("-") | Literal(".") | Literal("|")

datestring1 = month +  dateseprator + day + dateseprator + Group(year)

datestring2 = day +  dateseprator + monthstring + dateseprator + Group(year)

datestring = datestring1 | datestring2

cat = lambda l: reduce(lambda x,y: x+y, l)
 
if __name__ == '__main__':
	assert month.parseString('01')[0] == '01'
	assert month.parseString('02')[0] == '02'
	assert month.parseString('03')[0] == '03'
	assert month.parseString('04')[0] == '04'
	assert month.parseString('05')[0] == '05'
	assert month.parseString('06')[0] == '06'
	assert month.parseString('07')[0] == '07'
	assert month.parseString('08')[0] == '08'
	assert month.parseString('09')[0] == '09'
	assert month.parseString('10')[0] == '10'
	assert month.parseString('11')[0] == '11'
	assert month.parseString('12')[0] == '12'

	try:
		month.parseString('0')
	except ParseException, pe:
		pass

	assert datestring.parseString('12/21/2000')[0] == '12'
	assert datestring.parseString('12/21/2000')[2] == '21'
	assert cat(datestring.parseString('12/21/2000')[4]) == '2000'
	
	assert cat(datestring.parseString('12-21-00')[4]) == '00'

	assert datestring.parseString('01-01-0000')[0] == '01'
	assert datestring.parseString('01-01-0000')[2] == '01'
	assert cat(datestring.parseString('01-01-0000')[4]) == '0000'
	
	assert datestring.parseString('12-31-9999')[0] == '12'
	assert datestring.parseString('12-31-9999')[2] == '31'
	assert cat(datestring.parseString('12-31-9999')[4]) == '9999'

	assert datestring.parseString('21-DEC-2000')[0] == '21'
	assert datestring.parseString('21-DEC-2000')[2] == 'DEC'
	assert cat(datestring.parseString('21-DEC-2000')[4]) == '2000'
	
	assert cat(datestring.parseString('21-DEC-00')[4]) == '00'

	assert datestring.parseString('01-JAN-0000')[0] == '01'
	assert datestring.parseString('01-JAN-0000')[2] == 'JAN'
	assert cat(datestring.parseString('01-JAN-0000')[4]) == '0000'
	
	assert datestring.parseString('31-MAR-9999')[0] == '31'
	assert datestring.parseString('31-MAR-9999')[2] == 'MAR'
	assert cat(datestring.parseString('31-MAR-9999')[4]) == '9999'
	
	try:
		datestring.parseString('13/21/2000')
	except ParseException, pe:
		pass
	