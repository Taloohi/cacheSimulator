#Talha Abdulaziz

import math

offsetBits = 2
hits = 0
misses = 0

cache = []
cycles = 0
writeBack = 0


def bi(x): #Converts decimal to 32 bit binary integer
    #return(bin(x)[2:])
    return("{0:{fill}32b}".format(x, fill='0'))

def dec(x): #Converts binary to a decimal form 
    return(int(str(x),2))


def tagBits(addr,blockBits,rowBits): #Returns tagbits of an address based on block and rowbits
    num = 32 - blockBits - rowBits - 2
    return addr[:num]

def index(addr,blockBits,rowBits):
    tag = 32 - blockBits - rowBits - 2
    return addr[tag:tag+rowBits]

def shift(x):
    return [x[-1]] + x[:-1]

def determineSet(addr,blockBits):
    return((addr>>2)&((2**blockBits)-1))

# of sets = lines/ways = 2**rowbits/associativity 
    
rowbit = int(input("How many rowbit? "))
blockbit = int(input("How many blockbits? "))
associativity = int(input("How much associativity? "))

fileName = (input("Name of MAT? "))

cache = [[0 for x in range(associativity)] for y in range(int((2**rowbit)))]

dirtyArray = [[0 for x in range(associativity)] for y in range(int((2**rowbit)))] #Same size of cache, corresponsing elements are dirty (1) or not (0)

tagbit = 32 - rowbit - blockbit - offsetBits
sizeSRAM = (2**rowbit)*(tagbit + 2 + (2**blockbit)*32)*associativity

count = 0

file = open(fileName,'r')
mat = file.readlines()

for line in mat:


        address = int(line[2:len(line)])
        binAddress = bi(address)
        tag = tagBits(binAddress,blockbit,rowbit)
        row = index(binAddress,blockbit,rowbit)

        
        if line[0] == 'R':
            if(tag in cache[dec(row)]): #Checks the set where the tag belongs based on the index
                hits+=1
                cycles += 1 + (rowbit)/2 + math.log2(associativity) #Cycles required per hit
                    
            else:
                misses +=1
                
                cycles += 20 + 2**blockbit
                
                cache[dec(row)] = shift(cache[dec(row)]) #Shifts all components of the set to the right once
                cache[dec(row)][0] = tag #Replaces the LRU with the new tag, data

                
                
                dirtyArray[dec(row)] = shift(dirtyArray[dec(row)])

                #If miss and the dirty bit needs to be replaced
                if dirtyArray[dec(row)][0] == 1: #If write-back is necessary, there is a delay
                    cycles += 1 + 2**blockbit  #1 cycle for transfer and additional before it can be used again
                    dirtyArray[dec(row)][0] = 0
                    writeBack += 1


        elif line[0] == 'W':
            if(tag in cache[dec(row)]):
                hits+=1
                cycles += 1 + (rowbit)/2 + math.log2(associativity) 
                loc = cache[dec(row)].index(tag)
                dirtyArray[dec(row)][loc] = 1 #Write to cache. This address is now dirty
                

            else:
                misses +=1

                cycles += 20 + 2**blockbit
                
                cache[dec(row)] = shift(cache[dec(row)]) 
                cache[dec(row)][0] = tag

                dirtyArray[dec(row)] = shift(dirtyArray[dec(row)]) #Same LRU process for dirtyArray

                if dirtyArray[dec(row)][0] == 1: #If write-back is necessary, there is a delay
                    cycles += 1 + 2**blockbit
                    writeBack += 1
                
                dirtyArray[dec(row)][0] = 1


print('Total Cycles: ', cycles, '\nRAM size: ', sizeSRAM,  ' \nHits: ', hits, ' \nMisses: ', misses, '\nWrite Backs: ', writeBack)

input("Press Enter to continue...")
        
