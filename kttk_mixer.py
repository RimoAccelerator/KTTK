import os, sys, re, numpy

class FchkInfo(object):
	def __init__(self):
		self.NumberOfAtoms = 0
		self.Charge = -114514
		self.Multiplicity = 114514
		self.NumberOfElectrons = 0
		self.NumberOfAlphaElectrons = 0
		self.NumberOfBetaElectrons = 0
		self.NumberOfBasisFunctions = 0
		self.AtomicNumbers = []
		self.NuclearCharges = []
		self.CurrentCartesianCoordinates = []
		self.NumberOfContractedShells = 0
		self.NumberOfPrimitiveShells = 0
		self.Pure_CartesianDShells = 0
		self.Pure_CartesianFShells = 0
		self.HighestAngularMomentum = 0
		self.LargestDegreeOfContraction = 0
		self.ShellTypes = []
		self.NumberOfPrimitivesPerShell = []
		self.ShellToAtomMap = []
		self.PrimitiveExponents = []
		self.ContractionCoefficients = []
		self.AlphaMOCoefficients = []
		self.BetaMOCoefficients = []
		self.GaussianVersion = 'ES64L-G16RevC.01'
		self.NumberOfContractedFunctions = 0
		self.PSPContractionCoefficients = []

	def calcNumberOfContractedFunctions(self):
		self.NumberOfContractedFunctions = 0
		mapping = {
		0: 1,
		1: 3,
		-1: 4,
		2: 6,
		-2: 5,
		3: 10,
		-3: 7,
		4: 15,
		-4: 9
		} # 1-s, 2-p, -2-sp, 2-6d, -2-5d, 3-10f, -3-7f, 4-15g, -4-9g
		for i in range(self.NumberOfContractedShells):
			self.NumberOfContractedFunctions += mapping[self.ShellTypes[i]]

