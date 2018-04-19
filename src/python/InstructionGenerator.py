from random import randint
import os
twoExp15 = 32768
twoExp15MinusOne = 32767
negativeTwoExp15 = -32768

INSTRUCTION_PATH = "lib/Instructions.bin"
PARAM_PATH = "lib/Parameters.txt"
INST_LIST_PATH = "lib/InstructionList.txt"
#######################################################################################
#get the parameters (only instruction count for now)
def getParameters():
  myParameters = ''
  open_Parameters = open(PARAM_PATH,'r')
  for item in open_Parameters:
    equalsSign = item.find('=')
    myLine = item[equalsSign+1:]
    if myParameters == '':
      myParameters = myLine
    else:
      myParameters = myParameters + "," + myLine
  open_Parameters.close()
  return myParameters
#end getParameters
#######################################################################################
def getInstructions():
  myInstructions = ''
  open_file = open(INST_LIST_PATH,'r')
  for line in open_file:
    if myInstructions == '':
      myInstructions = line
    else:
      myInstructions = myInstructions + ',' + line    
  open_file.close()
  return myInstructions
#######################################################################################
def convertBinary(n):
  result = ''  
  for x in range(16): #16 bits
    r = n % 2  #modulus division
    n = n // 2 #floor division
    result += str(r)
  result = result[::-1] #reverse the order
  return result
#######################################################################################
def complementConverter(n):
  binary = convertBinary(n)
  #print(str(binary))
  return binary
#######################################################################################
def rFormat(myInt,myArray,myLowerRegister,myUpperRegister):
  lowerShiftBound = 0
  upperShiftBound = 31
  myBin = ''
  for i in range(0,len(myArray),5):
    #print("ARRAY: " + myArray[i])
    if myArray[i] == str(myInt):
      print("R-Format Instruction: " + myArray[i])
      opCode = myArray[i+1]
      shiftAmt = myArray[i+2]
      if shiftAmt == '':
        shifter = randint(lowerShiftBound,upperShiftBound) #a0 - t9
        shiftAmt = '{0:05b}'.format(shifter)
      funct = myArray[i+3]
      myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
      myRs = '{0:05b}'.format(myRandInt)
      myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
      myRt = '{0:05b}'.format(myRandInt)
      myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
      myRd = '{0:05b}'.format(myRandInt)
      myBin = opCode + myRs + myRt + myRd + shiftAmt + funct
      break
  return myBin
#######################################################################################
def immediateFormat(myInt,myArray,myLowerRegister,myUpperRegister):
  myImm = ''
  myBin = ''
  for i in range(0,len(myArray),5):
    #print("ARRAY: " + myArray[i])
    if myArray[i] == str(myInt):
      print("I-Format Instruction: " + myArray[i])
      opCode = myArray[i+1]
      shiftAmt = myArray[i+2]
      funct = myArray[i+3]
      myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
      myRs = '{0:05b}'.format(myRandInt)
      myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
      myRt = '{0:05b}'.format(myRandInt)
      if myArray[i] == '8' or myArray[i] == '9':
        #myRandInt = randint(0,32768) #range from 0 - 32768 2^15
        myRandInt = randint(0,twoExp15)
        myImm = '{0:16b}'.format(myRandInt).strip()
        myImm = myImm.zfill(16)
      elif myArray[i] == '10' or myArray[i] == '11':
        #myRandInt = randint(-32768,32767) #2^15 signed range
        myRandInt = randint(negativeTwoExp15,twoExp15MinusOne)  
        #myRandInt = randint(-10,10) #2^15 signed range
        print("IMM VALUE: " + str(myRandInt))
        if myRandInt < 0:
          myImm = complementConverter(myRandInt)
        else:
          myBin = bin(myRandInt)
          myBin = myBin[2:]
          myImm = myBin.zfill(16)
      myBin = opCode + myRs + myRt + myImm
      break
  return myBin
