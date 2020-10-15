import os
import sys
from vyperlogix.money import floatValue
import globalVars
from vyperlogix.hash import lists
from vyperlogix.gds import julian
from vyperlogix.money import QIF
#from vyperlogix import oodb
from vyperlogix.enum.Enum import *
from vyperlogix.oodb import PickledHash
from vyperlogix.oodb import PickleMethods
from vyperlogix.misc import _utils
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
import traceback
import re
from sets import Set
from vyperlogix.classes import CooperativeClass

_available_sources = [['wellsfargo','paypal']]

_money_dbx = -1

_money_data = lists.HashedLists()
_money_data_checks = lists.HashedLists2()
_money_data_amounts = lists.HashedLists()

_deposits_classified = lists.HashedLists2()
_classified_deposits = lists.HashedLists()

_withdrawls_classified = lists.HashedLists2()

_w2_date_ranges = lists.HashedLists2()

_w2_data_2005 = lists.HashedLists()

#_w2_data_2005['Indotronix'] = floatValue.floatValue('$41,400.00',floatValue.Options.asDollar)
#_w2_data_2005['Indotronix'] = '01-01-2005'
#_w2_data_2005['Indotronix'] = '06-30-2005'

_w2_data_2007 = lists.HashedLists()

_w2_data_2007['DSoftware_1099'] = floatValue.floatValue('$7,280.00',floatValue.Options.asDollar)
_w2_data_2007['DSoftware_1099'] = '05-16-2007'
_w2_data_2007['DSoftware_1099'] = '06-05-2007'

#_w2_data_2007['BigFix_1099'] = floatValue.floatValue('$62,827.37',floatValue.Options.asDollar)
#_w2_data_2007['BigFix_1099'] = '07-09-2007'
#_w2_data_2007['BigFix_1099'] = '12-31-2007'

_w2_data_2006 = lists.HashedLists()

_w2_data_2006['ANR Consultants'] = floatValue.floatValue('$9,206.78',floatValue.Options.asDollar)
_w2_data_2006['ANR Consultants'] = '04-18-2006'
_w2_data_2006['ANR Consultants'] = '06-15-2006'

_w2_data_2006['WeatherNews'] = floatValue.floatValue('$32,740.00',floatValue.Options.asDollar)
_w2_data_2006['WeatherNews'] = '01-20-2006'
_w2_data_2006['WeatherNews'] = '04-15-2006'

_w2_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$45,669.93',floatValue.Options.asDollar)
_w2_data_2006['Sequoia Insurance Company'] = '08-14-2006'
_w2_data_2006['Sequoia Insurance Company'] = '10-15-2006'

_w2_data_by_year = lists.HashedLists2()
_w2_data_by_year[2005] = _w2_data_2005
_w2_data_by_year[2006] = _w2_data_2006
_w2_data_by_year[2007] = _w2_data_2007

_w2_missing_data_2006 = lists.HashedLists()
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$3,909.37',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$1,960.00',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$5,004.24',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$7,102.92',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$7,030.49',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$6,879.46',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$7,082.86',floatValue.Options.asDollar)
_w2_missing_data_2006['Sequoia Insurance Company'] = floatValue.floatValue('$6,670.09',floatValue.Options.asDollar)

_w2_missing_data_by_year = lists.HashedLists2()
_w2_missing_data_by_year[2006] = _w2_missing_data_2006

_w2_misc_income_rule_2007 = lists.HashedLists()
_w2_misc_income_rule_2007['min'] = 500.00

_w2_misc_income_rule_by_year = lists.HashedLists2()
_w2_misc_income_rule_by_year[2007] = _w2_misc_income_rule_2007

class DepositsClassifications(Enum):
    no_classification = 0
    google_adsense = 2**0
    atm_deposit = 2**1
    atm_check_deposit = 2**2
    purchase_return = 2**3
    payroll = 2**4
    tax_refund = 2**5
    misc_deposit = 2**6
    bank_fee_rebate = 2**7
    tax_fin_deposit = 2**8
    Indotronix_Payroll = 2**9
    Visioneer_Payroll = 2**10
    AllBusiness_Payroll = 2**11
    DSoftware_Payroll = 2**12
    Bigfix_Payroll = 2**13
    payroll_advance = 2**14
    funds_transfer = 2**15
    funds_from_wife = 2**16
    RobertHalf_Payroll = 2**17
    EverestConsulting_Payroll = 2**18

def classifyDeposit(dList):
    item = dList[1].lower()
    if (_yyyy == 2005):
        if ( (dList[0] == '03/07') or (dList[0] == '04/12') ):
            return DepositsClassifications.Indotronix_Payroll
        if ( (dList[0] == '07/05') or (dList[0] == '07/07') ):
            return DepositsClassifications.Indotronix_Payroll
        if ( (dList[0] == '08/12') or (dList[0] == '11/04') ):
            return DepositsClassifications.Visioneer_Payroll
        if ( (dList[0] == '11/16') or (dList[0] == '12/05') or (item.find('trinet payroll') > -1) ):
            return DepositsClassifications.AllBusiness_Payroll
    if (item.find('google adsense') > -1):
        return DepositsClassifications.google_adsense
    elif (item.find('indotronix') > -1):
        return DepositsClassifications.Indotronix_Payroll
    elif (item.find('visioneer') > -1):
        return DepositsClassifications.Visioneer_Payroll
    elif (item.find('d software') > -1):
        return DepositsClassifications.DSoftware_Payroll
    elif (item.find('bigfix') > -1):
        return DepositsClassifications.Bigfix_Payroll
    elif (item.find('trust for public payroll') > -1):
        return DepositsClassifications.funds_from_wife
    elif (item.find('robert half') > -1):
        return DepositsClassifications.RobertHalf_Payroll
    elif (item.find('everest consulta payroll') > -1):
        return DepositsClassifications.EverestConsulting_Payroll
    elif (item.find('atm deposit') > -1):
        return DepositsClassifications.atm_deposit
    elif (item.find('atm check deposit') > -1):
        return DepositsClassifications.atm_deposit
    elif (item.find('check crd pur rtrn') > -1):
        return DepositsClassifications.purchase_return
    elif (item.find('payroll') > -1):
        return DepositsClassifications.atm_deposit
    elif (item.find('salary') > -1):
        return DepositsClassifications.atm_deposit
    elif ( (item.find('tax-refund') > -1) or (item.find('tax refund') > -1) ):
        return DepositsClassifications.tax_refund
    elif (item == 'deposit'):
        return DepositsClassifications.misc_deposit
    elif (item.find('advance') > -1):
        return DepositsClassifications.payroll_advance
    elif (item.find('discount') > -1):
        return DepositsClassifications.bank_fee_rebate
    elif (item.find('billpay refund') > -1):
        return DepositsClassifications.bank_fee_rebate
    elif (item.find('transfer') > -1):
        return DepositsClassifications.funds_transfer
    elif (item.find('tax fin') > -1):
        return DepositsClassifications.tax_fin_deposit
    return DepositsClassifications.no_classification

