import numpy as np
import pandas as pd

# Generate basic scoring_list to score the top 'n'
def scoring_list_gen(n):
    scoring_list = numpy.zeros(n)
    for i in n:
        scoring_list[i] = n - i
    return scoring_list

# Score the top 'n' chosen through a particular method
def score(sorted_list, scoring_list, top_n):
    scored_list = numpy.zeros(5000)
    for i in top_n:
        scored_list[sorted_list[i]] = scoring_list[i]
    return scored_list

def cbscore(uid, iid, IIM, UIM, scoring_list, top_n):
    uid_row = UIM[uid]
    clean_uid_row = numpy.zeros(5000)

    top = numpy.sort(iid_row)[:top_n]
    return score(top, scoring_list, top_n)

def ucfscore(uid, UIM, label_list, scoring_list, top_n):
    #Cloning UIM[uid,iid] with zeros
    uidIM = numpy.zeros(1000, 5000)
    #Filling uidIM with input uid's row            
    uid_label = label_limit
    for i in len(label_list):
        #If this uid label found
        if uid_label != label_limit:
            if label_list[i] == uid_label:
                uidIM[i] = UIM[i]
        #Choosing label for this uid
        elif i == uid:
            uid_label = label_list[i]
    #Clean uidIM of previously seen items
    
    #Square and sum item coloumns and pick top_n iids
    uidItemList = sqr_sum(uidIM, top_n)

    score(uidItemList, scoring_list, top_n)

def sqr_sum(uidIM, top_n):
    #Squaring and summing columns of uidIM
    sqr_uidIM = uidIM * uidIM
    sqrd_sum_list = sqr_uidIM.sum(axis=0)
    #Argsort sqrd_sum_list to get uidItemList
    return numpy.argsort(sqrd_sum_list)[:top_n]

def icfscore(uid, iid, UIM, UUM, scoring_list, top_n):
    UIMtp = UIM.transpose
    #Get the uids of non-empty elements of this iid
    uid_list = []
    for userid in 1000:
        if UIMtp[iid, userid] != 0:
            uid_list.append(userid)
    #Creating UUM row of only relevant users for this uid
    UUM_row = numpy.zeros[1000] + 355
    for userid in uid_list:
        UUM_row[userid] = UUM[uid,userid]
    #Sort UUM_row and pick top_n uids
    topn_sorted_UUM_uids = numpy.argsort(UUM[uid])[:top_n]
    #Creating UIM of only relevant user's items
    uidIM = numpy.zeros[1000,5000]
    for userid in topn_sorted_UUM_uids:
        uidIM[userid] = UIM[userid]
    #Square and sum item coloumns and pick top_n uids
    uidItemList = sqr_sum(uidIM, top_n)

    score(uidItemList, scoring_list, top_n)