#######################################################################################
def jumpFormat(myInt,myArray,myLowerRegister,myUpperRegister):
  lowerBound = -32
  upperBound = 32
  jrFunct = '000000'
  jrConst = '000000000000000'
  myBin = ''
  for i in range(0,len(myArray),5):
    #print("ARRAY: " + myArray[i])
    if myArray[i] == str(myInt):
      print("J-Format Instruction: " + myArray[i])
      if myArray[i] == '12':
        opCode = myArray[i+1]
        myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
        myRs = '{0:05b}'.format(myRandInt)
        myRandInt = randint(myLowerRegister,myUpperRegister) #a0 - t9
        myRt = '{0:05b}'.format(myRandInt)
        #myRandInt = randint(-32,32) #-128 to 128 range in bytes.  The branch immediate value represents words
        myRandInt = randint(lowerBound,upperBound)
        if myRandInt < 0:
          myImm = complementConverter(myRandInt)
        else:
          myBin = bin(myRandInt)
          myBin = myBin[2:]
          myImm = myBin.zfill(16)
        myBin = opCode + myRs + myRt + myImm
      elif myArray[i] == '13' or myArray[i] == '14':
        opCode = myArray[i+1]
        myRandInt = randint(0,1000000) #0 - 1 million. This can be increased to accommodate a larger instruction count
        myRandInt = myRandInt / 4
        myJmp = '{0:20b}'.format(myRandInt).strip()
        myJmp = myJmp.zfill(32)
        myJmp = myJmp[4:]
        myJmp = myJmp[:-2]
        myBin = opCode + myJmp
      elif myArray[i] == '15':
        opCode = myArray[i+1]
        myRandInt = randint(myLowerRegister,myUpperRegister) #Do we want this to be $ra all the time or random using all the available registers from $4 - $25?
        myRs = '{0:05b}'.format(myRandInt)
        myBin = opCode + myRs + jrConst + jrFunct
      break
  return myBin
#######################################################################################
def deleteInstructionFile():
  if os.path.exists(INSTRUCTION_PATH):
    os.remove(INSTRUCTION_PATH)
  return
#######################################################################################
def createInstructionsFile():
  file = open(INSTRUCTION_PATH,'w')
  file.close()
  return
#######################################################################################
def writeInstructions(myArray):
  import random
  file = open(INSTRUCTION_PATH,'a')
  instructionArray = myArray.split(',')
  random.shuffle(instructionArray)
  for i in range(0,len(instructionArray)):
   file.write(instructionArray[i])
   if i < (len(instructionArray) - 1):
     file.write('\n')
  file.close()
  return
#######################################################################################
def driver():
  lowerRegister = 0
  upperRegister = 25
  nonBranchInstructions = ''
  branchInstructions = ''
  deleteInstructionFile()
  createInstructionsFile()
  inputArray = getParameters()
  parameterArray = inputArray.split(',')
  totalInstructions = parameterArray[0]
  branchFrequency = int(parameterArray[1]) / 100.0
  dataDependency = int(parameterArray[2]) / 100.0
  if dataDependency == 0.0:
    lowerRegister = 4
  elif dataDependency == 0.25:
    lowerRegister = 9
  elif dataDependency == 0.5:
    lowerRegister = 13
  elif dataDependency == 0.75:
    lowerRegister = 17
  elif dataDependency == 1.0:
    lowerRegister = 21
  print("DATA DEPENDENCY: " + str(dataDependency))
  print("LOWER REGISTER: " + str(lowerRegister))
  print("BRANCH FREQUENCY: " + str(branchFrequency))
  numberOfBranchInstructions = int(int(totalInstructions) * float(branchFrequency))
  numberOfInstructions = int(totalInstructions) - int(numberOfBranchInstructions)
  print("# Branch Instructions: " + str(numberOfBranchInstructions))
  instrString = getInstructions()
  convertedToInstArray = instrString.split(',')
  myRandInt = 0
  for x in range(0,int(numberOfInstructions)):
    myRandInt = randint(1,11)
    if myRandInt == 1 or myRandInt == 2 or myRandInt == 3 or myRandInt == 4 or myRandInt == 5 or myRandInt == 6 or myRandInt == 7:
      #call the R-format function
      myInstruction = rFormat(myRandInt,convertedToInstArray,lowerRegister,upperRegister)
      if nonBranchInstructions == '':
        nonBranchInstructions = myInstruction
      else:
        nonBranchInstructions = nonBranchInstructions + "," + myInstruction
      print(myInstruction)
    elif myRandInt == 8 or myRandInt == 9 or myRandInt == 10 or myRandInt == 11:
      myInstruction = immediateFormat(myRandInt,convertedToInstArray,lowerRegister,upperRegister)
      if nonBranchInstructions == '':
        nonBranchInstructions = myInstruction
      else:
        nonBranchInstructions = nonBranchInstructions + "," + myInstruction
      print(myInstruction)

  for x in range(0,int(numberOfBranchInstructions)):
    myRandInt = randint(12,15)
    if myRandInt == 12 or myRandInt == 13 or myRandInt == 14 or myRandInt == 15:
      myInstruction = jumpFormat(myRandInt,convertedToInstArray,lowerRegister,upperRegister)
      if branchInstructions == '':
        branchInstructions = myInstruction
      else:
        branchInstructions = branchInstructions + "," + myInstruction
      print(myInstruction)
  instructionList = nonBranchInstructions + "," + branchInstructions
  writeInstructions(instructionList)
  return
#######################################################################################
driver()