class WithdrawlsClassifications(Enum):
    no_classification = 0
    business_meal = 2**0
    business_travel = 2**1
    petty_cash = 2**2
    advertising = 2**3
    shipping_and_receiveing = 2**4
    business_research = 2**5
    medical_expense = 2**6
    computer_hardware_software = 2**7
    banking_fees = 2**8
    business_utilities = 2**9
    repairs = 2**10
    vehicle_expense = 2**11
    tax_preparation_fees = 2**12
    business_entertainment = 2**13
    insurance_and_fees = 2**14
    patents_and_trademarks = 2**15
    business_clothing = 2**16
    education_expenses = 2**17
    office_supplies = 2**18
    office_furniture = 2**19
    legal_fees = 2**20
    business_rent = 2**21
    vehicle_purchase = 2**22
    pet_expense = 2**23
    petty_cash_paypal = 2**24
    mortgage = 2**25
    moving_expense = 2**26
    savings_plan = 2**27

def classifyWithdrawl(dList, phase=None):
    item = dList[1].lower()
    if (item.find('restaurant') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('fedex') > -1):
        return WithdrawlsClassifications.shipping_and_receiveing
    elif (item.find('step by step') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('keith urban') > -1):
        return WithdrawlsClassifications.business_entertainment
    elif (item.find('vzwrlss') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find("chili's") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('goode wraps') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('upromise') > -1):
        return WithdrawlsClassifications.savings_plan
    elif (item.find('to savings') > -1):
        return WithdrawlsClassifications.savings_plan
    elif (item.find('savings plan') > -1):
        return WithdrawlsClassifications.savings_plan
    elif (item.find('moving & sto') > -1):
        return WithdrawlsClassifications.moving_expense
    elif (item.find('rent payment') > -1):
        return WithdrawlsClassifications.business_rent
    elif (item.find('att*cons') > -1):
        return WithdrawlsClassifications.business_utilities
    elif (item.find('cordella ca') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('pinole ca') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('hsbc online') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('pmr loan') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('home online pmt') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('pmr down payment') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('title company') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('mortgage') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('quicken loans') > -1):
        return WithdrawlsClassifications.mortgage
    elif (item.find('costco whse') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('kenny chesney') > -1):
        return WithdrawlsClassifications.business_entertainment
    elif (item.find('san francisco ca') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('vaccaville ca') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('mankato mn') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('amz*prime') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('wingware') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('drive solutions') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('hpshopping.com') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('dell catalog') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('macromedia') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('soe*') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('playstation') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('wilson windowware') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('software') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('mwave') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('technology') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('realvnc') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('nero ag') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find("fairfield ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("vallejo ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("vacaville ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("concord ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("emeryville ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("folsom ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("anaheim ca") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find("venetian-in") > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('rent-a-car') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('rent a car') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('paypal') > -1):
        return WithdrawlsClassifications.petty_cash_paypal
    elif (item.find('withdrawal') > -1):
        return WithdrawlsClassifications.petty_cash
    elif (item.find('cafe') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('food') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('raley') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('pizza') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('market') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('jillian') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('albertsons') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('working girls') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('safeway store') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('luna azul') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('manchu wok') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('outback') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('black angus') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('hudson news') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('candies') > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("applebee") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("vending") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("stadium") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("grill") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("aramark") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("las vegas") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("callender") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("red robin") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("chevy") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("starbucks") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("margaritas") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("freshens") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("cache creek") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("olive gard") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("oakland a") > -1):
        return WithdrawlsClassifications.business_entertainment
    elif (item.find("pasta") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("back forty") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("resta") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("togo") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("hungry") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("nob hill") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find('fuel') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('travelocity') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('shell oil') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('delta air') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('full serve') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('disney world') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('car rental') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('airport') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('inn') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('fastrak') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('tire') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('chase loans') > -1):
        return WithdrawlsClassifications.vehicle_purchase
    elif (item.find('chase auto') > -1):
        return WithdrawlsClassifications.vehicle_purchase
    elif (item.find('ford') > -1):
        return WithdrawlsClassifications.vehicle_purchase
    elif (item.find('fireside thrift') > -1):
        return WithdrawlsClassifications.vehicle_purchase
    elif (item.find('bart') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('oil change') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('exxon') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('hess') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('wash metro') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('parking') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('turnpk') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('svc station') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('resorts') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('flowers') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('travel') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('jetblue') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('american express') > -1):
        return WithdrawlsClassifications.business_travel
    elif (item.find('atm purchase') > -1):
        return WithdrawlsClassifications.petty_cash
    elif (item.find('paypal') > -1):
        return WithdrawlsClassifications.petty_cash
    elif (item.find('noip com') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('no ip') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('comcast') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('clkbank*com') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('monster products') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('todaysescapes') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('comcast cable') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('digital candle') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('regnow') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('cyber edit') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('tucows') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('assoc shareware') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('sprint pcs') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('sbc consumer') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('webservice') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('verizon') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('acs express') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('vz wireless') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('icca') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('ebay') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('remit online') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('vzw web') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('vistaprint') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('text link') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('.com') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('at&t') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('postal & busin') > -1):
        return WithdrawlsClassifications.shipping_and_receiveing
    elif (item.find('click-n-ship') > -1):
        return WithdrawlsClassifications.shipping_and_receiveing
    elif (item.find('usps') > -1):
        return WithdrawlsClassifications.shipping_and_receiveing
    elif (item.find('mail') > -1):
        return WithdrawlsClassifications.shipping_and_receiveing
    elif (item.find('ups') > -1):
        return WithdrawlsClassifications.shipping_and_receiveing
    elif (item.find('barnes & noble') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('loews metreon') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('www.netflix.com') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('museum') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('gamefly') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('amzn.com') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('imax') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('basebal') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('internet') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('edwards fairfield') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('elton john') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('tivo') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('godaddy.com') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('note netwo') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('google') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('go daddy.com') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('career') > -1):
        return WithdrawlsClassifications.advertising
    elif (item.find('cobra payment') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('kaiser ') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('healthcare') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('optometry') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('best buy') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('intervideo') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('radio shack') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('bestbuycom') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('bmtmicro') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('frys electronics') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('techsmith') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('pgp online') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('hp home store') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('smartphone') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('symantec') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('compusa') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('server') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('walgreen') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('pharmacy') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('memo prove') > -1):
        return WithdrawlsClassifications.medical_expense
    elif (item.find('foreign curr') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('overdraft') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('point-of-sale') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('transaction fee') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('service fee') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('banking') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('safe box') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('bill pay') > -1):
        return WithdrawlsClassifications.banking_fees
    elif (item.find('water & sewer') > -1):
        return WithdrawlsClassifications.business_utilities
    elif (item.find('pacific gas') > -1):
        return WithdrawlsClassifications.business_utilities
    elif (item.find('garbage') > -1):
        return WithdrawlsClassifications.business_utilities
    elif (item.find('city of vallejo') > -1):
        return WithdrawlsClassifications.business_utilities
    elif (item.find('home depot') > -1):
        return WithdrawlsClassifications.repairs
    elif (item.find('lumber') > -1):
        return WithdrawlsClassifications.repairs
    elif (item.find('orchard supply') > -1):
        return WithdrawlsClassifications.repairs
    elif (item.find('sears') > -1):
        return WithdrawlsClassifications.repairs
    elif (item.find('glass') > -1):
        return WithdrawlsClassifications.repairs
    elif (item.find('autozone') > -1):
        return WithdrawlsClassifications.vehicle_expense
    elif (item.find('ca dmv') > -1):
        return WithdrawlsClassifications.vehicle_expense
    elif (item.find('auto service') > -1):
        return WithdrawlsClassifications.vehicle_expense
    elif (item.find('pepboys') > -1):
        return WithdrawlsClassifications.vehicle_expense
    elif (item.find('taxcut') > -1):
        return WithdrawlsClassifications.tax_preparation_fees
    elif (item.find('h&r block') > -1):
        return WithdrawlsClassifications.tax_preparation_fees
    elif (item.find('microsoft') > -1):
        return WithdrawlsClassifications.computer_hardware_software
    elif (item.find('comedy club') > -1):
        return WithdrawlsClassifications.business_entertainment
    elif (item.find('tcktweb') > -1):
        return WithdrawlsClassifications.business_entertainment
    elif (item.find('eve-online') > -1):
        return WithdrawlsClassifications.business_research
    elif (item.find('csaa') > -1):
        return WithdrawlsClassifications.insurance_and_fees
    elif (item.find('ca state auto') > -1):
        return WithdrawlsClassifications.insurance_and_fees
    elif (item.find('auto insurance') > -1):
        return WithdrawlsClassifications.insurance_and_fees
    elif (item.find('us patent') > -1):
        return WithdrawlsClassifications.legal_fees
    elif (item.find('legal fee') > -1):
        return WithdrawlsClassifications.legal_fees
    elif (item.find('macy*s') > -1):
        return WithdrawlsClassifications.business_clothing
    elif (item.find('nordstrom') > -1):
        return WithdrawlsClassifications.business_clothing
    elif (item.find('wearhouse') > -1):
        return WithdrawlsClassifications.business_clothing
    elif (item.find('brainbench') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('devry') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('textbook') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('learning') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('vue*allaire') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('trafficschoo') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('university') > -1):
        return WithdrawlsClassifications.education_expenses
    elif (item.find('office') > -1):
        return WithdrawlsClassifications.office_supplies
    elif (item.find('target') > -1):
        return WithdrawlsClassifications.office_supplies
    elif (item.find('qvc*2972654971') > -1):
        return WithdrawlsClassifications.office_furniture
    elif (item.find(' law ') > -1):
        return WithdrawlsClassifications.legal_fees
    elif (item.find(" ut ") > -1):
        return WithdrawlsClassifications.business_meal
    elif (item.find("pet") > -1):
        return WithdrawlsClassifications.pet_expense
    elif (item.find("cat clinic") > -1):
        return WithdrawlsClassifications.pet_expense
    if (phase == None):
        if (_money_data_checks.has_key(dList[1])):
            chk = _money_data_checks[dList[1]]
            dList[1] = '%s %s %s' % (chk.memo,chk.payee,chk.category.replace(':',' '))
            classifyWithdrawl(dList,1)
    pass
    return WithdrawlsClassifications.no_classification

def detailsForCheckByNumber(chkNum):
    if (not isinstance(chkNum,str)):
        chkNum = '%d' % chkNum
    if (_money_data_checks.has_key(chkNum)):
        chk = _money_data_checks[chkNum]
        return 'Check #%s %s %s %s' % (chkNum,chk.memo if chk.memo else '',chk.payee if chk.payee else '',chk.category.replace(':',' ') if chk.category else '')
    return chkNum

def total_w2_data():
    total_w2s = floatValue.floatValue('0.0',floatValue.Options.asDollar)
    if (_w2_data_by_year.has_key(_yyyy)):
        for k,v in _w2_data_by_year[_yyyy].iteritems():
            total_w2s += v[0]
            if (len(v) > 1):
                v[1:] = [d.split('-') for d in v[1:]]
                x = []
                for d in v[1:]:
                    x.append([int(n) for n in d])
                v[1:] = x
                v[1:] = [(d,julian.DayOfYear(d[0],d[1],d[2])) for d in v[1:] if len(d) == 3]
                begin = v[1:][0][-1]
                end = v[1:][-1][-1]
                _w2_date_ranges[(begin,end)] = k
    return total_w2s

def reverseDepositsByClassifications():
    for k,v in _deposits_classified.iteritems():
        _classified_deposits[v[0] if isinstance(v,list) else str(v)] = k.split(',')
    if (0):
        items = _classified_deposits[DepositsClassifications.atm_deposit]
        for item in items:
            val = floatValue.floatValue(item[-1],floatValue.Options.asDollar)
            if (isinstance(item[0],list)):
                mmDD = item[0][0]
                doy = int(item[0][-1])
                mm,dd = mmDD.split('/')[:2]
            else:
                mmDD = item[0]
                doy = -1
                mm,dd = mmDD.split('/')[:2]
            _dt = '%02d/%02d/%04d' % (int(mm),int(dd),int(_yyyy))
            recs = [_money_dbx[r] for r in _money_dbx.queryMostlyANDitems(_dt,str(val),str(-val)) if _money_dbx.has_key(r)]
            recs = [r for r in recs if r.category ] # str(r.category).lower().find('payroll') > -1
            if len(recs) > 0:
                print '(reverseDepositsByClassifications) :: '
                for rec in recs:
                    print '\t%s' % str(item)
                    print '\t%s' % rec.pretty()
                    print '\t%s' % '='*30
    pass

def w2_employer_for_day_of_year(doy):
    for k,v in _w2_date_ranges.iteritems():
        if ( (doy >= k[0]) and (doy <= k[-1]) ):
            return v
    return ''

def w2_employer_delta_days_of_year(doy):
    d = {}
    for k,v in _w2_date_ranges.iteritems():
        d[doy - k[-1]] = v
    return d

def handle_missing_w2_for_employer(item,employer):
    isFound = False
    if (_w2_missing_data_by_year.has_key(employer)):
        val_item = floatValue.floatValue(item[-1],floatValue.Options.asDollar)
        if (val_item in _w2_missing_data_by_year[employer]):
            for i in xrange(0,len(_w2_missing_data_by_year[employer])):
                if (_w2_missing_data_by_year[employer][i] == val_item):
                    isFound = True
                    del _w2_missing_data_by_year[employer][i]
                    break
    return isFound

def actualYearBasedOnMonthDay(mm,dd,yyyy):
    if ( (mm == 12) and (dd < 8) ):
        return yyyy-1
    return yyyy

def gather_w2_data_for_dates():
    db = lists.HashedLists()
    d = _classified_deposits[DepositsClassifications.atm_deposit]
    xfer_from_wife_amount = floatValue.floatValue('900.00',floatValue.Options.asDollar)
    for item in d:
        val = floatValue.floatValue(item[-1],floatValue.Options.asDollar)
        if (val == xfer_from_wife_amount):
            db['Xfer from Wife for Bills'] = item
        else:
            dt = item[0].split('/')[:2]
            dt = [int(n) for n in dt]
            doy = julian.DayOfYear(dt[0],dt[1],actualYearBasedOnMonthDay(dt[0],dt[1],_yyyy))
            item[0] = [item[0],doy]
            employer = w2_employer_for_day_of_year(doy)
            db[employer] = item
            handle_missing_w2_for_employer(item,employer)
    if (_w2_data_by_year.has_key(_yyyy)):
        for k,v in db.iteritems():
            if (_w2_data_by_year[_yyyy].has_key(k)):
                vals = [floatValue.floatValue(item[-1],floatValue.Options.asDollar) for item in v]
                total_vals = sum(vals)
                expected_total = _w2_data_by_year[_yyyy][k][0]
                if (total_vals != expected_total):
                    diff_val = max(total_vals,expected_total) - min(total_vals,expected_total)
                    if (diff_val in vals):
                        i = vals.index(diff_val)
                        db[''] = v[i]
                        del v[i]
                    doys = [item[0][-1] for item in v]
                    doys.sort()
                    diffs = [0]
                    dayNum = doys[0]
                    for doy in doys[1:]:
                        diffs.append(doy - dayNum)
                        dayNum = doy
                    pass
    return db

def sortItemsBasedOnDOY(items):
    d = lists.HashedLists()
    for item in items:
        if (not isinstance(item[0],list)):
            toks = [int(n) for n in item[0].split('/')]
            if (len(toks) == 2):
                toks.append(_yyyy)
            if (len(toks) == 3):
                item[0] = [item[0],julian.DayOfYear(toks[0],toks[1],actualYearBasedOnMonthDay(toks[0],toks[1],toks[-1]))]
    for item in items:
        d[item[0][-1]] = item
    keys = d.keys()
    keys.sort()
    _items = []
    for k in keys:
        for n in d[k]:
            _items.append(n)
    return _items

def redactDetails2(item):
    iBegin = item.find('?MCC=')
    if (iBegin > -1):
        item = item[0:iBegin] # + item[1][iEnd:]
    return item

def redactDetails(item):
    iBegin = item.find('4873')
    if (iBegin > -1):
        iEnd = item.find('7156')
        item = item[0:iBegin] # + item[1][iEnd:]
    return redactDetails2(item)

def reclassifyUnclassifiedDeposits(d_w2Deposits):
    # Any value that is an ATM deposit greater than the threshold in _w2_misc_income_rule_by_year[_yyyy] is considered to be "income"
    pass

def reportDeposits():
    deposits = globalVars.dataFilesFor(globalVars.DataFileTypes.deposits,_yyyy)
    k_deposits = []
    for f in deposits:
        dbx = PickledHash(globalVars.PathName(f))
        for k,v in dbx.iteritems():
            _deposits_classified[','.join(v)] = [classifyDeposit(v)]
            k_deposits.append(v)
        dbx.close()
    assert len(k_deposits) == len(_deposits_classified.keys()), 'Oops, something went wrong with the way deposits are being handled.'
    d = {}
    cd = lists.HashedLists()
    total_deposits = floatValue.floatValue('0.0',floatValue.Options.asDollar)
    for k,v in _deposits_classified.iteritems():
        val = k.split(',')
        total_deposits += floatValue.floatValue(val[-1],floatValue.Options.asDollar)
        if (v[0] == DepositsClassifications.no_classification):
            d[k] = v
        else:
            cd[v[0]] = val
    assert len(d) == 0, 'Oops, forgot to classify %d deposits.\n%s' % (len(d),str(d))
    print 'Total Deposits: $%-10.2f' % total_deposits
    td = {}
    for k,v in cd.iteritems():
        td[k] = floatValue.floatValue('0.0',floatValue.Options.asDollar)
        for item in v:
            td[k] += floatValue.floatValue(item[-1],floatValue.Options.asDollar)
    _total_deposits = floatValue.floatValue('0.0',floatValue.Options.asDollar)
    for k,v in td.iteritems():
        _total_deposits += v
    assert total_deposits == _total_deposits, 'Oops, the Total of Deposits does not match when compared with the total of the Deposits Classifications.'
    w2_total = total_w2_data()
    reverseDepositsByClassifications()
    # gather deposits based on their dates from the viewpoint of the w2 data...
    w2_deposits = gather_w2_data_for_dates()
    reclassifyUnclassifiedDeposits(w2_deposits)
    for k,v in td.iteritems():
        print '$%10.2f\t%s' % (v,k)
    print
    print 'W2 Analysis:'
    total_payroll_atm_deposits = td[DepositsClassifications.atm_deposit]
    print 'Total for ATM Deposits=$%-10.2f' % (total_payroll_atm_deposits)
    print 'Total for W2 Deposits=$%-10.2f' % (w2_total)
    print '='*30
    print 'Remainder Deposits less W2 Deposits=$%-10.2f' % (total_payroll_atm_deposits-w2_total)
    print
    print '='*30
    print
    print 'W2 Deposit Analysis:'
    isUnclassified = False
    _total_for_employers = floatValue.floatValue('0.00',floatValue.Options.asDollar)
    for k,v in w2_deposits.iteritems():
        print
        print '(%s)' % k if len(k) > 0 else 'UNCLASSIFIED'
        isUnclassified = False if len(k) > 0 else True
        _total_per_employer = floatValue.floatValue('0.00',floatValue.Options.asDollar)
        _items = sortItemsBasedOnDOY(v)
        for item in _items:
            val = floatValue.floatValue(item[-1],floatValue.Options.asDollar)
            if (isinstance(item[0],list)):
                mmDD = item[0][0]
                doy = int(item[0][-1])
                mm,dd = mmDD.split('/')[:2]
            else:
                mmDD = item[0]
                doy = -1
                mm,dd = mmDD.split('/')[:2]
            print '$%10.2f\t%s/%s, (#%4d)\t%s' % (val,mmDD,actualYearBasedOnMonthDay(mm,dd,_yyyy),doy,item[1])
            if (isUnclassified):
                if (_money_data_amounts.has_key(item[-1])):
                    xList = _money_data_amounts[item[-1]]
                    for xItem in xList:
                        print '\t%s\t%s\t%s' % (xItem.date,xItem.memo,xItem.payee)
                    pass
            _total_per_employer += val
        print '='*11
        print '$%10.2f Total' % _total_per_employer
        _total_for_employers += _total_per_employer
        print
    print 'Grand Total=$%10.2f' % _total_for_employers
    print
    print '='*30
    isAccountedFor = _total_for_employers == total_payroll_atm_deposits
    print 'All W2 Deposits have %sbeen accounted for however some of them may require re-classification.' % ('NOT ' if not isAccountedFor else '')
    print '='*30
    print
    print 'General Deposit Analysis:'
    _total_for_classes = floatValue.floatValue('0.00',floatValue.Options.asDollar)
    for k,v in cd.iteritems():
        print
        print '(%s)\n' % str(k)
        _total_per_class = floatValue.floatValue('0.00',floatValue.Options.asDollar)
        _items = sortItemsBasedOnDOY(v)
        for item in _items:
            val = floatValue.floatValue(item[-1],floatValue.Options.asDollar)
            if (not isinstance(item[0],list)):
                mmDD = item[0]
                doy = -1
                mm,dd = mmDD.split('/')[:2]
            else:
                mmDD = item[0][0]
                doy = int(item[0][-1])
                mm,dd = mmDD.split('/')[:2]
            print '$%10.2f\t%s/%s, (#%4d)\t%s' % (val,mmDD,actualYearBasedOnMonthDay(mm,dd,_yyyy),doy,redactDetails(item[1]))
            _total_per_class += val
        print '='*11
        print '$%10.2f Total' % _total_per_class
        _total_for_classes += _total_per_class
        print
    print '$%10.2f Grand Total' % _total_for_classes
    print
    print '='*30
    pass

def reportWithdrawls():
    withdrawls = globalVars.dataFilesFor(globalVars.DataFileTypes.withdrawls,_yyyy)
    k_withdrawls = []
    for f in withdrawls:
        dbx = PickledHash(globalVars.PathName(f))
        for k,v in dbx.iteritems():
            if (v[0].isdigit()):
                x = v[0]
                v[0] = v[1]
                v[1] = detailsForCheckByNumber(x)
            s = ','.join(v)
            _withdrawls_classified[s] = [classifyWithdrawl(v)]
            k_withdrawls.append(s)
        dbx.close()
    for k,v in _withdrawls_classified.iteritems():
        if (v[0] == WithdrawlsClassifications.no_classification):
            data = k.split(',')
            data_value = floatValue.floatValue(data[-1],floatValue.Options.asDollar)
            if (data_value == floatValue.floatValue('1550.00',floatValue.Options.asDollar)):
                _withdrawls_classified[k] = [WithdrawlsClassifications.business_rent]
            elif (data_value == floatValue.floatValue('5500.00',floatValue.Options.asDollar)):
                _withdrawls_classified[k] = [WithdrawlsClassifications.education_expenses]
            elif (data[0] == '5277'):
                _withdrawls_classified[k] = [WithdrawlsClassifications.business_utilities]
            elif (data[0] in ['5279','5281','5285','5288','5292','5297','5303']):
                _withdrawls_classified[k] = [WithdrawlsClassifications.medical_expense]
            elif (data[0] == '5287'):
                _withdrawls_classified[k] = [WithdrawlsClassifications.legal_fees]
            elif (data[0] == '5308'):
                _withdrawls_classified[k] = [WithdrawlsClassifications.insurance_and_fees]
            elif (data[0] == '5311'):
                _withdrawls_classified[k] = [WithdrawlsClassifications.medical_expense]
    d = {}
    cd = lists.HashedLists()
    total_withdrawls = floatValue.floatValue('0.0',floatValue.Options.asDollar)
    for k,v in _withdrawls_classified.iteritems():
        val = k.split(',')
        total_withdrawls += floatValue.floatValue(val[-1],floatValue.Options.asDollar)
        if (v[0] == WithdrawlsClassifications.no_classification):
            d[k] = v
        else:
            cd[v[0]] = val
    print 'Total Withdrawals: $%-10.2f' % total_withdrawls
    print '='*80
    print 'UNCLASSIFIED EXPENSES:'
    _d = d.keys()
    _d.sort()
    for k in _d:
        print '%s' % redactDetails(k)
    print '='*80
    print '='*80
    print 'CLASSIFIED EXPENSES:\n'
    cd_total_withdrawls = floatValue.floatValue('0.0',floatValue.Options.asDollar)
    cd_total_withdrawls2 = floatValue.floatValue('0.0',floatValue.Options.asDollar)
    report_details = lists.HashedLists()
    for k,v in cd.iteritems():
        d = lists.HashedLists()
        report_details[k] = '\t%s\n' % str(k)
        cd_total_withdrawls_per_class = floatValue.floatValue('0.0',floatValue.Options.asDollar)
        for item in v:
            val = floatValue.floatValue(item[-1],floatValue.Options.asDollar)
            cd_total_withdrawls += val
            cd_total_withdrawls_per_class += val
            d[item[0]] = item
        d_keys = d.keys()
        d_keys.sort()
        for dk in d_keys:
            for di in d[dk]:
                val = floatValue.floatValue(di[-1],floatValue.Options.asDollar)
                try:
                    mm,dd = di[1].split('/')[:2]
                except:
                    mm,dd = di[0].split('/')[:2]
                report_details[k] = '$%10.2f\t%s/%s\t%s' % (val,di[0],actualYearBasedOnMonthDay(mm,dd,_yyyy),redactDetails(di[1]))
        report_details[k] = ''
        report_details[k] = '='*11
        _line = '$%10.2f Total Withdrawals for %s' % (cd_total_withdrawls_per_class,str(k))
        cd_total_withdrawls2 += cd_total_withdrawls_per_class
        print _line
        report_details[k] = _line
        report_details[k] = ''
        print
    print '$%10.2f Total Classified Withdrawals (%s)' % (cd_total_withdrawls,'VALIDATED' if cd_total_withdrawls == cd_total_withdrawls2 else 'WRONG')
    print '='*80
    print '\n\n'
    print '='*80
    print
    for k,v in cd.iteritems():
        print '\n'.join(report_details[k])
    print '$%10.2f Total Classified Withdrawals' % cd_total_withdrawls
    print '='*80
    pass

def getMoneyCheck(chkNum):
    if (not isinstance(chkNum,str)):
        chkNum = '%d' % chkNum
    if (_money_data_checks.has_key(chkNum)):
        return _money_data_checks[chkNum]
    return None

def main_wellsfargo():
    global _money_dbx
    qifReader = QIF.QifReader(None) # ['12/8/%d' % (_yyyy-1),'12/31/%d' % _yyyy]
    fname = qifReader.getDatabaseFileNameFor(_yyyy)
    dbx = PickledHash(fname,PickleMethods.useSafeSerializer)
    _vals = oodb.unique([dbx[k] for k in dbx.keys() if k.startswith('amount_')])
    #_vals = [v for v in _vals if floatValue.floatValue(v) < 0.0]
    for k in _vals:
        if (dbx.has_key(k)):
            v = dbx[k]
            if (not isinstance(v,list)):
                v = [v]
            for item in v:
                qif = dbx[item]
                _money_data_amounts[qif.amount] = qif
    _date_vals = oodb.unique([dbx[k] for k in dbx.keys() if k.startswith('__date_')])
    _date_vals.sort()
    _keys = []
    for k in _date_vals:
        val = dbx[k]
        if (isinstance(val,list)):
            for v in val:
                _keys.append(v)
        else:
            _keys.append(v)
    _keys = oodb.unique(_keys)
    _keys.sort()
    _items = [dbx[k] for k in _keys]
    for item in _items:
        _money_data[item.date[-1]] = item
        if (item.checkNumber):
            _money_data_checks['%d' % item.checkNumber] = item
    _money_dbx = dbx
    reportDeposits()
    reportWithdrawls()
    dbx.close()

def main_paypal():
    global _isVerbose

    make_unqiue_type = lambda t:'_'.join(t.split())

    reportable_keys = ['Transaction ID','Date','Time','Time Zone','Name','Gross','Fee','Net','Type']
    reportable_totals_keys = ['Gross','Fee','Net']

    _income_classifications = ['CreditClassifications.Dividend_From_PayPal_Money_Market.PayPal_-_Money_Market']

    _unique_credit_types = Set()
    _unique_debit_types = Set()

    _classified_credits = lists.HashedLists()
    _classified_debits = lists.HashedLists()

    _classified_income_credits = lists.HashedLists()
    _classified_refund_credits = lists.HashedLists()
    
    _debit_classifications = lists.HashedLists2()
    
    class CreditClassifications(Enum):
        no_classification = 0
    class DebitClassifications(Enum):
        no_classification = 0

    class DebitTaxClassifications(Enum):
        no_classification = 1
        advertising = 2**1
        business_meals = 2**2
        business_entertainment = 2**3
        business_travel = 2**4
        computers_software = 2**5
        business_research = 2**6
        medical_expense = 2**7
        postage_expense = 2**8
        copy_services = 2**9
        credit_monitoring = 2**10
        banking_expense = 2**11

    _debit_classifications['DebitClassifications.Debit_Card_Authorization.TMOBILE*HOTSPOT'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.WBO*THE_MATRIX_ONLINE'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ALBERTSONS'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ARAMARK_OAKLAND_STADIU_OAKLAND_CA'] = DebitTaxClassifications.business_entertainment
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ARAMARK_SVCS_CO_PACIFI_SAN_RAMON_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BART-EL_CERRITO_DEL_NR_RICHMOND_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BART_NORTH_BERKELEY_BERKELEY_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BART_SAN_BRUNO_STATION_SAN_BRUNO_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BEST_BUY'] = DebitTaxClassifications.computers_software
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CHILI\'S_GRILL'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ARAMARK_SVCS_CO_SBC_SA_SAN_RAMON_CA'] = DebitTaxClassifications.business_entertainment
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ARAMARK_SVC_CO_PACIFIC_SAN_RAMON_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CHILIS'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CONTRA_COSTA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.DISNEY_ROYAL_STREET_ANAHEIM_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.EL_DORADO_SVCS_BOARDIN_LONG_BEACH_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.EVE-ONLINESUBSCRIPTION_REYKJAVIK_IS'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.LUMINATOR_SUNGLASSES'] = DebitTaxClassifications.medical_expense
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.MLB.COM_WWW.MLB.COM_NY'] = DebitTaxClassifications.business_entertainment
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.MOLLIE_ST_BAYHILL_SAZ_SAN_BRUNO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.NOB_HILL_#610_SA9_PLEASANTON_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SAFEWAY_FUEL'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SAFEWAY_STORE00009894_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SHELL/708_ADMIRAL_CALL_VALLEJO_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SOE*STARWARS_GALAXIES'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SPECIALTY\'S_CAFE_&_Q49_SAN_FRANCISCO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.TOGO\'S_PLEASANTON_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.UNION'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.VALERO'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.WALGREEN_00062Q39_SAN_FRANCISCO_CA'] = DebitTaxClassifications.medical_expense
    _debit_classifications['DebitClassifications.PayPal_Services.UPS*1ZX515V10390018415'] = DebitTaxClassifications.postage_expense
    _debit_classifications['DebitClassifications.PayPal_Services.UPS*1ZX515V10392497029'] = DebitTaxClassifications.postage_expense
    _debit_classifications['DebitClassifications.PayPal_Services.UPS*INTERNETSHIPWAYBIL'] = DebitTaxClassifications.postage_expense
    _debit_classifications['DebitClassifications.Web_Accept_Payment_Sent.Dennis_Babkin'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Web_Accept_Payment_Sent.FeedShot'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Web_Accept_Payment_Sent.paypal@amplecom.com'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.DOWNEY_VALERO_DOWNEY_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.FEDEX_KINKO\'S'] = DebitTaxClassifications.copy_services
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.GARMIN_INTERNATIONAL_OLATHE_KS'] = DebitTaxClassifications.computers_software
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.MATE1.COM_MONTREAL_CA'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.Microsoft_Online_Svcs'] = DebitTaxClassifications.computers_software
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.THE_VENETIAN_SHOWROO_LAS_VEGAS_NV'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Authorization.WALGREENS_SAN_FRANCISCO_CA'] = DebitTaxClassifications.medical_expense
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ALBERTSONS_#7254_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.APPLEBEE\'S_FOR01700020_MIDVALE_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.Applebee\'s_Ft_Union_Midvale_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BLACK_ANGUS_VALLEJO_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BRITTON\'S_MINI_MARTQ39_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.BRITTON\'S_MINI_MAR_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CAESARS_ELTON_JOHN_STO_LAS_VEGAS_NV'] = DebitTaxClassifications.business_entertainment
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CHEVRON'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CHIPOTLE_#0138_Q20_SAN_FRANCISCO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.CIC*TRIPLE_ADVANTAGE'] = DebitTaxClassifications.credit_monitoring
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.COURTYARD_BY_MARRIOTT_SALT_LK_CITY_UT'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.DELTA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.E_MEDIA_CONCEPTS_CORP'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.FRESHENS_#37_OAKLAND_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.HMS_HOST_-_SLC-AIRPT_#_SALT_LAKE_CIT_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.JAGDEEP_SIDHU_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.LONE_PEAK'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.MARIE_CALLENDER\'S_WEST_VALLEY_C_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.MATE1.COM_MONTREAL_QC'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.MAVERICK_COUNTRY'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.O\'CONNOR_LUMBER_ACE_HA_VALLEJO_CA'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.OUTBACK_#4510_SANDY_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.PAC_BELL_CONCES#76455_SAN_FRANCISCO_CA'] = DebitTaxClassifications.business_entertainment
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.PIZZA_H011699'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.PIZZA_H011699_01200Q_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.PIZZA_HUT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.RALEYS_#307_S4I_VALLEJO_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.RED_WHITE_&_BLUE_RVC76_LAS_VEGAS_NV'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.REMIT_ONLINE_DENVER_CO'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.ROADRUNNER_GAS_VALLEJO_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.RUBY_TUESDAY'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SMITHS_FOOD_#4132_SS6_DRAPER_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SOHQPAY.COM_1-320-210-300_NL'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SPRGBRKVID'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.TUCOWS_*AUTHORCNTR8468'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.UNION_POST_SAN_FRANCISCO_CA'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.USPS'] = DebitTaxClassifications.postage_expense
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.VILIEN_DELI_CAFE_DRAPER_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.Vilien_Deli_Cafe_Draper_UT'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.WALGREEN_00006Q39_SAN_FRANCISCO_CA'] = DebitTaxClassifications.medical_expense
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.WORKING_GIRLS'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.WPG_PRODUCTS_LOS_ANGELES_CA'] = DebitTaxClassifications.business_research
    _debit_classifications['DebitClassifications.Web_Accept_Payment_Sent.JGsoft_-_Just_Great_Software'] = DebitTaxClassifications.computers_software
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.GODADDY.COM'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.QUIZNOS_SUB_#5044_Q22_EMERYVILLE_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.SUBWAY_#36635_00366Q16_EMERYVILLE_CA'] = DebitTaxClassifications.business_meals
    _debit_classifications['DebitClassifications.Debit_Card_Purchase.TOWER_MART_#86_Q53_CORDELLA_CA'] = DebitTaxClassifications.business_travel
    _debit_classifications['DebitClassifications.Payment_Sent.GlobalWare_Solutions_Security_Key'] = DebitTaxClassifications.banking_expense
    _debit_classifications['DebitClassifications.Preapproved_Payment_Sent.GoDaddy.com,_Inc.'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Subscription_Payment_Sent.Byethost_Internet'] = DebitTaxClassifications.advertising
    _debit_classifications['DebitClassifications.Temporary_Hold.PayPal'] = DebitTaxClassifications.banking_expense
    
    class MoneyTracker(CooperativeClass.Cooperative):
        def __init__(self,rep_keys=[]):
            self.__values__ = {}
            self.reportable_keys = rep_keys
            self.__gross_symbol__ = 'Gross'
            self.__ZERO__ = floatValue.floatValue('0.00',floatValue.Options.asDollar)

        def __repr__(self):
            return '(%s)' % (str(self.__class__))

        def store(self,item):
            if (type(self) != type(item)):
                for k in self.reportable_keys:
                    _fv = floatValue.floatValue(item[k],floatValue.Options.asDollar)
                    self.values[k] = ((self.values[k] if (self.values.has_key(k)) else self.__ZERO__) + _fv)
            else:
                for k in self.reportable_keys:
                    self.values[k] = (self.values[k] if (self.values.has_key(k)) else self.__ZERO__) + item.values[k]

        def iteritems(self):
            return ((k,v) for k,v in self.values.iteritems() if (k in self.reportable_keys))
        
        def __str__(self):
            _values = []
            for k,v in self.iteritems():
                _v = '$%-10.2f' % v
                _values.append('%s=%s' % (k,_v.strip()))
            return '(%s)' % '\t'.join(_values)

        def __lt__(self, other):
            if (type(self) == type(other)):
                try:
                    return all([self.values[k] < other.values[k] for k in self.values.keys()])
                except:
                    pass
            return False
        
        def __le__(self, other):
            if (type(self) == type(other)):
                try:
                    return all([self.values[k] <= other.values[k] for k in self.values.keys()])
                except:
                    pass
            return False
        
        def __eq__(self, other):
            if (type(self) == type(other)):
                    return all([self.values[k] == other.values[k] for k in self.values.keys()])
            return False
        
        def __ne__(self, other):
            if (type(self) == type(other)):
                try:
                    return all([self.values[k] != other.values[k] for k in self.values.keys()])
                except:
                    pass
            return False
        
        def __gt__(self, other):
            if (type(self) == type(other)):
                try:
                    return all([self.values[k] > other.values[k] for k in self.values.keys()])
                except:
                    pass
            return False
        
        def __ge__(self, other):
            if (type(self) == type(other)):
                try:
                    return all([self.values[k] >= other.values[k] for k in self.values.keys()])
                except:
                    pass
            return False

        def get_reportable_keys(self):
            return self.__reportable_keys__

        def set_reportable_keys(self,keys):
            self.__reportable_keys__ = keys
            self.__values__ = lists.HashedLists2()
            for f in reportable_keys:
                self.__values__[f] = floatValue.floatValue('0.00',floatValue.Options.asDollar)
                    
        def get_gross_symbol(self):
            return self.__gross_symbol__

        def set_gross_symbol(self,symbol):
            self.__gross_symbol__ = symbol

        def get_values(self):
            return self.__values__

        values = property(get_values)
        gross_symbol = property(get_gross_symbol,set_gross_symbol)

    _classified_credits_totals = MoneyTracker(reportable_totals_keys)
    _classified_debits_totals = MoneyTracker(reportable_totals_keys)

    _classified_income_totals = MoneyTracker(reportable_totals_keys)
    _classified_refund_totals = MoneyTracker(reportable_totals_keys)

    def normalizeName(name):
        toks = []
        for t in name.split():
            if (t.isdigit()):
                break
            elif re.match(r"\(?\b[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b\Z", t):
                break
            else:
                toks.append(t)
        return '_'.join(toks)
    
    def normalizeDate(d):
        toks = d.split('/')
        toks[0] = '%02d' % int(toks[0])
        toks[1] = '%02d' % int(toks[1])
        toks[2] = '%04d' % int(toks[2])
        return '/'.join(toks)
    
    def classify(isCredit,_item):
        try:
            _type = '%s.%s' % (_item['Type'],normalizeName(_item['Name']))
        except KeyError:
            _type = None
            print >>sys.stderr, '_item=%s' % _item
            exc_info = sys.exc_info()
            info_string = '\n'.join(traceback.format_exception(*exc_info))
            print >>sys.stderr, info_string
        if (_type):
            if (isCredit):
                _unique_credit_types.add(_type)
                _classification = CreditClassifications('%s' % make_unqiue_type(_type))
                _classified_credits[str(_classification)] = _item
                _classified_credits_totals.store(_item)
            else:
                _unique_debit_types.add(_type)
                _classification = DebitClassifications('%s' % make_unqiue_type(_type))
                
                _classified_debits[str(_classification)] = _item if (not isinstance(_item,dict)) else lists.HashedLists2(_item)
                _classified_debits_totals.store(_item)
            if (_classification < 0):
                print >>sys.stderr, 'ERROR: Unable to determine the classification for type "%s".' % _type
            elif (_isVerbose):
                print '_classification "%s" for type "%s".' % (_classification,_type)
        pass
    
    def _report_item(_item):
        s = []
        for k,v in _item.iteritems():
            s.append('%s=%s' % (k,v))
        return '\t'.join(s)
    
    def report_item(isCredit,_item):
        classify(isCredit,_item)
        if (_isVerbose):
            for k,v in _item.iteritems():
                print '\t\t\t%s=%s' % (k,v)
            print '-'*80
            
    def _report_data(items):
        data = [items[k] if items.has_key(k) else '' for k in reportable_keys]
        return '\t\t%s' % '\t'.join([d for d in data if len(d) > 0])
    
    def report_data(key,items,isCredit):
        if (isCredit):
            _is_income_credit = (key in _income_classifications)
            if (_is_income_credit):
                if (_isVerbose):
                    print '(INCOME.1) %s' % (items)
                _classified_income_credits['INCOME'] = items
                x = _classified_income_credits['INCOME']
                if (_isVerbose):
                    print '(INCOME.2) (%s) len=[%s]' % (type(x),len(x))
            else:
                if (_isVerbose):
                    print '(REFUND.1) %s' % (items)
                _classified_refund_credits['REFUND'] = items
                x = _classified_refund_credits['REFUND']
                if (_isVerbose):
                    print '(REFUND.2) (%s) len=[%s]' % (type(x),len(x))
        if (_isVerbose):
            print _report_data(items)
            
    _ignore_names = ['...','Bank Account']
    qifReader = QIF.QifReader(None)
    fname = qifReader.getDatabaseFileNameFor(_yyyy)
    p = os.path.abspath('data\\paypal\\%d' % _yyyy)
    print 'p=%s' % p
    try:
        files = [os.sep.join([p,f]) for f in os.listdir(p) if (f.find('-details_name') > -1) and (f.find('Memo-') == -1)]
        for f in files:
            _isCredit = f.find('Credit-') > -1
            if (_isVerbose):
                print '(%s) f=[%s]' % ('CREDIT' if _isCredit else 'DEBIT',f)
            dbx = PickledHash(f,PickleMethods.useSafeSerializer)
            _keys = dbx.normalizedSortedKeys()
            for k,v in dbx.iteritems():
                if (k not in _ignore_names):
                    if (_isVerbose):
                        print '(%s) :: %s=(%s) len=(%s)' % (f,k,type(v),len(v))
                    if (isinstance(v,lists.HashedLists2)):
                        report_item(_isCredit,v)
                    elif (isinstance(v,list)):
                        if (_isVerbose):
                            print '\t\tBEGIN: %s' % ('='*30)
                        for item in v:
                            report_item(_isCredit,item)
                        if (_isVerbose):
                            print '\t\tEND! %s' % ('='*30)
                            print ''
            dbx.close()
        print 'Classified Credit Items:'
        print str(_classified_credits_totals)
        _keys = list(set(_classified_credits.keys()))
        _keys.sort()
        for k in _keys:
            if (_isVerbose):
                print '\n\t"%s"' % k
                print '\t\t%s' % '\t'.join(reportable_keys)
            for items in _classified_credits[k]:
                report_data(k,items,True)
            pass
        print '='*80
        print ''

        _money_sum = MoneyTracker(reportable_totals_keys)
        
        print 'Classified Credit (Income) Items:'
        d_values = lists.HashedLists()
        for k,v in _classified_income_credits.iteritems():
            if (isinstance(v,list)):
                for item in v:
                    item['Date'] = normalizeDate(item['Date'])
                    d_values[item['Date']] = item
                    _classified_income_totals.store(item)
            else:
                v['Date'] = normalizeDate(v['Date'])
                d_values[v['Date']] = v
                _classified_income_totals.store(v)
        _values = []
        for k in d_values.sortedKeys():
            v = d_values[k]
            if (isinstance(v,list)):
                for item in v:
                    _values.append(_report_data(item))
            else:
                _values.append(_report_data(v))
        print '\n'.join(_values)
        print '-'*80
        print str(_classified_income_totals)
        _money_sum.store(_classified_income_totals)
        print '='*80
        print ''
        print 'Classified Credit (Refund) Items:'
        d_values = lists.HashedLists()
        for k,v in _classified_refund_credits.iteritems():
            if (isinstance(v,list)):
                for item in v:
                    item['Date'] = normalizeDate(item['Date'])
                    d_values[item['Date']] = item
                    _classified_refund_totals.store(item)
            else:
                v['Date'] = normalizeDate(v['Date'])
                d_values[v['Date']] = v
                _classified_refund_totals.store(v)
        _values = []
        for k in d_values.sortedKeys():
            v = d_values[k]
            if (isinstance(v,list)):
                for item in v:
                    _values.append(_report_data(item))
            else:
                _values.append(_report_data(v))
        print '\n'.join(_values)
        print '-'*80
        print str(_classified_refund_totals)
        _money_sum.store(_classified_refund_totals)
        print '='*80
        print ''

        print '-'*80
        print 'Sum of Classified Credit Items: %s' % str(_money_sum)
        print 'Validated !' if (_money_sum == _classified_credits_totals) else 'Not Validated !'
        print '-'*80
        print '='*80
        print ''

        _debits_by_classification = lists.HashedLists()

        _money_totals_classified_debits = MoneyTracker(reportable_totals_keys)
        _money_totals_debits_by_classification = lists.HashedLists2()
        
        _money_sum_debits_by_classification = MoneyTracker(reportable_totals_keys)

        print 'Classified Debit Items:'
        print str(_classified_debits_totals)
        _keys = list(set(_classified_debits.keys()))
        _keys.sort()
        _numDebits_total = 0
        _isHeaderShown = False
        for k in _keys:
            c = _debit_classifications[k]
            if (not c):
                _msg = 'WARNING: There is no classification for "%s".' % k
                print >>sys.stderr, _msg
                print >>sys.stdout, _msg
            if (_isVerbose):
                if (not _isHeaderShown):
                    print '\t\t%s' % '\t'.join(reportable_keys)
                    _isHeaderShown = True
            for items in _classified_debits[k]:
                if (c):
                    _debits_by_classification[str(c)] = items
                    _money_totals_classified_debits.store(items)
                report_data(k,items,False)
                _numDebits_total += 1
        print ''
        print 'There are a total of "%s" Debit items.' % _numDebits_total
        print '-'*80
        print str(_money_totals_classified_debits)
        print '-'*80
        # +++ here we print out the classified debits by classification
        print ''
        print 'Debits by Classifications:'
        _numCheckDebits_total = 0
        for k,v in _debits_by_classification.iteritems():
            print ''
            print '%s\n' % k
            d_values = lists.HashedLists()
            if (not _money_totals_debits_by_classification[k]):
                _money_totals_debits_by_classification[k] = MoneyTracker(reportable_totals_keys)
            for item in v:
                item['Date'] = normalizeDate(item['Date'])
                d_values[item['Date']] = item
                _money_totals_debits_by_classification[k].store(item)
            _values = []
            for _k in d_values.sortedKeys():
                v = d_values[_k]
                if (isinstance(v,list)):
                    for item in v:
                        _values.append(_report_data(item))
                else:
                    _values.append(_report_data(v))
            print '\n'.join(_values)
            print ''
            print '-'*80
            print '%s :: %s' % (k,str(_money_totals_debits_by_classification[k]))
            print '-'*80
            _money_sum_debits_by_classification.store(_money_totals_debits_by_classification[k])
            _numCheckDebits_total += len(_values)
        print ''
        print 'There are a total of "%s" Debit items by Classification.' % _numCheckDebits_total
        assert _numDebits_total == _numCheckDebits_total, 'Oops, something is wrong because the number of Debits by Classification (%s) does not match the number of Debits (%s).' % (_numCheckDebits_total,_numDebits_total)
        print '-'*80
        print str(_money_sum_debits_by_classification)
        print 'Validated !' if (_money_sum_debits_by_classification == _money_totals_classified_debits) else 'Not Validated !'
        print '-'*80
        if (_isVerbose):
            print '='*80
            print ''
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        print >>sys.stderr, info_string
    pass

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible()

    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--help':'displays this help text.','--verbose':'output more stuff.','--year=?':'[2005,2006,2007]','--source=?':'%s' % _available_sources}
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

    try:
        _isHelp = _argsObj.booleans['isHelp'] if _argsObj.booleans.has_key('isHelp') else False
    except:
        _isHelp = False

    try:
        _isVerbose = _argsObj.booleans['isVerbose'] if _argsObj.booleans.has_key('isVerbose') else False
    except:
        _isVerbose = False

    try:
        _yyyy = int(_argsObj.arguments['year']) if _argsObj.arguments.has_key('year') else 2005
        k = [s for s in args.keys() if s.find('--year') > -1]
        possible_years = []
        if (len(k) > 0):
            try:
                possible_years = eval(args[k[0]])
            except:
                pass
        _yyyy = _yyyy if _yyyy in possible_years else 2005
        pass
    except:
        _yyyy = 2005

    try:
        _source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else _available_sources[0][-1]
        k = [s for s in args.keys() if s.find('--source') > -1]
        possible_sources = []
        if (len(k) > 0):
            try:
                possible_sources = eval(args[k[0]])
            except:
                pass
        _source = _source if _source in possible_sources else _available_sources[0][-1]
        pass
    except:
        _source = _available_sources[0][-1]

    if (_utils.getVersionNumber() >= 251):
        if (_isHelp):
            ppArgs()
        else:
            if (_source == 'wellsfargo'):
                main_wellsfargo()
            elif (_source == 'paypal'):
                main_paypal()
            else:
                print 'Unable to determine which database to use...'
    else:
        print 'You seem to be using the wrong version of Python, try using 2.5.1 rather than "%s".' % sys.version.split()[0]
