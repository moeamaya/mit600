txtFile = open("ryan.rmtl")
subjectList = []
test = 0
finalValue = 0

for line in txtFile:
    if test > 1:
        break
    else:
        test += 1
        each = line.split('notes')
        try:
            finalValue = each[1]
        except:
            continue

print finalValue.strip('=').strip('"')
