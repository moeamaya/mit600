# Problem Set 1C
# Name: Jorge Amaya
# Collaborators: None
# Time Spent: 2:30

def test(initialBalance, interest, pay):
    """solves for final balance with a varying input of
    payment values"""

    #resets balance and month
    balance = initialBalance
    month = 0
    
    while month < 12:
        balance = ((balance*(1+interest))-pay)
        month += 1
    return balance

#constants
initialBalance = float(raw_input("Enter the outstanding balance on your credit card: "))
interestRate = float(raw_input("Enter the annual credit card interest as a decimal: "))
interest = interestRate/12
epsilon = 0.000001

#variable values
low = initialBalance/12
high = (initialBalance*(1+interest)**12)/12
pay = (high + low)/2.0

#loop to find payment value within epsilon
while abs(test(initialBalance,interest,pay)) > epsilon:
    if test(initialBalance, interest, pay) > 0:
        low = pay
    else:
        high = pay
    pay = (high + low)/2.0

#run loop again to find which month debt is less than or equal to 0
month = 0
balance = initialBalance
while balance >= 0:
    balance = ((balance*interest)+balance)-pay
    month += 1

print ' '
print 'RESULT'
print 'Monthly payment to pay off debt in 1 year: $%f' % round(pay,2)
print 'Number of months needed: %d' % month
print 'Balance: %f' % round(balance,2)
