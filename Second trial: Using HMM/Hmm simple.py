#! -- encoding: utf-8
from __future__ import unicode_literals
from hazm import *

normalizer = Normalizer()
out_file = open('out.txt','w')

#RAW TEXT:
text = 'علی از مدرسه آمد. سیب میوه ای خوشمزه است. رییس-جمهور روحانی عید مبعث حضرت محمد را تبریک گفتند. مصطفی در تهران آنفولانزا گرفته است.'

norm_text = normalizer.normalize(text)

text = word_tokenize(norm_text)
j=0
for i in text:
	out_file.write(str(j)+' ')
	out_file.write(i.encode('utf8'))
	out_file.write('\n')
	j+=1

#ANNOTATING TEXT:
text[0] = [text[0],'PERSON']
text[1] = [text[1],'OTHER']
text[2] = [text[2],'OTHER']
text[3] = [text[3],'OTHER']
text[4] = [text[4],'OTHER']
text[5] = [text[5],'OTHER']
text[6] = [text[6],'OTHER']
text[7] = [text[7],'OTHER']
text[8] = [text[8],'OTHER']
text[9] = [text[9],'OTHER']
text[10] = [text[10],'OTHER']
text[11] = [text[11],'PERSON']
text[12] = [text[12],'OTHER']
text[13] = [text[13],'OTHER']
text[14] = [text[14],'OTHER']
text[15] = [text[15],'PERSON']
text[16] = [text[16],'OTHER']
text[17] = [text[17],'OTHER']
text[18] = [text[18],'OTHER']
text[19] = [text[19],'OTHER']
text[20] = [text[20],'PERSON']
text[21] = [text[21],'OTHER']
text[22] = [text[22],'LOCATION']
text[23] = [text[23],'OTHER']
text[24] = [text[24],'OTHER']
text[25] = [text[25],'OTHER']

#CALCULATING PARAMETERS OF HMM MODEL
states = ['PERSON', 'LOCATION','OTHER']

#CALCULATING START PROBABILITY:

#detecting start of sentences:
start_indexes = [0]				#this list holds indexes of the starting words
for i in range(len(text)-1):
	if text[i][0]=='.':
		start_indexes.append(i+1)


start_p = []					#this list holds probability of each state begining a sentence, parameter 'pi' for each state

for state in states:
	n = 0.0
	for index in start_indexes:
		if text[index][1] == state:
			n+=1
	start_p.append(n/len(start_indexes)) 

#CALCULATING TRANSITION PROBABILITY:
transition_p = []
total_number_of_states = []
for state in states:
	n = 0
	for word in text:
		if word[1] == state:
			n+=1
	total_number_of_states.append(n)
# her is OTHER because we omit 2 first characters
counter = 0
for state_i in states:
	temp = []
	for state_j in states:
		n=0.0
		for i in range(len(text)-1):
			if (text[i][1] == state_i) and (text[i+1][1] == state_j):
				n+=1
		temp.append(n/total_number_of_states[counter])
	transition_p.append(temp)
	counter += 1			 		


#using viterbi algorithm we decide tags for a sample text!
sample_text = 'محمد به مدرسه رفت. پرتقال میوه خوبی است. پایتخت ایران تهران است.'

norm_text = normalizer.normalize(sample_text)

sample_text = word_tokenize(norm_text)

tagged = []
for i in range(len(sample_text)):
	tagged.append('OTHER')

for i in range(len(sample_text)-1):
	word = sample_text[i]
	if i == 0:
		tagged[i] = states[start_p.index(max(start_p))]
	if word == '.':
		tagged[i+1] = states[start_p.index(max(start_p))]

	else:
		current_tag = tagged[i]
		current_state_index = int(states.index(tagged[i]))
		maximum_p = max(transition_p[current_state_index])
		maximum_index = transition_p[current_state_index].index(maximum_p)
		tagged[i+1] = states[maximum_index]

print tagged
