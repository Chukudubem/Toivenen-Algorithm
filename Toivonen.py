import os
import sys
import random
import math
import time
import itertools
from itertools import combinations

input_file = sys.argv[1]
with open(input_file, "r") as f:
    '''
    Read input file
    '''
    data = f.readlines()    

def get_parameters(data):
    n = len(data)                                       
    sample_size = int(math.ceil(0.1 * n))              
    threshold = 4/15.0                                  
    support = int(math.ceil(sample_size*threshold))     
    n_samples = n/sample_size                           
    return n, support, sample_size, n_samples

def random_sample_generation(n, sample_size, seeder):
    random.seed(seeder)
    k = random.randint(0, n - sample_size)
    x = [i for i in range(k, k + sample_size)]
    return x

def load_sample(data, x):
    sample = [eval(data[i]) for i in x]
    return sample

def load_baskets(data,n):
    baskets = [eval(data[i]) for i in range(n)]
    return baskets

def make_tuple(k):
    if isinstance(k, tuple):
        return k
    else:
        return k,

def singletons(baskets, support):
    candidate_items = {}
    frequent_items = []
    negative_border = []
    for basket in baskets:
        basket = make_tuple(basket)    
        for j in basket:
            if j in candidate_items:
                candidate_items[j] +=1
            else:
                candidate_items[j] = 1
    for k,v in candidate_items.items():
        if v >= support:
            frequent_items.append(k)
        else:
            negative_border.append(k)
            
    return frequent_items, negative_border

def candidate_itemset_generator(frequent_items, frequent_itemset, baskets, p):
    candidate_set = []
    if p == 2:
        for basket in baskets:
            basket = make_tuple(basket)    
            for pairs in itertools.combinations(frequent_items, 2):
                if len(pairs) == p and pairs not in candidate_set:
                    candidate_set.append(pairs)
    else:
        for i, f1 in enumerate(frequent_itemset):
            for j, f2 in enumerate(frequent_itemset):
                if j > i:
                    if len(set(f1).intersection(set(f2))) == p - 2:
                        pair =  set(f1)|set(f2)
                        if pair not in candidate_set:
                            pairs = list(itertools.combinations(pair, p-1))
                            b = 0
                            for each in pairs:
                                if b == p - 2:
                                    break
                                if (set(f1).intersection(set(f2))).issubset(each) == False:
                                    if each in frequent_itemset:
                                        b += 1
                            if b == p - 2:
                                candidate_set.append(pair)

    return candidate_set

def counter(baskets, candidate_set):
    candidate_ = {}
    for candidate in candidate_set:
        
        for basket in baskets:
            basket = make_tuple(basket)    
            if len(candidate) > 2:
                candidate_.setdefault(tuple(candidate),0)
                if candidate.issubset(basket):
                    candidate_[tuple(candidate)] += 1
            else:    
                candidate_.setdefault(candidate,0)
                if set(candidate).issubset(basket):
                    candidate_[candidate] += 1
    
    return candidate_

def frequent_itemset_finder(candidates, support, frequent_itemset, negative_border):
    frequent = []
    for k,v in candidates.items():
            if v >= support:
                frequent.append(k)
                frequent_itemset.append(k)
            else:
                negative_border.append(k)
    return frequent

def apriorii(data):
    p = 2
    threshold = 4/15.0 
    frequent_itemset = []
    n, support = get_parameters(data)[:2]
    support = int(math.ceil(n*threshold))
    baskets = load_baskets(data,n)
    frequent_items, negative_border = singletons(baskets, support)
    while 1:
        candidate_set = candidate_itemset_generator(frequent_items, frequent_itemset, baskets, p)
        candidates = counter(baskets, candidate_set)
        frequent = frequent_itemset_finder(candidates, support, frequent_itemset, negative_border)
        p = p+1
        if not frequent:
            break
    return baskets, frequent_items + frequent_itemset, negative_border

def apriori(data,seeder):
    p = 2
    frequent_itemset = []
    n, support, sample_size, n_samples = get_parameters(data)
    x = random_sample_generation(n, sample_size, seeder)
    baskets = load_sample(data, x)
    frequent_items, negative_border = singletons(baskets, support)
    while 1:
        candidate_set = candidate_itemset_generator(frequent_items, frequent_itemset, baskets, p)
        candidates = counter(baskets, candidate_set)
        frequent = frequent_itemset_finder(candidates, support, frequent_itemset, negative_border)
        p = p+1
        if not frequent:
            break  
    return baskets, frequent_items + frequent_itemset, negative_border

def Toivenen(data):
    directory = os.path.join("../", 'chukwudubem_nwoji_hw2/output')
    if not os.path.exists(directory):
        os.mkdir(directory)   
    start_time = time.time()
    seeder = 1
    checker = 1
    while checker:
        sample_basket, sample_frequent_itemset, sample_negative_border = apriori(data, seeder)
        full_basket, full_frequent_itemset, full_negative_border = apriorii(data)
        false_negative = sorted(set(full_frequent_itemset) - set(sample_frequent_itemset))
        true_frequent_sample = [value for value in sample_frequent_itemset if value in full_frequent_itemset]
        true_negative_sample = [(value) for value in sample_negative_border if value in full_negative_border]
        print("False Negative: " + str(false_negative))
        filename = "OutputForIteration_%s.txt" %seeder
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write("Sample Created: " + str(sample_basket))
            f.write(" \nFrequent Itemsets: " + str(true_frequent_sample))
            f.write(" \nNegative Border: " + str(true_negative_sample))   
        seeder +=1
        if not false_negative:
            checker = 0
    print( "---" + str(seeder - 1) + " time iterations ---")
    print("--- %s seconds ---" % (time.time() - start_time))

Toivenen(data)
