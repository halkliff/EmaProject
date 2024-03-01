# EmaProject NEO

Telegram-based **E**astern **M**edia **A**ssistant to manage content from image boards online.

## **Quick start**

* Install Poetry (latest version)
* Install the dependencies for all the packages inside the `./packages` folder with poetry

### **To startup locally with long polling**

* Change working directory to `./packages/bot-cloud-handler`
* Run the command: `$ poetry run start`
  * To start the bot in development (with auto restart), make sure to have Node (v16+) & npm installed, then run the command `$ npx nodemon --watch ./bot_cloud_handler --ext py --exec poetry run start`

### **To startup locally with Pub/Sub**

* Follow the instructions to [set up a local pub/sub emulator](https://cloud.google.com/pubsub/docs/emulator)
* Clone locally the [`Python Pubsub`](https://github.com/googleapis/python-pubsub) repository
* In `python-pubsub/samples/snippets`, install a new virtual environment (suggested to use [`virtualenv`](https://virtualenv.pypa.io/)) and activate it
* With the virtual environment activated, install the dependencies running the command `$ pip install -r requirements.txt`
* Run the command `python publisher.py <project_id> create <topic_id>` to create a new topic, and don't forget to set this topic in the cloud handler!
* Run the command `python subscriber.py <project_id> create-push <topic_id> <subscription_id> http://localhost:8080` to create a new subscription
* Deploy the Handler [locally with functions framework](https://cloud.google.com/functions/docs/running/function-frameworks) by running the command `functions-framework --target=bot_cloud_handler --signature-type=cloudevent`
* start the events dispatcher in `packages/bot-event-dispatcher` directory with the command `$ poetry run start-dev`
