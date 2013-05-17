# Problem Set 1B
# Name: Jorge Amaya
# Collaborators: None
# Time Spent: 1:30

#constants
initialBalance = float(raw_input("Enter the outstanding balance on your credit card: "))
interestRate = float(raw_input("Enter the annual credit card interest as a decimal: "))
monthlyInterest = interestRate/12

#variables
pay = 0
balance = initialBalance
month = 0

#loop to search for correct multiple of $10 payment
while balance >= 0:
    pay += 10
    #resets balance to original balance
    balance = initialBalance
    month = 0
    
    #loop that runs for a 12-month period
    while month<12:
        month += 1
        balance = ((1+monthlyInterest)*balance)-pay
        
  

#run loop again to find which month debt is less than or equal to 0
month = 0
balance = initialBalance
while balance >= 0:
    balance = ((balance*monthlyInterest)+balance)-pay
    month += 1


print ' '
print 'RESULT'
print 'Monthly payment to pay off debt in 1 year: $%d' % pay
print 'Number of months needed: %d' % month
print 'Balance: %g' % round(balance,2)
