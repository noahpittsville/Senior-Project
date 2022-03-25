from TwitterMenu import *
def main():
    run_main_menu = True
    while run_main_menu == True:
        print('[1] Twitter Scraper\n'
              '[2] Stock Scraper')
        menu_choice = int(input("Enter a menu number: "))
        if menu_choice == 0:
            run_main_menu = False
            return
        elif menu_choice == 1:
            twitterMenu()
        elif menu_choice == 2:
            makeDataTable('UserTimeline')
        else:
            print('Try again.')
main()
exit(1)