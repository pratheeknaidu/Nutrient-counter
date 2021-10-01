const subscriptionName = 'gcp-images-sub';
const timeout = 60;

// Imports the Google Cloud client library
const {PubSub} = require('@google-cloud/pubsub');
const { response } = require('express');

// Creates a client; cache this for further use
const pubSubClient = new PubSub();

let getMessages = {};

getMessages.messages = new Map();

getMessages.listenWithCustomAttributes = (req, res, next) => {
  // References an existing subscription, e.g. "my-subscription"
  const subscription = pubSubClient.subscription(subscriptionName);

  // Create an event handler to handle messages
  const messageHandler = message => {
    console.log(
      `Received message: id ${message.id}, data ${
        message.data
      }, attributes: ${JSON.stringify(message.attributes)}`
    );
    console.log("messages image_name")
    getMessages.messages.set(message.attributes.image_name, message.attributes.calorie_values)
    console.log("messages map")
    console.log(getMessages.messages)


    // "Ack" (acknowledge receipt of) the message
    message.ack();
  };

  // Listen for new messages until timeout is hit
  subscription.on('message', messageHandler);
}

module.exports = getMessages;