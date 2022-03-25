from TwitterScraper import *

def twitterMenu():
    in_menu = True
    while in_menu == True:
        print('[0] Go Back\n'
              '[1] Livestream data\n'
              '[2] Query data')
        menu_choice = int(input('Enter a Menu Number: '))
        if menu_choice == 0:
            in_menu = False
            return
        elif menu_choice == 1:
            tmenuOne()
        elif menu_choice == 2:
            tmenuTwo()
        else:
            print('Try again.')

# LIVESTREAM
def tmenuOne():
    in_menu_one = True
    while in_menu_one == True:
        print('[0] Go Back\n'
              '[1] Run\n'
              '[2] Option 2')
        menu_choice = int(input('Enter a Menu Number: '))
        if menu_choice == 0:
            in_menu_one = False
            return
        elif menu_choice == 1:
            #exec(open("TwitterScraperLivestream.py").read())
            TwitterLiveStream('keywords')
        elif menu_choice == 2:
            print('TODO')
        else:
            print('Try again.')

# QUERY
def tmenuTwo():
    in_menu_two = True
    while in_menu_two == True:
        print('[0] Go Back\n'
              '[1] Home Timeline\n'
              '[2] User Timelines\n'
              '[3] Filter by Usernames\n'
              '[4] Filter by Hashtags\n'
              '[5] Filter by Keywords')
        menu_choice = int(input('Enter a Menu Number: '))
        if menu_choice == 0:
            in_menu_two = False
            return
        elif menu_choice == 1:
            trunMenu('HomeTimeline')
        elif menu_choice == 2:
            trunMenu('UserTimeline')
        elif menu_choice == 3:
            trunMenu('UserKeywords')
        elif menu_choice == 4:
            trunMenu('HashtagKeywords')
        elif menu_choice == 5:
            trunMenu('SearchKeywords')
        else:
            print('Try again.')


def trunMenu(element):
    run_menu = True
    while run_menu == True:
        print('[0] Go Back\n'
              '[1] Configure Settings\n'
              '[2] Run')
        menu_choice = int(input('Enter a Menu Number: '))
        if menu_choice == 0:
            run_menu = False
            return
        elif menu_choice == 1:
            tconfigureSettings(element)
        elif menu_choice == 2:
            makeTable(element)
            print('{}.csv updated.'.format(element))
        else:
            print('Try again.')

def tconfigureSettings(element):
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    in_configure_settings = True
    while in_configure_settings == True:
        print('[0] Go Back\n'
              '[1] Set Grab Limit (Current: {})'.format(grab_limit))
        if element == 'SearchKeywords':
            print('[2] Edit Keyword List')
        if element == 'HashtagKeywords':
            print('[2] Edit Hashtag List (#)')
        if element == 'UserKeywords':
            print('[2] Edit User List (@)')
        if element == 'UserTimeline':
            print('[2] Edit User Timeline List')
        menu_choice = int(input('Enter a Menu Number: '))
        if menu_choice == 0:
            in_configure_settings = False
            return
        elif menu_choice == 1:
            grab_limit = int(input('Set Grab Limit: '))
            setSettings('settings', 'limit', grab_limit, 'set')
        elif menu_choice == 2:
            if element == 'SearchKeywords':
                tsearchMenu('Keyword')
            if element == 'HashtagKeywords':
                tsearchMenu('Hashtag')
            if element == 'UserKeywords':
                tsearchMenu('User')
            if element == 'UserTimeline':
                tsearchMenu('UserTimeline')
        else:
            print('Try again.')

def tsearchMenu(search_type):
    in_keyword_menu = True
    while in_keyword_menu == True:
        grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
        print('[0] Go Back\n'
              '[1] List {}s\n'
              '[2] Add\n'
              '[3] Delete'.format(search_type))
        menu_choice = int(input('Enter a Menu Number: '))
        if menu_choice == 0:
            in_keyword_menu = False
            return
        elif menu_choice == 1:
            if search_type == 'Keyword':
                print(keywords)
            if search_type == 'Hashtag':
                print(hashtags)
            if search_type == 'User':
                print(usernames)
            if search_type == 'UserTimeline':
                print(timeline)
        elif menu_choice == 2:
            value = input('Add {}: '.format(search_type))
            if search_type == 'Keyword':
                setSettings('search', 'key', str(value), 'add')
            if search_type == 'Hashtag':
                setSettings('search', 'hash', str(value), 'add')
            if search_type == 'User':
                setSettings('search', 'user', str(value), 'add')
            if search_type == 'User Timeline':
                setSettings('search', 'user_timeline', str(value), 'add')
        elif menu_choice == 3:
            value = input('Delete {}: '.format(search_type))
            if search_type == 'Keyword':
                setSettings('search', 'key', str(value), 'delete')
            elif search_type == 'Hashtag':
                setSettings('search', 'hash', str(value), 'delete')
            elif search_type == 'User':
                setSettings('search', 'user', str(value), 'delete')
            elif search_type == 'User Timeline':
                setSettings('search', 'user_timeline', str(value), 'delete')
        else:
            print('Try again.')