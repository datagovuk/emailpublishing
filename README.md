
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
3. python setup.py develop
4. ```pip install -r requirements.txt```
5. Copy sample_config.yml to config.yml
6. Edit config.yml


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

#### Testing template generation

To test how the HTML emails look, there is a command that can be run that will generate a test email (per template paid) and send it to the specified address

```bash
test_templates --to my@mail.com
```

### Security

As email isn't very secure, and it is possible to some degree to fake the sender we have to take
extra steps to make sure the user is allowed to publish data.

If someone were to fake the email address of a user, to obtain a schedule, we haven't really
leaked anything and so it is probably not a problem.

If someone were to fake the email address of the user and know how to build a target address for
publishing data, then that clearly is a problem.

#### TODO:

 * ~~Add a token to all outgoing notification emails so that we can see if we get it back in the response.~~
 * Make sure we tell users after we have added a data file so they can check.
 * Time limit the replies
 * Check DKIM/SPF etc to make sure the email server is also confident on who the sender is.






