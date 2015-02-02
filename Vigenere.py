#------------------------------------------------------------------------------
# Author: Frank Carotenuto Date: 11/27/2014
#
# Description: Porvides Methods for Encription, Decription and Atacking
#			   the Vigenere Cipher using Frequency analysis
#------------------------------------------------------------------------------
import pygal, decimal, collections
from detect_peaks import detect_peaks

#------------------------------------------------------------------------------
# Takes input key and plain_text. Returns encripted text
#------------------------------------------------------------------------------
def vigenere_Cipher_Encript(key, plain_text):
	cipher_text = [((ord(plain_text[i])-65) + (ord(key[i % len(key)])-65))% 26 
	for i in range(len(plain_text))]
	return ''.join([chr(ch+65) for ch in cipher_text])

#------------------------------------------------------------------------------
# Takes input key and cipher_text. Returns plain text
#------------------------------------------------------------------------------
def vigenere_Cipher_Decript(key, cipher_text):
	plain_text = [((ord(cipher_text[i])-65) - (ord(key[i % len(key)])-65))% 26 
	for i in range(len(cipher_text))]
	return ''.join([chr(ch+65) for ch in plain_text])

#------------------------------------------------------------------------------
# Takes input cipher_text_ and retuens key length using frequency analysis
#------------------------------------------------------------------------------
def find_key_len(cipher_text_):
	cipher_text = cipher_text_
	cipher_list0 = [ord(letter)-65 for letter in cipher_text]

	# Creates array of match counts with each shift
	count_array = []
	for i in range(1,50):
		count = 0
		temp_list = [0 for t in range(i)]+cipher_list0
		for w in range(i,len(cipher_list0)):
			if temp_list[w] == cipher_list0[w]:
				count += 1
		count_array.append(count)

	# Attempts to determine key length
	avg_match = sum(count_array)/len(count_array)
	over_avg = detect_peaks(count_array, show=True, threshold=30)
	key_len = over_avg[1] - over_avg[0]

	return key_len

#------------------------------------------------------------------------------
# Using frequency analysis and the "Dot Product" method, returns the 
# encription key
#------------------------------------------------------------------------------
def find_key(key_len, cipher_text):
	chunk, chunk_size = len(cipher_text), key_len
	chunks = [cipher_text[i:i+chunk_size] for i in range(0, chunk, chunk_size)]
	del chunks[-1]

	# Appends every i % key_len char to its respective array 
	# to reduce the problem to a simple shift cipher
	A = [[] for i in range(key_len)]
	for i in range(len(chunks)):
		for j in range(key_len):
			A[j].append(chunks[i][j])

	# Counts all the occurances of each letter
	list_of_counts = [collections.Counter(A[i]) for i in range(key_len)]

	# Converts the dictionary of letter counts in to a list of frequencies 
	# sorted Alphabeticaly
	FRQ = [[] for i in range(key_len)]
	for i in range(key_len):
		for j in range(26):
			FRQ[i].append(list_of_counts[i][chr(j+65)]/float(len(A[0])))

	# Frequencies of english letters
	SL = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
		  0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 
		  2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

	# Calculates the dot product of each set of frequencies
	FL = [[] for i in range(key_len)]
	for i in range(key_len):
		for j in range(26):
			FL[i].append(sum([FRQ[i][(j+k) % 26]*SL[k] for k in range(26)]))

	# Finds max Dot Product which is the offest, converts to character, joins
	# and displays string.
	return ''.join([chr(FL[i].index(max(FL[i]))+65) for i in range(key_len)])


#------------------------------------------------------------------------------
# Example using a few pages of Harry Potter
#------------------------------------------------------------------------------
if __name__ == '__main__':

	plain_text = ''.join('''A breeze ruffled the neat hedges of Privet Drive 
		which lay silent and tidy under the inky sky the very last place you 
		would expect astonishing things to happen Harry Potter rolled over 
		inside his blankets without waking up One small hand closed on the 
		letter beside him and he slept on not knowing he was special not 
		knowing he was famous not knowing he would be woken in a few hours 
		time by Mrs Dursleys scream as she opened the front door to put out 
		the milk bottles nor that he would spend the next few weeks being 
		prodded and pinched by his cousin Dudley He couldnt know that at 
		this very moment people meeting in secret all over the country were 
		holding up their glasses and saying in hushed voices To Harry Potter 
		the boy who lived! CHAPTER TWO THE VANISHING GLASS Nearly ten years 
		had passed since the Dursleys had woken up to find their nephew on 
		the front step but Privet Drive had hardly changed at all The sun 
		rose on the same tidy front gardens and lit up the brass number four 
		on the Dursleys front door it crept into their living room which was 
		almost exactly the same as it had been on the night when Mr Dursley had 
		seen that fateful news report about the owls Only the photographs on the 
		mantelpiece really showed how much time had passed Ten years ago there had 
		been lots of pictures of what looked like a large pink beach ball wearing 
		different colored bonnets but Dudley Dursley was no longer a baby and 
		now the photographs showed a large blond boy riding his first bicycle 
		on a carousel at the fair playing a computer game with his father being 
		hugged and kissed by his mother The room held no sign at all that 
		another boy lived in the house too Yet Harry Potter was still there 
		asleep at the moment but not for long His Aunt Petunia was awake and 
		it was her shrill voice that made the first noise of the day Up! Get 
		up! Now! Harry woke with a start His aunt rapped on the door again Up! 
		she screeched Harry heard her walking toward the kitchen and then the 
		sound of the frying pan being put on the stove He rolled onto his back 
		and tried to remember the dream he had been having It had been a 14 
		good one There had been a flying motorcycle in it He had a funny feeling 
		hed had the same dream before His aunt was back outside the door Are you 
		up yet she demanded Nearly said Harry Well get a move on I want you to 
		look after the bacon And dont you dare let it burn I want everything 
		perfect on Duddys birthday Harry groaned What did you say his aunt 
		snapped through the door Nothing nothing Dudleys birthday how could 
		he have forgotten Harry got slowly out of bed and started looking 
		for socks He found a pair under his bed and after pulling a spider 
		off one of them put them on Harry was used to spiders because the 
		cupboard under the stairs was full of them and that was where he slept 
		When he was dressed he went down the hall into the kitchen The table was 
		almost hidden beneath all Dudleys birthday presents It looked as though 
		Dudley had gotten the new computer he wanted not to mention the second 
		television and the racing bike Exactly why Dudley wanted a racing bike was 
		a mystery to Harry as Dudley was very fat and hated exercise unless of 
		course it involved punching somebody Dudleys favorite punching bag was 
		Harry but he couldnt often catch him Harry didnt look it but he was 
		very'''.replace('\n', '').upper().split())

	CT = vigenere_Cipher_Encript('TUNA', plain_text)

	KL = find_key_len(CT)

	K = find_key(KL, CT)

	print CT
	print K
	print vigenere_Cipher_Decript(K, CT)