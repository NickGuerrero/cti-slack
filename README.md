# CTI Slack App: MyCTI
Goal: Create a Slack Interface to grant data system access to students
* Slack GUI where students can view and edit their records
* Distribute notifications and reminder more programmatically

### Development Notes:
* Uses Slack Bolt (Python + Flask + Gunicorn)
  * The Flask adapter is used since the sample seems more up to date
    * We could change adapters later (e.g. FastAPI), more research could be done to ensure compatability
  * Gunicorn is currently configured with a basic sync worker
    * Once we have a better idea on what works for Slack bolt, we can modify this too