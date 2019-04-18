import re
import json
import heapq
from pprint import pprint
lines = []
#with open("~/path/to/dic.txt", 'r') as f:
#    handle2name = json.load(f)
with open("~/path/to/gtweets.dat") as f:
    for line in f:
        if line[:5] == '"RT @':
            start = line.find(':')+2
            lines.append(line[start:-1])
        else:
            lines.append(line[1:-1])
global_awards = {}
host_lines = []
win_lines = []
present_lines = []
nominee_lines = []
regexs = {
    "award":            'Best(?: (?:[A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+',
    "winner":           '(@[\w]+|[A-Z][a-z]+(?: [A-Z][a-z]+){1,2})',
    "presenter":        '(@[\w]+|[A-Z][a-z]+(?: [A-Z][a-z]+){1,2})',
    "host_words":       '([Mm]onologue|[Oo]pening)',
    "winner_words":     '(congra|win|won|goes to|takes home)',
    "presenter_words":  '( present|introduce| announc)',
    "nominee_words":    '( nom|didnt|not|did not|didnt|should|wow|believe)',
}

class Award(object):
    def __init__(self, name):
        self.name = name
        split_name = name[5:].replace(',','').replace('-','').split()
        self.gist = [word for word in split_name if word[0].isupper()]
        self.freq = 1
        self.aliases = []
        self.winner = {}
        self.presenters = {}
        self.nominees = {}

def similar(l1, l2):
    acc = 0
    len1 = len(l1)
    len2 = len(l2)
    if len1 <= len2:
        for x in l1:
            if x in l2:
                acc += 1
        if type(l1) == str:
            return acc/len1 >= .8
        else:
            return acc/len1 > .5
    else:
        for x in l2:
            if x in l1:
                acc += 1
        if type(l2) == str:
            return acc/len2 >= .8
        else:
            return acc/len2 > .5

def parse_lines(data):
    for line in data:
        # make Award obj for each award-matching regex
        for award_match in re.findall(regexs["award"], line):
            if award_match in global_awards:
                global_awards[award_match].freq += 1
            else:
                global_awards[award_match] = Award(award_match)
        # store host-, winner-, presenter-, and nominee-related lines for later
        if re.search(regexs["host_words"], line):
            host_lines.append(line)
        if re.search(regexs["winner_words"], line):
            win_lines.append(line)
        if re.search(regexs["presenter_words"], line):
            present_lines.append(line)
        if re.search(regexs["nominee_words"], line):
            nominee_lines.append(line)
parse_lines(lines)

def build_freq_dicts(awards):
    for award in awards:
        for line in win_lines:
            search_str = regexs['winner'] + "(?=.* (?:win|won|takes home).+" + award + ")"
            search_str2 = '(?<=' + award + ' goes to )' + regexs['winner'] 
            winners = re.findall(search_str, line) or re.findall(search_str2, line)
            for winner in winners:
                winner_dict = awards[award].winner
                if winner in winner_dict:
                    winner_dict[winner] += 1
                else:
                    winner_dict[winner] = 1
        for line in present_lines:
            search_str = regexs['presenter'] + "(?=.* (?:present|announc|introduc).+" + award + ")"
            search_str2 = '(?<=' + award + ' presented by )' + regexs['presenter'] 
            presenters = re.findall(search_str, line) or re.findall(search_str2, line)
            for presenter in presenters:
                presenter_dict = awards[award].presenters
                if presenter in presenter_dict:
                    presenter_dict[presenter] += 1
                else:
                    presenter_dict[presenter] = 1
build_freq_dicts(global_awards)

def link_awards(awards):
    pass
