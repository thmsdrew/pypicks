#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
import re
import requests
import sys

def scrape_picks():
    url = 'http://nflpickwatch.com/2016-nfl-expert-picks-results/?text=1'
    
    print 'Getting initial scrape... (' + url + ')'
    page = requests.get('http://nflpickwatch.com/2016-nfl-expert-picks-results/?text=1')
    tree = html.fromstring(page.content)
    everything = tree.xpath('//table[@id="resultsTable"]//thead//td[@width="37px"]')

    scraped_matchups = []
    scraped_consensus = []
    
    for e in everything:
        if "@" in e.text_content():
            scraped_matchups.append(e.text_content())
        elif "%" in e.text_content():
            scraped_consensus.append(e.text_content())

    unsorted_consensus = []
    for c in scraped_consensus:
        match = re.match(r"([a-z]+)([0-9]+)", c, re.I)
        unsorted_consensus.append(match.groups())
    
    sorted_consensus = sorted(unsorted_consensus, key=lambda x: x[1])

    final_picks = []
    points = 1
    for pick in sorted_consensus:
        for index, matchup in enumerate(scraped_matchups):
            if pick[0] in matchup:
                scraped_matchups.pop(index) # pop the value out to speed up on subsequent loops
                break
        winner = pick[0]
        percent = pick[1]
        final_picks.append([points, matchup, winner, percent])
        points += 1
    
    return final_picks

def print_picks(picks):
    print 'Points\tMatchup\tWinner\tConsensus'
    print '---------------------------------'
    for pick in picks:
        print str(pick[0]) + '\t' + pick[1] + '\t' + pick[2] + '\t' + '(' + pick[3] + '%)'

def user_input(picks):
    command = raw_input('\nEnter a command... (exit, swap, flip, ags, print, help)\n> ')
    if command == 'exit' or command == 'quit':
        sys.exit(0)
    elif command.index('swap') if 'swap' in command else None == 0:
        split_command = command.split()
        if len(split_command) != 3:
            print 'invalid swap usage'
        user_input(picks)
    elif command.index('flip') if 'flip' in command else None == 0:
        print 'flip'
        user_input(picks)
    elif command.index('ags') if 'ags' in command else None == 0:
        print 'ags'
        user_input(picks)
    elif command == 'help':
        print 'help'
        user_input(picks)
    elif command == 'print':
        print 'Here are your picks...\n'
        print_picks(picks)
        user_input(picks)
    else:
        print 'command not recognized'
        user_input(picks)

def main():
    picks = scrape_picks()
    print 'Here are your picks...\n'
    print_picks(picks)
    user_input(picks)

if __name__ == "__main__":
    main()