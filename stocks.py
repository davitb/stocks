# - ISO - 14.144 - possibility of long-term cap gain (2 years from grant and 1 year from exercise)
# - NSO - 19.856, no possibility

import datetime
import json

def loadJSONFromFile(filePath):
    with open(filePath) as config:
        obj = json.load(config)
    return obj

def qualifiesForLTCG(stock):
    grantDate = getDate(stock['grant_date'])

    if diffMonth(datetime.date.today(), grantDate) > 12:
        return True
    return False

def getDate(strDate):
    return datetime.datetime.strptime(strDate, '%Y-%m-%d').date()

def diffMonth(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def getVested(stock, futureDate):

    grantDate = getDate(stock['grant_date'])

    diff = diffMonth(futureDate, grantDate)
    if diff < 0:
        return 0

    potential = int(stock['count'] / stock['vesting_period'] * diff)
    if potential > stock['count']:
        potential = stock['count']
    return potential


def doExercise(stocks, exercise):
    eStock = exercise['stocks']
    stock = [i for i in stocks if i['type'] == eStock['type'] ][0]

    eDate = datetime.date.today()
    if "date" in exercise:
        eDate = getDate(exercise['date'])

    vested = eStock['count']
    if type(eStock['count']) is unicode:
        vested = getVested(stock, eDate)

    payRightWay = vested * stock['strike_price']
    taxRate = 40
    if stock['type'] == "ISO" and qualifiesForLTCG(stock):
        taxRate = 15
    payFiscalTax = (exercise['price'] - stock['strike_price']) * vested * taxRate / 100

    valueAtThatMoment = exercise['price'] * vested

    print "Scenario: " + exercise['name']
    print "vested: " + str(vested)
    print "price: " + str(exercise['price'])
    print "payRightWay: " + str(payRightWay)
    print "payFiscalTax: " + str(payFiscalTax)
    print "payOverall: " + str(payRightWay + payFiscalTax) 
    # print "valueAtThatMoment: " + str(valueAtThatMoment) 
    print ""

def doSell(stocks, sell):
    finalCash = 0
    isoVested = 0
    nsoVested = 0

    for stock in stocks:
        sDate = datetime.date.today()
        if "date" in sell:
            sDate = getDate(sell['date'])

        vested = getVested(stock, sDate)
        if stock['type'] == "ISO":
            isoVested += vested

        if stock['type'] == "NSO":
            nsoVested += vested

        finalCash += sell['price'] * vested

    print "Scenario: " + sell['name']
    print "ISO sold: " + str(isoVested)
    print "NSO sold: " + str(nsoVested)
    print "price: " + str(sell['price'])
    print "cash: " + str(finalCash) 
    print ""

def exerciseAllScenarios(config):
    print "EXERCISE SCENARIOS"
    print "-------------------------------------------"
    for e in config['exercise']:
        doExercise(config['stocks'], e)

def sellAllScenarios(config):
    print "SELL SCENARIOS"
    print "-------------------------------------------"
    for e in config['sell']:
        doSell(config['stocks'], e)

config = loadJSONFromFile('config.json')

exerciseAllScenarios(config)
sellAllScenarios(config)
