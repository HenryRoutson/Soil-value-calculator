import numpy as np

SpaceConv = 1000000

"Create scaleable conversion ratios"
Conversions = [0.001,1,1000,1000000,SpaceConv*1,SpaceConv*10000]

ConversionNames = ["mg","g","kg","t","sqm","ha"]

"Create functions" 
# Convert Input values to new form
def ToNew(Input,Output):
    # Create conversion ratios
    for x in range(len(ConversionNames)): 

        if ConversionNames[x] == Input[1]:
            Output[0] = Output[0]*Conversions[x]

        if ConversionNames[x] == Output[1]:
            Output[0] = Output[0]/Conversions[x] 

    print(Output[0],Output[1],"equals 1",Input[1])  
    # Multiply by input scale
    Output[0] = Output[0] * Input[0]

# Simplify ratio 
def Normalise(List):
    List[0][0] = float(List[0][0]/ List[1][0])
    List[1][0] = 1

while True:
    "Take Inputs"
    # Example values
    Input = [[10, "kg"],[1, "ha"]]
    Output = [[1,"kg"],[1,"sqm"]]

    # # Input Values
    #Input = [[float(input()), input()],[float(input()), input()]]
    #Output = [[1,input()],[1,input()]]
    #sqm = input("sqm weight in g")

    "Execute functions"
    print(Input)
    ToNew(Input[0],Output[0])
    ToNew(Input[1],Output[1])
    print(Output)
    print("Simplifies to")
    Normalise(Output) 
    print(Output)
    input("Press enter to continue")


"""Pint python libary can also be used"""