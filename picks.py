#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
import re
import requests
import sys

def scrape_picks():
    url = 'http://nflpickwatch.com/?text=1'

    print 'Getting initial scrape... (' + url + ')'
    page = requests.get(url)
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

def validate_swap(first, second, num_picks):
    valid = False
    if first.isdigit() and second.isdigit():
        if int(first) <= num_picks and int(first) >= 1 and int(second) <= num_picks and int(second) >= 1:
            valid = True
    if valid == False:
        print 'Invalid arguments for swap, must be two numbers between 1 and ' + str(num_picks)
    return valid

def swap(first, second, picks):
    first_idx = int(first) - 1
    second_idx = int(second) - 1
    first_pick = picks[first_idx]
    second_pick = picks[second_idx]
    # swap picks
    picks[second_idx] = first_pick
    picks[first_idx] = second_pick
    # correct the assigned points
    picks[first_idx][0] = first
    picks[second_idx][0] = second
    return picks

def validate_flip(arg, num_picks):
    valid = False
    if arg.isdigit():
        if int(arg) >= 1 and int(arg) <= num_picks:
            valid = True
    if valid == False:
        print 'Invalid arguments for flip, must be one number between 1 and ' + str(num_picks)
    return valid

def flip(arg, picks):
    flip_idx = int(arg) - 1
    print flip_idx
    pick = picks[flip_idx][2]
    print pick
    split_matchup = picks[flip_idx][1].split('@')
    print split_matchup
    for team in split_matchup:
        if pick != team:
            picks[flip_idx][2] = team
    return picks

def validate_ags(arg, num_picks):
    

def user_input(picks):
    command = raw_input('\nEnter a command... (exit, swap, flip, ags, print, help)\n> ')
    if command == 'exit' or command == 'quit':
        sys.exit(0)
    elif command.startswith('swap'):
        split_command = command.split()
        if len(split_command) != 3:
            print 'invalid swap usage'
        else:
            if validate_swap(split_command[1], split_command[2], len(picks)):
                picks = swap(split_command[1], split_command[2], picks)
                print_picks(picks)
        user_input(picks)
    elif command.startswith('flip'):
        split_command = command.split()
        if len(split_command) != 2:
            print 'invalid flip usage'
        else:
            if validate_flip(split_command[1], len(picks)):
                picks = flip(split_command[1], picks)
                print_picks(picks)
        user_input(picks)
    elif command.startswith('ags'):
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