#for a1 in global_awards:
#    award1 = global_awards[a1]
#    for a2 in global_awards:
#        award2 = global_awards[a2]
#        if award1 is award2:
#            pass
#        else:
#            if a1 in a2:
#                award1.abbrev_of.append(award2)
#            elif similar(award1.gist, award2.gist):
#                if award1.winner and award2.winner:
#                    a1win = max(award1.winner, key=lambda key: award1.winner[key])
#                    a2win = max(award2.winner, key=lambda key: award2.winner[key])
#                    if (similar(a1win, a2win) and award1 not in award2.aliases
#                            and a2 not in a1):
#                        award1.aliases.append(award2)
#                        award2.aliases.append(award1)
#    if len(award1.abbrev_of) == 1:
#        award1.aliases.append(award1.abbrev_of[0])
#
##print(global_awards["Best TV Actor Drama"].aliases[0].freq)
##print(global_awards["Best Actor in a TV Drama"].aliases[0].freq)
##print(global_awards["Best Actor"].aliases[0].freq)
#
#for award_name in global_awards:
#    award = global_awards[award_name]
#    skip = False
#    if award.abbrev_of[1:]:
#        for awa in award.abbrev_of:
#            if awa.winner:
#                skip = True
#    if award.aliases:
#        for al in award.aliases:
#            if al.winner:
#                if al.freq > award.freq or (al.freq == award.freq and len(al.name) > len(award.name)):
#                    skip = True
#    if not skip and award.winner:
#        awin = max(award.winner, key=lambda key: award.winner[key])
#        print(award_name+": ")
#        print(awin)
#print("-----------------begin aliases BO")
#for x in global_awards["Best Original"].aliases:
#    print(x.name)
#    print(x.winner)
#print("-----------------begin aliases BOSMP")
#for x in global_awards["Best Original Song - Motion Picture"].aliases:
#    print(x.name)
#    print(x.winner)
#print("-----------------begin abbrevs BO")
#for x in global_awards["Best Original"].abbrev_of:
#    print(x.name)
#    print(x.winner)
#print("-----------------begin abbrevs BOSMP")
#for x in global_awards["Best Original Song - Motion Picture"].abbrev_of:
#    print(x.name)
#    print(x.winner)
#print(global_awards["Best Original Score"].abbrev_of)
#print(global_awards["Best Original Song"].abbrev_of)
#print(global_awards["Best Performance by an Actress in a Television Series - Musical or Comedy"].gist)

#for line in win_lines:
#    award_match = re.search('(?<=wins )[A-Z][A-Za-z]+( ([A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+',line)
#    winner_match = re.search('[A-Z][a-z]+( [A-Z][a-z]+)*(?= wins)',line)
#    award_match2 = re.search('(?<=takes home )[A-Z][A-Za-z]+( ([A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+',line)
#    winner_match2 = re.search('[A-Z][a-z]+( [A-Z][a-z]+)*(?= takes home)',line)
#    award_match3 = re.search('[A-Z][A-Za-z]+( ([A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+(?=[,]* goes to)',line)
#    winner_match3 = re.search('(?<=goes to )@[\w]+|[A-Z][a-z]+ [A-Z][a-z]+',line)
    #winner_match3 = re.search('(?<=goes to )@[\w]+',line)
    #match = re.search('((?<=wins )|(?<=winning ))[A-Z][A-Za-z]+( ([A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+',line)
    #match = re.search('(?<=win[a-z]*) [A-Z][A-Za-z]+( ([A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+',line)
    #match = re.search('win[a-z]* [A-Z][A-Za-z]+( ([A-Z][A-Za-z,]+|in|a|by|an|any|or|-))* [A-Z][A-Za-z]+',line)
    #if award_match != None:
    #    if award_match.group() in rough_award_names:
    #        rough_award_names[award_match.group()] += 1
    #    else:
    #        rough_award_names[award_match.group()] = 1
    #if winner_match != None:
    #    if winner_match.group() in rough_winner_names:
    #        rough_winner_names[winner_match.group()] += 1
    #    else:
    #        rough_winner_names[winner_match.group()] = 1
    #if award_match != None and winner_match != None:
    #    my_award = award_match.group()
    #    my_winner = winner_match.group()
    #    if my_award in awards_dict:
    #        if my_winner in awards_dict[my_award].winner:
    #            awards_dict[my_award].winner[my_winner] += 1
    #        else:
    #            awards_dict[my_award].winner[my_winner] = 1
    #    else:
    #        awards_dict[my_award] = Award(my_award)
    #        awards_dict[my_award].winner[my_winner] = 1
    #elif award_match2 != None and winner_match2 != None:
    #    my_award = award_match2.group()
    #    my_winner = winner_match2.group()
    #    if my_award in awards_dict:
    #        if my_winner in awards_dict[my_award]:
    #            awards_dict[my_award][my_winner] += 1
    #        else:
    #            awards_dict[my_award][my_winner] = 1
    #    else:
    #        awards_dict[my_award] = {my_winner : 1}
