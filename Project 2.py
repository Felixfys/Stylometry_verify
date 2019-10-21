
#This program aims to use stylometry to verify authorship

import math
import os

def getfile(textfile1): # function to open file
    file = textfile1
    with open(file,'rt') as file1:
        data = file1.read()
        return (data,file)

def word_par(file,data): # function to break file into list of words(string)
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    wordss = []
    word = ""
    mode = 0
    data = data.lower().replace('--',' ') #lowercase and replace all -- with ' '
    for ch in data:
        if mode == 1:
            wordss.append(word)
            word = ""
            mode = 0
        if ch in alpha or ch == "'" or ch == '-':
            word += ch
        elif ch == '.' or ch == ',' or ch == ';':
            wordss.append(word)
            word = ""
            wordss.append(ch)
        else:
            mode = 1
    words = []
    for string in wordss:
        string = string.lstrip("'") #removing any special case where "'" is the start of end of a string
        string = string.rstrip("'")
        words.append(string)        
    return(words,data)

def words_count(words,data1): #count number of words and  modify profile dict
    profile = {
        "'" : 0.0,
        ',' : 0.0,
        '-' : 0.0,
        ';' : 0.0,
        'also' : 0.0,
        'although' : 0.0,
        'and' : 0.0,
        'as' : 0.0,
        'because' : 0.0,
        'before' : 0.0,
        'but' : 0.0,
        'for' : 0.0,
        'if' : 0.0,
        'nor' : 0.0,
        'of' : 0.0,
        'or' : 0.0,
        'sentences_per_par' : 0.0,
        'since' : 0.0,
        'that' : 0.0,
        'though' : 0.0,
        'until' : 0.0,
        'when' : 0.0,
        'whenever' : 0.0,
        'whereas' : 0.0,
        'which' : 0.0,
        'while' : 0.0,
        'words_per_sentence' : 0.0,
        'yet' : 0.0,}
    for string in words:
        for key in profile:
            if string == key:
                profile[key] = profile.get(key,0) + 1
        for ch in string:
            if ch == '-':
                profile['-'] = profile.get('-',0) + 1
            elif ch == "'":
                profile["'"] = profile.get("'",0) + 1
    words_per_sent,sent_per_par,num_sent = sent_words(data1) #compute 'sentences_per_par' and 'words_per_sentence' seperately and add back into profile
    profile['sentences_per_par'] = sent_per_par
    profile['words_per_sentence'] = words_per_sent
    return(profile,num_sent)

def printfile(profile,file): #function to print file
    print('profile of text ' + str(file))
    for key,value in profile.items():
        print(key,'\t','{0:.4f}'.format(value))

def sent_words(data): # 'sentences_per_par' and 'words_per_sentence'
    data = data.lower().replace('--',' ')
    data1 = data.replace("! ",". ").replace("? ",". ").replace("!'",". ").replace("?'",". ").replace('."',". ").replace('?"',". ").replace('!"',". ").replace(".'",". ").split(". ")
    #The above chain of .replace takes into consideration the definition of a sentence and change all sentence ending into '. ' for splitting creating a list of sentences
    data_sent_count = []
    for string in data1: #break up any strings that is suppose to be 2 seperate strings according to criteria
        string1 = string.split('.\n')
        data_sent_count.extend(string1)
    while '' in data_sent_count: data_sent_count.remove('')  #remove extra space
    data_para = data.replace('.\n','\n\n').split('\n\n')     #split based on paragraph criteria
    data_sent = []
    for para in data_para: #each paragraph in text is split into sentences
        while '' in data_para: data_para.remove('')          #remove extra space
        para1 = para.replace('\n',' ')
        data_sent.append(para1.replace("! ",". ").replace("? ",". ").replace("!'",". ").replace("?'",". ").replace('."',". ").replace('?"',". ").replace('!"',". ").replace(".'",". ").split(". "))
        list1_count = [] #list of number of words each sentence
    list2_count = [] #list of number of sentences each parahgraph
    words_per_sent = 0
    sent_per_par = 0
    sum1_count = 0
    for para in data_sent:
        while '' in para: para.remove('')
        for sentence in para:
            sentence = sentence.split()
            list1_count.append(len(sentence)) #list of num of words in a sentence
        list2_count.append(len(para)) #num of sentence in para
    for num in list1_count:
        sum1_count += num
    sum2_count = len(data_sent_count)
    words_per_sent = sum1_count/len(data_sent_count)
    sent_per_par = sum2_count/len(list2_count)
    return(words_per_sent,sent_per_par,sum2_count)

def normalise(file,profile,num_sent): #function to normalise data 
    for key in profile: 
        if key == 'sentences_per_par':
            continue
        elif key == 'words_per_sentence':
            continue
        else:
            profile[key] /= num_sent
    return(profile)
            
def dist(profile1,profile): #function to calculate standard distance formula
    summation = 0
    for (key1,value1),(key2,value2) in zip(profile1.items(),profile.items()): #loop together to get a summation of each row : row 1 value from profile1 minus the same row value from other profile
        summation += (value1 - value2)**2
    x = math.sqrt(summation)
    print('The distance between the two texts is: ' + '{0:.4f}'.format(x))
    
    
def main(textfile1, arg2, normalize = False):
    if not os.path.isfile(textfile1) :  #checking file is valid
        print('This is not a valid file name, please try again.')
        if arg2 == 'listing':
            return
        elif not os.path.isfile(arg2):  #if arg is a 2nd file, check if valid:
            print('This is not a valid file name as well, please try again.')
            return
    if os.path.isfile(textfile1): #if file1 valid, is arg 2 valid
            if arg2 != 'listing' and os.path.isfile(arg2) == False:
                print('This is not a valid file name, please try again.')
                return
    if arg2 == 'listing' and normalize == False: #output first file profile
        data,file = getfile(textfile1)
        words,data1 = word_par(file,data)
        sent_words(data)
        profile,num_sent = words_count(words,data1)
        printfile(profile,file)
    elif arg2 != 'listing' and normalize == False: # output both file dist
        data,file = getfile(textfile1)
        words,data1 = word_par(file,data)
        profile,num_sent = words_count(words,data1)
        profile1 = profile.copy()
        textfile1 = arg2
        data,file = getfile(textfile1)
        words,data1 = word_par(file,data)
        profile,num_sent = words_count(words,data1)
        dist(profile1,profile)
    elif arg2 == 'listing' and normalize == True: #normalize first file
        data,file = getfile(textfile1)
        words,data1 = word_par(file,data)
        profile,num_sent = words_count(words,data1)
        profile = normalise(file,profile,num_sent)
        printfile(profile,file)
    elif arg2 != 'listing' and normalize == True: #normalize both files and output dist
        data,file = getfile(textfile1)
        words,data1 = word_par(file,data)
        profile,num_sent = words_count(words,data1)
        profile = normalise(file,profile,num_sent)
        profile1 = profile.copy()
        data,file = getfile(arg2)
        words,data1 = word_par(file,data)
        profile,num_sent = words_count(words,data1)
        profile = normalise(file,profile,num_sent)
        dist(profile1,profile)
        

    