def readFchk(path):
	fchk = FchkInfo()
	with open(path) as f:
		for l in f:
			if not re.match('^\s*\-?\d+', l):
				isAtomicNumbers = False
				isNuclearCharges = False
				isCurrentCartesianCoordinates = False
				isShellTypes = False
				isShellToAtomMap = False
				isPrimitiveExponents = False
				isContractionCoefficients = False
				isAlphaMOCoefficients = False
				isBetaMOCoefficients = False
				isNumberOfPrimitivesPerShell = False
				isPSPContractionCoefficients = False

			if fchk.NumberOfAtoms == 0 and 'Number of atoms' in l:
				fchk.NumberOfAtoms = int(l.split()[-1])
			elif fchk.Charge == -114514 and 'Charge' in l:
				fchk.Charge = int(l.split()[-1])
			elif fchk.Multiplicity == 114514 and 'Multiplicity' in l:
				fchk.Multiplicity = int(l.split()[-1])
			elif fchk.NumberOfElectrons == 0 and 'Number of electrons' in l:
				fchk.NumberOfElectrons = int(l.split()[-1])
			elif fchk.NumberOfAlphaElectrons == 0 and 'Number of alpha electrons' in l:
				fchk.NumberOfAlphaElectrons = int(l.split()[-1])
			elif fchk.NumberOfBetaElectrons == 0 and 'Number of beta electrons' in l:
				fchk.NumberOfBetaElectrons = int(l.split()[-1])
			elif fchk.NumberOfBasisFunctions == 0 and 'Number of basis functions' in l:
				fchk.NumberOfBasisFunctions = int(l.split()[-1])
			elif fchk.NumberOfContractedShells == 0 and 'Number of contracted shells' in l:
				fchk.NumberOfContractedShells = int(l.split()[-1])
			elif fchk.NumberOfPrimitiveShells == 0 and 'Number of primitive shells' in l:
				fchk.NumberOfPrimitiveShells = int(l.split()[-1])
			elif 'Pure/Cartesian d shells' in l:
				fchk.Pure_CartesianDShells = int(l.split()[-1])
			elif 'Pure/Cartesian f shells' in l:
				fchk.Pure_CartesianFShells = int(l.split()[-1])
			elif 'Highest angular momentum' in l:
				fchk.HighestAngularMomentum = int(l.split()[-1])
			elif 'Largest degree of contraction' in l:
				fchk.LargestDegreeOfContraction = int(l.split()[-1])
			elif 'Atomic numbers' in l:
				isAtomicNumbers = True
			elif 'Nuclear charges' in l:
				isNuclearCharges = True
			elif 'Current cartesian coordinates' in l:
				isCurrentCartesianCoordinates = True
			elif 'Shell types' in l:
				isShellTypes = True
			elif 'Number of primitives per shell' in l:
				isNumberOfPrimitivesPerShell = True
			elif 'Shell to atom map' in l:
				isShellToAtomMap = True
			elif 'Primitive exponents' in l:
				isPrimitiveExponents = True
			elif 'P(S=P) Contraction coefficients' in l:
				isPSPContractionCoefficients = True
			elif 'Contraction coefficients' in l:
				isContractionCoefficients = True
			elif 'Alpha MO coefficients' in l:
				isAlphaMOCoefficients = True
			elif 'Beta MO coefficients' in l:
				isBetaMOCoefficients = True

			
			if re.match('^\s*\-?\d+', l):
				lSplitted = [float(i) for i in l.split()]
				lSplittedInt = [int(i) for i in lSplitted]
				if isAtomicNumbers:
					fchk.AtomicNumbers.extend(lSplittedInt)
				elif isNuclearCharges:
					fchk.NuclearCharges.extend(lSplitted)
				elif isCurrentCartesianCoordinates:
					fchk.CurrentCartesianCoordinates.extend(lSplitted)
				elif isShellTypes:
					fchk.ShellTypes.extend(lSplittedInt)
				elif isShellToAtomMap:
					fchk.ShellToAtomMap.extend(lSplittedInt)
				elif isPrimitiveExponents:
					fchk.PrimitiveExponents.extend(lSplitted)
				elif isContractionCoefficients:
					fchk.ContractionCoefficients.extend(lSplitted)
				elif isPSPContractionCoefficients:
					fchk.PSPContractionCoefficients.extend(lSplitted)
				elif isAlphaMOCoefficients:
					fchk.AlphaMOCoefficients.extend(lSplitted)
				elif isBetaMOCoefficients:
					fchk.BetaMOCoefficients.extend(lSplitted)
				elif isNumberOfPrimitivesPerShell:
					fchk.NumberOfPrimitivesPerShell.extend(lSplittedInt)
	if len(fchk.PSPContractionCoefficients) == 0:
		for i in fchk.ContractionCoefficients:
			fchk.PSPContractionCoefficients.append(0)
	fchk.calcNumberOfContractedFunctions()
	return fchk


