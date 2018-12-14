import json
import csv
import time
import re
import operator

def sol1(data1, data2):
    total = 0
    campaigns = []

    for elem in data1:
        tempData = elem.split(",")
        if "purple" in tempData[1]:
            campaigns.append(tempData[0])

    for elem in data2:
        tempData = elem.split(",")
        for campaign in campaigns:
            if campaign == tempData[0]:
                total += int(tempData[3])

    return total


def sol2(data):
    campaigns = {}
    total = 0

    for elem in data:
        day_list = []
        tempData = elem.split(",")
        campaign = tempData[0]
        date = tempData[2]
        if campaign not in  campaigns:
            day_list.append(date)
            campaigns[campaign] = day_list
        elif campaign in campaigns:
            if date not in campaigns[campaign]:
                campaigns[campaign].append(date)

    for k,v in campaigns.items():
        if len(v) > 4:
            total += 1
            
    return total


def sol3(data):
    total = 0

    for elem in data:
        if 'ad_type' not in elem:
            tempData = elem.rstrip().split(',"')[1]
            tempData = tempData.replace('""', '"').rstrip('"')
            tempJson = json.loads(tempData)
            for innerElem in tempJson:
                keys = list(innerElem.keys())
                if keys[0] == "H" and innerElem["action"] == "clicks":
                    total += int(innerElem[keys[0]])

    return total


def sol4(data):
    junk = {}
    noise = {}
    sources = []

    for elem in data:
        if 'ad_type' not in elem:
            tempData = elem.rstrip().split(',"')[1]
            tempData = tempData.replace('""', '"').rstrip('"')
            tempJson = json.loads(tempData)
            for innerElem in tempJson:
                keys = list(innerElem.keys())
                if innerElem['action'] == "junk" and keys[0] not in junk:
                    junk[keys[0]] = int(innerElem[keys[0]])
                elif innerElem[keys[1]] == "junk" and keys[0] in junk:
                    junk[keys[0]] += int(innerElem[keys[0]])
                if innerElem['action'] == "noise" and keys[0] not in noise:
                    noise[keys[0]] = int(innerElem[keys[0]])
                elif innerElem[keys[1]] == "noise" and keys[0] in noise:
                    noise[keys[0]] += int(innerElem[keys[0]])
                    
    for k, v in junk.items():
        for k2, v2 in noise.items():
            if k == k2 and v > v2:
                sources.append(k)

    return ', '.join(sources)


def sol5(data):
    clickTotal = 0
    totalCost = 0

    for elem in data:
        if 'ad_type' not in elem:
            if "video" in elem:
                tempData = elem.rstrip().split(',"')[1]
                tempData = tempData.replace('""', '"').rstrip('"')
                tempJson = json.loads(tempData)
                for innerElem in tempJson:
                    keys = list(innerElem.keys())
                    if innerElem["action"] == "clicks":
                        clickTotal += int(innerElem[keys[0]])
    
                totalCost += int(elem.split(',')[3])

    return round(totalCost / clickTotal, 2)


def sol6(data, data2):
    campaigns = []
    total = 0

    for elem in data:
        if "NY" in elem:
            campaigns.append(elem.split(",")[0])

    for elem in data2:
        campaign = elem.split(",")[0]
        if "B" in elem and campaign in campaigns:
            tempData = elem.rstrip().split(',"')[1]
            tempData = tempData.replace('""', '"').rstrip('"')
            tempJson = json.loads(tempData)
            for innerElem in tempJson:
                keys = list(innerElem.keys())
                if innerElem['action'] == "conversions" and keys[0] == 'B':
                    total += innerElem["B"]

    return total

#This is the only one I'm fairly certain is wrong. 
def sol7(data1,data2):
    campaign_spending = {}
    cpm_tracker = {}
    
    for elem in data2:
        if 'spend' not in elem:
            campaign = elem.split(',')[0]
            spend = int(elem.split(',')[3])
            if campaign not in campaign_spending:
                campaign_spending[campaign] = spend
            elif campaign in campaign_spending:
                campaign_spending[campaign] += spend

    for elem in data1:
        if 'campaign_id' not in elem:
            cost = 0
            campaign = elem.split(',')[0]
            impressions = int(elem.split(',')[2])
            if impressions != 0:
                audience = re.split('\d+-\d+',elem.split(',')[1])[0]
                if campaign in campaign_spending:
                    cost = campaign_spending[campaign]
                cpm = 1000 * (cost / impressions)
                if audience not in cpm_tracker:
                    cpm_tracker[audience] = round(cpm ,2)
                elif audience in cpm_tracker:
                    cpm_tracker[audience] += round(cpm, 2)

    return max(cpm_tracker.items(), key=operator.itemgetter(1))[0]


def main():
    fp1 = open("source1.csv", "r").readlines()
    fp2 = open("source2.csv", "r").readlines()
    start_time = time.time()

    print('The total spend against people with Purple hair was ${0}.'.format(sol1(fp1,fp2)))
    print('{0} campaigns spent on more than 4 days.'.format(sol2(fp2)))
    print('Source H reported clicks {0} times.'.format(sol3(fp2)))
    print('Source {0} reported more junk then noise.'.format(sol4(fp2)))
    print('The total cost per view for all video ads was ${0}'.format(sol5(fp2)))
    print('There were {0} source B conversions for campaigns targeting NY.'.format(sol6(fp1,fp2)))
    print('{0} had the best overall CPM.'.format(sol7(fp1,fp2)))
    print("The prog had a run time of {0} seconds.".format(time.time() - start_time))

main()