#for a in awards:
    #print(a.name+" was won by: "+a.winner+"\n")
#for a in awards_dict:
    #highest = max(awards_dict[a].winner, key=lambda key: awards_dict[a].winner[key])
    #highest_count = awards_dict[a].winner[highest]
    #print(a+": ")
    #print(highest+": ")
    #print(highest_count)
    #for oa in awards:
    #    if a.winner == oa.winner and a.name != oa.name:
    #        a.aliases.append(oa.name)
    #        oa.aliases.append(a.name)
            #if len(a.name) > len(oa.name):
            #    awards.remove(oa)
    #for pline in present_lines:
    #    if re.search(a, pline) != None:
    #        #presenter_matches = re.findall('[A-Z][a-z]+( [A-Z][a-z]+){1,2}',pline)
    #        presenter_matches = re.findall('@[\w]+|[A-Z][a-z]+ [A-Z][a-z]+',pline)
    #        award_part = False
    #        for pm in presenter_matches:
    #            for awa in awards_dict:
    #                if pm in awa:
    #                    award_part = True
    #            if award_part or pm == "@goldenglobes":
    #                pass
    #            elif pm in awards_dict[a].presenters:
    #                awards_dict[a].presenters[pm] += 1
    #            else:
    #                awards_dict[a].presenters[pm] = 1

#for a in awards_dict:
#    if len(awards_dict[a].presenters) > 0:
#        top_two = heapq.nlargest(2, awards_dict[a].presenters, key=awards_dict[a].presenters.get)
#        if len(top_two)>0 and top_two[0][0] == "@" and top_two[0] in handle2name:
#            top_two[0] = handle2name[top_two[0]]
#        if len(top_two)>1 and top_two[1][0] == "@" and top_two[1] in handle2name:
#            top_two[1] = handle2name[top_two[1]]
#        print(a+": ")
#        print(top_two)
        #highest = max(awards_dict[a].presenters, key=lambda key: awards_dict[a].presenters[key])
        #highest_count = awards_dict[a].presenters[highest]
        #print(highest+": ")
        #print(highest_count)
            
#for a in awards:
#    if len(a.aliases) > 0:
#        print(a.name+" has aliases: ")
#        pprint(a.aliases)
#        print('\n')
#        #print(a.aliases[0].name)

#award_names = [
#"Best Motion Picture - Drama",
#"Best Motion Picture - Comedy or Musical",
#"Best Actress in a Motion Picture - Drama",
#"Best Actor in a Motion Picture - Drama",
#"Best Performance By An Actress in a Motion Picture - Musical or Comedy",
#"Best Performance By An Actor in a Motion Picture - Musical or Comedy",
#"Best Performance by an Actress in a Supporting Role in any Motion Picture",
#"Best Supporting Actor in a Motion Picture",
#"Best Director - Motion Picture",
#"Best Screenplay - Motion Picture",
#"Best Motion Picture - Animated",
#"Best Foreign Film",
#"Best Original Score - Motion Picture",
#"Best Original Song - Motion Picture",
#"Best Television Series - Drama",
#"Best Television Series - Musical or Comedy",
#"Best Television Limited Series or Motion Picture Made for Television",
#"Best Actress in a Television Movie or Miniseries",
#"Best Actor in a Limited Series",
#"Best Performance by an Actor in a Limited Series or a Motion Picture Made for Television",
#"Best Performance by an Actress In A Television Series - Drama",
#"Best Performance by an Actor In A Television Series - Drama",
#"Best Performance by an Actress in a Television Series - Musical or Comedy",
#"Best Actor in a Television Series - Comedy or Musical",
#"Best Supporting Actress in a TV Movie, Series, or Miniseries",
#"Best Supporting Actor in a Television Series",
#"Cecil B. DeMille Award"
#]
#awards = []
#for award_name in award_names:
#    awards.append(Award(award_name))