def mixFchks(fchks, flipSigns): # flipSigns: [1, -1, ...] -1 to flip
	i = 0
	outFchk = FchkInfo()
	outFchk.Charge = 0
	outFchk.Multiplicity = 0
	for fchk in fchks:
		outFchk.Charge += fchk.Charge
		outFchk.Multiplicity += (fchk.Multiplicity - 1) * flipSigns[i] 
		#now it means the number of unpaired electrons
		outFchk.NumberOfAtoms += fchk.NumberOfAtoms
		outFchk.NumberOfElectrons += fchk.NumberOfElectrons
		outFchk.NumberOfBasisFunctions += fchk.NumberOfBasisFunctions
		outFchk.NumberOfContractedShells += fchk.NumberOfContractedShells
		outFchk.NumberOfPrimitiveShells += fchk.NumberOfPrimitiveShells
		outFchk.Pure_CartesianDShells = fchk.Pure_CartesianDShells
		outFchk.Pure_CartesianFShells = fchk.Pure_CartesianFShells

		if outFchk.HighestAngularMomentum < fchk.HighestAngularMomentum:
			outFchk.HighestAngularMomentum = fchk.HighestAngularMomentum
		if outFchk.LargestDegreeOfContraction < fchk.LargestDegreeOfContraction:
			outFchk.LargestDegreeOfContraction = fchk.LargestDegreeOfContraction
		outFchk.ShellTypes.extend(fchk.ShellTypes)

		previousAtomicNumbers = len(outFchk.AtomicNumbers)
		outFchk.ShellToAtomMap.extend([i + previousAtomicNumbers for i in fchk.ShellToAtomMap])

		outFchk.AtomicNumbers.extend(fchk.AtomicNumbers)
		outFchk.NuclearCharges.extend(fchk.NuclearCharges)
		outFchk.CurrentCartesianCoordinates.extend(fchk.CurrentCartesianCoordinates)
		outFchk.NumberOfPrimitivesPerShell.extend(fchk.NumberOfPrimitivesPerShell)
		outFchk.PrimitiveExponents.extend(fchk.PrimitiveExponents)
		outFchk.ContractionCoefficients.extend(fchk.ContractionCoefficients)
		outFchk.PSPContractionCoefficients.extend(fchk.PSPContractionCoefficients)
		i += 1

	outFchk.Multiplicity += 1
	outFchk.calcNumberOfContractedFunctions()

	#print('outFchk.NumberOfContractedFunctions')
	#print(outFchk.NumberOfContractedFunctions)

	alphaMOMixedOcc = numpy.zeros((outFchk.NumberOfContractedFunctions, 1))
	alphaMOMixedVir = numpy.zeros((outFchk.NumberOfContractedFunctions, 1))
	betaMOMixedOcc = numpy.zeros((outFchk.NumberOfContractedFunctions, 1))
	betaMOMixedVir = numpy.zeros((outFchk.NumberOfContractedFunctions, 1))

	#create a matrix with a rubbish column, which will be removed at the end
	i = 0
	previousContractedIndex = 0 # Record where the fragment orbital should be inserted
	for fchk in fchks:
		if len(fchk.BetaMOCoefficients) == 0:
			fchk.BetaMOCoefficients = fchk.AlphaMOCoefficients[:]
		#copy the alpha MO to beta in case of an RHF calculation
		numberOfAlphaElectrons = 0
		numberOfBetaElectrons = 0
		if flipSigns[i] == 1:
			numberOfAlphaElectrons = fchk.NumberOfAlphaElectrons
			numberOfBetaElectrons = fchk.NumberOfBetaElectrons
			#print("len(fchk.AlphaMOCoefficients)")
			#print(len(fchk.AlphaMOCoefficients))
			#print("fchk.NumberOfContractedShells")
			#print(fchk.NumberOfContractedShells)
			#print("fchk.NumberOfContractedFunctions")
			#print(fchk.NumberOfContractedFunctions)
			alphaMOs = numpy.array(fchk.AlphaMOCoefficients).reshape((
				fchk.NumberOfContractedFunctions, fchk.NumberOfContractedFunctions)).T
			betaMOs = numpy.array(fchk.BetaMOCoefficients).reshape((
				fchk.NumberOfContractedFunctions, fchk.NumberOfContractedFunctions)).T
		elif flipSigns[i] == -1: #swap both the orbital and the electron number
			numberOfAlphaElectrons = fchk.NumberOfBetaElectrons
			numberOfBetaElectrons = fchk.NumberOfAlphaElectrons
			betaMOs = numpy.array(fchk.AlphaMOCoefficients).reshape((
				fchk.NumberOfContractedFunctions, fchk.NumberOfContractedFunctions)).T
			alphaMOs = numpy.array(fchk.BetaMOCoefficients).reshape((
				fchk.NumberOfContractedFunctions, fchk.NumberOfContractedFunctions)).T
		outFchk.NumberOfAlphaElectrons += numberOfAlphaElectrons
		outFchk.NumberOfBetaElectrons += numberOfBetaElectrons
		
		#print('alphaMOs.shape')
		#print(alphaMOs.shape)

		thisAlphaOcc = alphaMOs[:,0:numberOfAlphaElectrons]

		thisAlphaVir = alphaMOs[:,numberOfAlphaElectrons:]
		
		thisBetaOcc = betaMOs[:,0:numberOfBetaElectrons]
		thisBetaVir = betaMOs[:,numberOfBetaElectrons:]

		#print('alphaMOs')
		#print(alphaMOs)
		#print('thisAlphaOcc')
		#print(thisAlphaOcc)
		#print('thisAlphaVir')
		#print(thisAlphaVir)
		#print('betaMOs')
		#print(betaMOs)
		#print('thisBetaOcc')
		#print(thisBetaOcc)
		#print('thisBetaVir')
		#print(thisBetaVir)

		zerosAlphaBefore = numpy.zeros((previousContractedIndex, numberOfAlphaElectrons))
		zerosAlphaAfter = numpy.zeros((
			outFchk.NumberOfContractedFunctions - previousContractedIndex - fchk.NumberOfContractedFunctions,
			numberOfAlphaElectrons))
		zerosBetaBefore = numpy.zeros((previousContractedIndex, numberOfBetaElectrons))
		zerosBetaAfter = numpy.zeros((
			outFchk.NumberOfContractedFunctions - previousContractedIndex - fchk.NumberOfContractedFunctions,
			numberOfBetaElectrons))

		#print('shapes')
		#print(zerosAlphaBefore.shape)
		#print(thisAlphaOcc.shape)
		#print(zerosAlphaAfter.shape)
		#print(alphaMOMixedOcc.shape)

		alphaMOMixedOcc = numpy.append(alphaMOMixedOcc, numpy.block([
			[zerosAlphaBefore],
			[thisAlphaOcc],
			[zerosAlphaAfter]
			]), axis = 1)
		betaMOMixedOcc = numpy.append(betaMOMixedOcc, numpy.block([
			[zerosBetaBefore],
			[thisBetaOcc],
			[zerosBetaAfter]
			]), axis = 1)
		#print('alphaMOMixedOcc')
		#print(alphaMOMixedOcc)
		#print('betaMOMixedOcc')
		#print(betaMOMixedOcc)

		
		zerosAlphaBefore = numpy.zeros((previousContractedIndex, 
			fchk.NumberOfContractedFunctions - numberOfAlphaElectrons))
		zerosAlphaAfter = numpy.zeros((
			outFchk.NumberOfContractedFunctions - previousContractedIndex - fchk.NumberOfContractedFunctions,
			fchk.NumberOfContractedFunctions - numberOfAlphaElectrons))
		zerosBetaBefore = numpy.zeros((previousContractedIndex, 
			fchk.NumberOfContractedFunctions - numberOfBetaElectrons))
		zerosBetaAfter = numpy.zeros((
			outFchk.NumberOfContractedFunctions - previousContractedIndex - fchk.NumberOfContractedFunctions,
			fchk.NumberOfContractedFunctions - numberOfBetaElectrons))
		#print('zerosAlphaBefore')
		#print(zerosAlphaBefore)
		#print('zerosAlphaAfter')
		#print(zerosAlphaAfter)
		#print('zerosBetaBefore')
		#print(zerosBetaBefore)
		#print('zerosBetaAfter')
		#print(zerosBetaAfter)
		alphaMOMixedVir = numpy.append(alphaMOMixedVir, numpy.block([
			[zerosAlphaBefore],
			[thisAlphaVir],
			[zerosAlphaAfter]
			]), axis = 1)
		betaMOMixedVir = numpy.append(betaMOMixedVir, numpy.block([
			[zerosBetaBefore],
			[thisBetaVir],
			[zerosBetaAfter]
			]), axis = 1)

		#print('betaMOMixedVir')
		#print(alphaMOMixedVir)
		#print('alphaMOMixedVir')
		#print(alphaMOMixedVir)

		previousContractedIndex += fchk.NumberOfContractedFunctions

	outFchk.AlphaMOCoefficients = numpy.append(
		numpy.delete(alphaMOMixedOcc, 0, 1), numpy.delete(alphaMOMixedVir, 0, 1), axis = 1
		).T.flatten()
	outFchk.BetaMOCoefficients = numpy.append(
		numpy.delete(betaMOMixedOcc, 0, 1), numpy.delete(betaMOMixedVir, 0, 1), axis = 1
		).T.flatten()
	return outFchk
	
