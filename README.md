# 🌂 UmbrellaReminder

- ***Some kid*** always forgets to bring an umbrella.

UmbrellaReminder is a simple Python automation tool that checks the daily weather forecast and sends a friendly email reminder if rain is expected. Designed to help ***some kid*** remember to bring an umbrella before leaving home.

---

#### UmbrellaReminder GitHub Actions Workflow
```yaml
on:
  schedule:
    - cron: '30 5 * * *'
  workflow_dispatch:
```