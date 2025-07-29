# 🌂 UmbrellaReminder

- ***Some kid*** always forgets to bring an umbrella.

UmbrellaReminder is a simple Python automation tool that checks the daily weather forecast and sends a friendly email reminder if rain is expected. Designed to help ***some kid*** remember to bring an umbrella before leaving home.

---

##### Run automatically every day at 8 AM using a cron job or Task Scheduler.
Change the path in [ ] to yours.
```bash
crontab -e
0 7 * * * [*/python (YOUR Interpreter path)] [*main.py] >> [*/logs/daily.log] 2>&1
crontab -l
crontab -r
```