import pandas as pd
import numpy as np
from scipy import stats

UIM = pd.DataFrame(np.zeros(5000,1000))
IIM = pd.DataFrame(np.zeros(1000,1000))
UUM = pd.DataFrame(np.zeros(5000,5000))
top_n = 20
labels = pd.DataFrame(np.zeros(1000))

def initI(uid):
    #Returns a list of item indices in UIM st. UIM(uid, i) = 0
    cond = UIM[uid] == 0
    return UIM.index[cond].tolist()

def initI_noIID(uid, iid):
    #Returns a list of item indices in UIM st. UIM(uid, i) = 0 and i != iid
    return init(uid).drop([iid])

def cbscore(uid, iid):
    I = initI_noIID(uid)
    #Storing the IIM values of this iid column restricted to indices in I
    M = IIM.iloc[I,iid]
    #Sort M and return the top n indices
    return pd.argsort(M)[:top_n]

def ucfscore(uid):
    I = initI(uid)
    #Storing list of user indices having the same label as this uid
    cond = labels == labels[uid]
    U = labels.index[cond].tolist()
    return slicingUIM(U, I)

def icfscore(uid, iid):
    I = initI_noIID(uid)
    U = genU(iid)
    #Storing top user indices 
    U1 = pd.argsort(UUM[uid, U])[:top_n].tolist()
    return slicingUIM(U1, I)

def slicingUIM(U, I):
    #Storing UIM values for indices in I and U for respective axes
    M = UIM.iloc[I,U]
    #Square and sum across users
    M2 = (M * M).sum(0)
    #Sort M and return the top n indices
    return pd.argsort(M2)[:top_n]

# Generate basic scoring_list to score the top 'n'
def scoring_list_gen(n):
    scoring_list = np.zeros(n)
    for i in n:
        scoring_list[i] = n - i
    return scoring_list

# Score the top 'n' chosen through a particular method
def score(sorted_list, scoring_list, top_n):
    scored_list = np.zeros(5000)
    for i in top_n:
        scored_list[sorted_list[i]] = scoring_list[i]
    return scored_list

def genU(iid):
    #Storing list of user indices in UIM st. UIM(u, iid) != 0
    UIMT = UIM.T
    cond = UIMT[iid] != 0
    return (UIMT.index[cond].tolist())

def genI(uid):
    #Storing list of user indices in UIM st. UIM(uid, i) != 0
    cond = UIM[uid] != 0
    return (UIMT.index[cond].tolist())

def finalscore(uid, iid):
    up = len(genU(iid))
    ip = len(genI(uid))

    scoring_list = scoring_list_gen()
    cbscore = score(cbscore, scoring_list, top_n)
    ucfscore = score(ucfscore, scoring_list, top_n)
    icfscore = score(icfscore, scoring_list, top_n)

    if up<20:
        if ip<20:
            return cbscore(uid,iid)
        else:
            return (icfscore(uid,iid) * up(iid)/1000 + cbscore(uid,iid) * (1 - up(iid)/1000))
    else:
        if ip<20:
            return (ucfscore(uid) * ip(uid)/5000 + cbscore(uid,iid) * (1 - ip(uid)/5000))
        else:
            return (ucfscore(uid) * ip(uid)/5000 +
            (icfscore(uid,iid) * up(iid)/1000 + cbscore(uid,iid) * (1 - up(iid)/1000)) * (1 - ip(uid)/5000))

#

#Returns randomly ranked list of 10 iids with 1 wildcard entry included
def wildcard(uid, iid):
    mainList = pd.argsort(finalscore(uid, iid))[:9].tolist()
    dropList = []
    dropList = dropList.append(mainList).append(iid).append(genI(uid))
    wildIIDList = pd.DataFrame(np.arange(5000)).drop(dropList)
    upList = wildIIDList.apply(lambda i: len(genI(i))+1)

    hm = scipy.stats.hmean(upList)
    length = wildIIDList.size()
    k = hm / length
    pList = wildIIDList.apply(lambda i: k/(len(genI(i))+1))
    wildIID = np.random.choice(wildIIDList, 1, True, pList)[0]

    return random.shuffle(mainList.append(wildIID))

#Returns randomly ranked list of 10 iids with 1 wildcard entry included without taking iid arg
def wildcard(uid):
    mainList = pd.argsort(finalscore(uid))[:9].tolist()
    dropList = []
    dropList = dropList.append(mainList).append(genI(uid))
    wildIIDList = pd.DataFrame(np.arange(5000)).drop(dropList)
    upList = wildIIDList.apply(lambda i: len(genI(i))+1)

    hm = scipy.stats.hmean(upList)
    length = wildIIDList.size()
    k = hm / length
    pList = wildIIDList.apply(lambda i: k/(len(genI(i))+1))
    wildIID = np.random.choice(wildIIDList, 1, True, pList)[0]

    return random.shuffle(mainList.append(wildIID))

