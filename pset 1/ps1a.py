# Problem Set 1A
# Name: Jorge Amaya
# Collaborators: None
# Time Spent: 1:00

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
interestRate = float(raw_input("Enter the annual credit card interest as a decimal: "))
monthRate = float(raw_input("Enter the minimum monthly payment rate as a decimal: "))
balanceInitial = balance

x = 1
#while loop for 12 months
while x<13:
    
    #minimum monthly payment
    monthPay = monthRate*balance
    monthRound = round(monthPay,2)

    #interest payment for this month
    interestPaid = (interestRate/12)*balance

    #balance after interest is addded and payment is applied
    balance = (balance+interestPaid)-monthPay
    balanceRound = round(balance,2)
    
    print 'Month: %d' % x
    print 'Minimum monthly payment: %g' % monthRound
    print 'Remaining balance: %g' % balanceRound
    x += 1
    
totalPaid = balanceInitial - balanceRound

print ' '
print 'RESULT'
print 'Total amount paid: %g' % totalPaid
print 'Remaing balance: %g' % balanceRound
