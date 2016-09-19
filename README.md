
## Email Publishing

This is a prototype to determine whether we can feasibly allow users
to deliver series data by email.

Users will be emailed before a dataset is due for update.  The user will
be prompted to reply to the email including the URL that points to the
new data file (later, perhaps we can try attachments too).

If a user sends an email to the address without replying to a notification
email then they will receive a schedule of releases that are due.


### Installation

1. Create a virtualenv
2. Clone this repo
3. ```pip install -r requirements.txt```
4. Copy sample_config.yml to config.yml
5. Edit config.yml


### Running the prototype

Before running either of the command below, you should set an environment variable
which points to your config file, such as:

```bash
export EMAIL_PUB_CONFIG=config.yml
```

#### Sending notifications

To send notifications, you should use the ```notify``` command which is installed in your virtualenv

#### Handling responses

To handles responses, you should use the ```respond``` command which is installed in your virtualenv