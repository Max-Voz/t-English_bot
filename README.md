# t-English bot


This bot was developed for giving an information about t-English school and allows to send an application for the
 certain course.
It sends an application via Gmail and writes all the information into a Google Spreadsheet.
Bot can be found at [t.me/t_english_bot](https://t.me/t_english_bot)
____
## It requires files:
- bot_token.txt - file with a token for Telegram bot;
- google_api/credentials.json - file with credentials, received in
 [developers.google.com](https://developers.google.com/) 
____
## It creates files:
- app.log - log file for an application
- user.csv - .csv file with all applications
- google_api/token.pickle - oauth2 file
- google_api/sprsh_link.txt - file with links to a Google spreadsheets