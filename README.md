# Automated-Speed-Test
I noticed that my internet connection increases whenever I use speed test, 
So, I created an automated speed test everytime I used my laptop or computer because it increases my internet speed

## How the program works?
When scheduled on startup via linux or task scheduler, the program will run speed test using Netflix's Fast.com on the background everytime you use your computer.
It will open chrome, run speed test after adjusting the settings, and run speed test on 7 - 8 paralled connections for 5 mins. 
Then, the speed test result will recorded into a log file. The program covers 24-hours period and will run during startup 
so you can enjoy "maximized" internet connection.



