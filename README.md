# Automated-Speed-Test
I noticed that my internet connection increases whenever I use speed test, So, I created an automated speed test. 
Now everytime I use my laptop or computer, the internet speed will increase.

## How the program works?
When scheduled on startup via linux or task scheduler, the program will run speed test using Netflix's Fast.com on the background everytime you use your computer.
It will open chrome then adjust the settings to run speed test on 7 - 8 parallel connections for 5 mins. 
The speed test result will be recorded into a log file. The program covers 24-hour period and will run during startup 
so you can enjoy "maximized" internet connection.



