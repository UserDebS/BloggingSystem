def DataCorrection(inputString : str) -> str:
    outputString = ''
    for i in inputString.lower():
        if(i.isalpha()):
            outputString += i

        else:
            if(outputString[-1] != '_'):
                outputString += '_'

    return outputString

if __name__ == '__main__':
    print(DataCorrection('hello & bye'))