import os, sys, re

def writeGjf(path, coords, kwd, core, mem, chargeAndMult, end, chk):
	cont = f'%chk={chk}\n'
	cont += f"%mem={mem}\n%nprocshared={core}\n# {kwd}\n\nTC\n\n{chargeAndMult}\n"
	for c in coords:
		cont += c
		cont += '\n'
	cont += f'\n{end}\n\n'
	f = open(path,"w")
	f.write(cont)
	f.close()

def readGjf(path):  # read the geometry from a gjf
	coords = []
	mem = ''
	nproc = ''
	multAndCharge = ''
	with open(path) as f:
		isCoord = False
		for l in f:
			l = l.strip()
			if '%mem' in l:
				mem = l.split('=')[-1]
			elif '%nproc' in l:
				nproc = l.split('=')[-1]
			if re.match('^\s*\-?\d+\s+\d+\s*$', l):
				multAndCharge = l.strip()
				isCoord = True
			elif isCoord and l.strip() == '':
				isCoord = False
			elif isCoord:
				coords.append(l)
	return [nproc, mem, multAndCharge, coords]

assignedAtoms = [] #recored atoms assigned to fragments

def analyzeFragmentIndex(str, totalAtomNumber): # transform user inputted atom range into a list
	atomRange = []
	if str == 'else': # assign the unassigned atoms
		for i in range(totalAtomNumber):
			if not i in assignedAtoms:
				atomRange.append(i)
	else:
		for i in str.split(','):
			if '-' in i:
				lower, upper = [int(num) for num in i.split('-')]
				atomRange.extend(range(lower - 1, upper))
			else:
				atomRange.append(int(i) - 1)
	assignedAtoms.extend(atomRange)
	return atomRange

def sortCoordinates(allCoords, fragmentIndexes): #rearrange coordinates to follow the order of fragments
#and return the coordinates for each fragment
	fragments = []
	for f in fragmentIndexes:
		thisFragment = []
		for i in f:
			thisFragment.append(allCoords[i])
		fragments.append(thisFragment)
	return fragments

def joinFragments(fragments):
	allCoords = []
	for f in fragments:
		for c in f:
			allCoords.append(c)
	return allCoords

if __name__ == '__main__':
	print('Input the gjf file for your whole molecule:')
	gjf = input()
	nproc, mem, overallMultAndCharge, coords = readGjf(gjf)
	print('Input your atom indexes for each fragment. E.g. 1-5,10,12-14')
	print('Empty line to end the input, and the unassigned atoms will be automatically assigned into a new fragment.')
	fragmentIndexes = []
	while True:
		inp = input()
		if inp.strip() == '':
			fragmentIndexes.append(analyzeFragmentIndex('else', len(coords)))
			break
		fragmentIndexes.append(analyzeFragmentIndex(inp, len(coords)))
	fragmentCoordinates = sortCoordinates(coords, fragmentIndexes)
	print('Input the charge and multiplicity for each fragment, respectively. \
		Empty line to end the input. E.g. 0 1')
	chargeAndMults = []
	while True:
		thisCharge = input()
		if thisCharge.strip() == '':
			break
		chargeAndMults.append(thisCharge)
	print('Input the kwds. Do not write guess=xxx.')
	kwd = input()
	if not 'nosymm' in kwd:
		kwd += ' nosymm'
	end = ''
	with open('end.txt') as f:
		end += ''.join(f.readlines())
	i = 0
	for f in fragmentCoordinates:
		i += 1
		writeGjf(gjf.replace('.gjf', f'_{i}.gjf'),
			f, kwd, nproc, mem, chargeAndMults[i - 1], end, gjf.replace('.gjf', f'_{i}.chk'))
	writeGjf(gjf.replace('.gjf', f'_mixed.gjf'),
			joinFragments(fragmentCoordinates), kwd + ' guess=read', nproc, mem, 
			overallMultAndCharge, end, gjf.replace('.gjf', f'_mixed.chk'))
	print('Now the gjf files for each fragment is outputted. Modify them to adapt to your task, run,\
	 and use kttk_mixer.py to build the combined fchk.')