def outputList(list):
	i = 0
	output = ''
	for num in list:
		i += 1
		if i == 6:
			output += '\n'
			i = 1
		output += str(format(num, '16.8E'))
	return output

def outputListInt(list):
	i = 0
	output = ''
	for num in list:
		i += 1
		if i == 7:
			output += '\n'
			i = 1
		output += str(format(int(num), '12'))
	return output

def buildFchk(fchk, path):
	output = f'Title Card Required\n\
SP        UHF  GENECP\n\
Number of atoms                            I     {fchk.NumberOfAtoms:12d}\n\
Charge                                     I     {fchk.Charge:12d}\n\
Multiplicity                               I     {fchk.Multiplicity:12d}\n\
Number of electrons                        I     {fchk.NumberOfElectrons:12d}\n\
Number of alpha electrons                  I     {fchk.NumberOfAlphaElectrons:12d}\n\
Number of beta electrons                   I     {fchk.NumberOfBetaElectrons:12d}\n\
Number of basis functions                  I     {fchk.NumberOfBasisFunctions:12d}\n\
Atomic numbers                             I   N={len(fchk.AtomicNumbers):12d}\n\
{outputListInt(fchk.AtomicNumbers)}\n\
Nuclear charges                            R   N={len(fchk.NuclearCharges):12d}\n\
{outputList(fchk.NuclearCharges)}\n\
Current cartesian coordinates              R   N={len(fchk.CurrentCartesianCoordinates):12d}\n\
{outputList(fchk.CurrentCartesianCoordinates)}\n\
Number of contracted shells                I     {fchk.NumberOfContractedShells:12d}\n\
Number of primitive shells                 I     {fchk.NumberOfPrimitiveShells:12d}\n\
Pure/Cartesian d shells                    I     {fchk.Pure_CartesianDShells:12d}\n\
Pure/Cartesian f shells                    I     {fchk.Pure_CartesianFShells:12d}\n\
Highest angular momentum                   I     {fchk.HighestAngularMomentum:12d}\n\
Largest degree of contraction              I     {fchk.LargestDegreeOfContraction:12d}\n\
Shell types                                I   N={len(fchk.ShellTypes):12d}\n\
{outputListInt(fchk.ShellTypes)}\n\
Number of primitives per shell             I   N={len(fchk.NumberOfPrimitivesPerShell):12d}\n\
{outputListInt(fchk.NumberOfPrimitivesPerShell)}\n\
Shell to atom map                          I   N={len(fchk.ShellToAtomMap):12d}\n\
{outputListInt(fchk.ShellToAtomMap)}\n\
Primitive exponents                        R   N={len(fchk.PrimitiveExponents):12d}\n\
{outputList(fchk.PrimitiveExponents)}\n\
Contraction coefficients                   R   N={len(fchk.ContractionCoefficients):12d}\n\
{outputList(fchk.ContractionCoefficients)}\n\
P(S=P) Contraction coefficients            R   N={len(fchk.PSPContractionCoefficients):12d}\n\
{outputList(fchk.PSPContractionCoefficients)}\n\
Num ILSW                                   I                1\n\
ILSW                                       I   N=           1\n\
           1\n\
Alpha Orbital Energies                     R   N={fchk.NumberOfContractedFunctions:12d}\n\
{outputList(range(fchk.NumberOfContractedFunctions))}\n\
Beta Orbital Energies                      R   N={fchk.NumberOfContractedFunctions:12d}\n\
{outputList(range(fchk.NumberOfContractedFunctions))}\n\
Alpha MO coefficients                      R   N={len(fchk.AlphaMOCoefficients):12d}\n\
{outputList(fchk.AlphaMOCoefficients)}\n\
Beta MO coefficients                       R   N={len(fchk.BetaMOCoefficients):12d}\n\
{outputList(fchk.BetaMOCoefficients)}\n\
Gaussian Version                           C   N=2\n\
ES64L-G16RevC.01'
	f = open(path, 'w')
	f.write(output)
	f.close()

if __name__ == '__main__':
	print('Input the fragment fchk files, and an empty line to end the input.')
	fchks = []
	while True:
		path = input()
		if path.strip() == '':
			break
		fchks.append(readFchk(path))
	print('Input the flag (1 or -1) for each fragment, respectively. -1 to flip the spin. E.g. 1 -1 1')
	flags = [int(i) for i in input().split()]
	outfchk = mixFchks(fchks, flags)
	outpath = input('Where to save the output fchk file? ')
	buildFchk(outfchk, outpath)