#for b in blines:
    #myreg = r"Best( [A-Z][a-z]+)+"
    #ob = re.search('Best( ([A-Z][a-z]+)|in|a)+',b)
    #ob = re.search('Best([ \/]([A-Z][A-Za-z,]*|in|a|by|an|any|or|-))*[ \/][A-Z][a-z\/]+',b)
    #obb = re.findall('Best([ \/]([A-Z][a-z,]+|in|a|an|any|or|-))*[ \/][A-Z][a-z\/]+',b)
    #if ob != None:
    #    if ob.group() in adictt:
    #        adictt[ob.group()] += 1
    #    else:
    #        adictt[ob.group()] = 1
#for xxx in adictt:
#    if adictt[xxx] > 50:
        #print(xxx)
        #print(adictt[xxx])
#ended by:
# - punc except , - / but no preceding space (only 1 of each) maybe ()
# 
##for line in hlines:
    #names = re.findall('(?<=[ \"])[A-Z][A-Za-z ]+?(?=\'| [a-z])',line)
 ##   names = re.findall('[A-Z][A-Za-z ]+?(?=\'| [a-z])',line)
   ## for name in names:
    ##    if name in hdict:
      ##      hdict[name] += 1
        ##else:
          ##  hdict[name] = 1
#for line1 in lines:
    #names = re.findall('J[a-z]+ F[a-z]?(?=\'s)',line1)
    #names = re.findall('[A-Z][a-z]+ [A-Z][a-z]?(?=\')',line1)
#    apos = re.findall('[A-Z][a-z]+ [A-Z][a-z]+?(?=\'s [Gg]olden)',line1)
##for yy in hdict:
  ##  if hdict[yy] > 5 and ' ' in yy:
    ##    yn = yy.replace(' ', '')
      ##  yl = yy.lower()
        ##if yn in hdict:
         ##   hdict[yy] += hdict[yn]
            #del hdict[yn] 
##for line in hlines:
 ##   for yy in hdict:
   ##     if hdict[yy] > 5 and yy.lower().replace(' ', '') in line:
     ##       hdict[yy] += 1
            #del hdict[yn] 

#def get_names(s):
#    names = re.findall('[A-Z][a-z]+ [A-Z][a-z]+', s)

#aw = {}
#for award in awards:
#    for line in lines:
#        if award.name in line:
#    for wline in wlines:
#        if re.search(award, wline) != None:
#            nam = re.findall('[A-Z][a-z]+ [A-Z][a-z]+', wline)
#            for n in nam:
#                if n not in award and n in aw:
#                    aw[n] += 1
#                elif n not in award:
#                    aw[n] = 1
#for award in awards:
#    for wline in wlines:
#        if re.search(award, wline) != None:
#            nam = re.findall('[A-Z][a-z]+ [A-Z][a-z]+', wline)
#            for n in nam:
#                if n not in award and n in aw:
#                    aw[n] += 1
#                elif n not in award:
#                    aw[n] = 1

#pprint(aw)
#for x in hdict:
#    for y in hlines:
#        xy = re.search(x,y)
#        if xy != None:
#            if x in adict:
#                adict[x] != 1
#            else:
#                adict[x] = 1
#print("Host: "+max(hdict, key=lambda key: hdict[key]))
input("Press Enter to continue ...")
#presenter notes:
# - chopra and morgan are lone presenters
# - link barrymore and olyphant to canonical best award through winner traceeelissross
# how to link witherspoon:
# 1) equate tv and television
# 2) search for all awards at first off
# 3) search for award names not just as following "wins" but also "present"
