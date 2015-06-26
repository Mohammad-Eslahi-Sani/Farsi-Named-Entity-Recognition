#! -- encoding: utf-8
from __future__ import unicode_literals
from hazm import *

normalizer = Normalizer()
out_file = open('out.txt','w')
dictionary = { 'علی':'PERSON', 'اصلاحی':'PERSON' ,'زهرا':'PERSON' , 'رضا':'PERSON', 'بردسکن':'LOCATION', 'تهران':'LOCATION', 'ایران':'LOCATION', 'مشهد':'LOCATION' , 'علی':'PERSON', 'آنفولانزا':'SICKNESS' ,'سرطان':'SICKNESS' }
	
s = 'دکتر قلی اصلاحی در تهران بیماری آنفولانزا گرفت. علی فلانی در مشهد دچار بیماری سرطان شده است.استاد تقوی آدم خوبی است. شهر اصفهان زیبا است. بیماری ایدز خطرناک است. و در مجارستان رایج است. مرکز استان سیستان-و-بلوچستان شهر زاهدان است. '
out_file.write('\n')
out_file.write(s.encode('utf8'))
out_file.write('\n')
s = normalizer.normalize(s)
tagger = POSTagger(model='resources/postagger.model')
a = tagger.tag(word_tokenize(s))
out = []
for i in a:
	for j in i:
		out_file.write(j.encode('utf8'))
		out_file.write('\t')
	out_file.write('\n')

noune_clause = []
n = len(a)
i=0
while i < n:
	
	#clean the noune clause:
	noune_clause = []	
		
	if (a[i][1] =='Ne') or (a[i][1] == 'N'):
		#Start of noune clause
		noune_clause.append(a[i])
		while (i+1 < n) and (a[i+1][1]=='N'):
			#noune clause continues
			i = i+1
			noune_clause.append(a[i])
		#end of noune clause
		
		i=i+1
		#Check being in dictionary:
		check = False
		check_value = 'O'
		for j in noune_clause:
			if j[0] in dictionary:
				check = True
				check_value = dictionary[j[0]]
				break
		
		#check using words like 'پروفسور'
		pre_PERSON = ['پروفسور','دکتر','مهندس','خانم','آقا','استاد']
		count = len(noune_clause)
		if count>1 and not check:
			for h in noune_clause:
				for q in pre_PERSON:
					if h[0]==q:
						check = True
						check_value = 'PERSON'
						break


		#check location identifiers:
		pre_LOCATION = ['استان','کشور','شهر','قاره','روستا','ناحیه']
		count = len(noune_clause)
		if count>1 and not check:
			for h in noune_clause:
				for q in pre_LOCATION:
					if h[0]==q:
						check = True
						check_value = 'LOCATION'
						break
		
		#check sickness identifiers:
		pre_SICKNESS = ['بیماری','سندروم','سرطان']
		count = len(noune_clause)
		if count>1 and not check:
			for h in noune_clause:
				for q in pre_SICKNESS:
					if h[0]==q:
						check = True
						check_value = 'SICKNESS'
						break
		
		
		#check having 'ستان' at the end of word
		if not check:
			for h in noune_clause:
				if h[0][-4:]=='ستان':
					check = True
					check_value = 'LOCATION'
		

		#Adding to out list
		if check:
			for j in noune_clause:
				if noune_clause.index(j) == 0:
					out.append([j[0],'B_'+check_value])
				else:
					out.append([j[0],'I_'+check_value])
		else:
			for j in noune_clause:
				out.append([j[0],'O'])
		
	else:
		out.append([a[i][0],'O'])
		i+=1

#writing out list in the output file
for i in out:
	out_file.write(i[0].encode('utf8'))
	out_file.write('\t')
	out_file.write(i[1])
	out_file.write('\n')

		

out_file.close()
