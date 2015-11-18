/**
    Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.amazon.com/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

/**
 * This simple sample has no external dependencies or session management, and shows the most basic
 * example of how to create a Lambda function for handling Alexa Skill requests.
 *
 * Examples:
 * One-shot model:
 *  User: "Alexa, ask Space Geek for a space fact"
 *  Alexa: "Here's your space fact: ..."
 */

/**
 * App ID for the skill
 */
var APP_ID = undefined; //replace with "amzn1.echo-sdk-ams.app.[your-unique-value-here]";

/**
 * Array containing space facts.
 */
/**
 * The AlexaSkill prototype and helper functions
 */
var AlexaSkill = require('./AlexaSkill');

/**
 * Fridge is a child of AlexaSkill.
 * To read more about inheritance in JavaScript, see the link below.
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Introduction_to_Object-Oriented_JavaScript#Inheritance
 */
var Fridge = function () {
    AlexaSkill.call(this, APP_ID);
};

// Extend AlexaSkill
Fridge.prototype = Object.create(AlexaSkill.prototype);
Fridge.prototype.constructor = Fridge;

Fridge.prototype.eventHandlers.onSessionStarted = function (sessionStartedRequest, session) {
    console.log("Fridge onSessionStarted requestId: " + sessionStartedRequest.requestId
        + ", sessionId: " + session.sessionId);
    // any initialization logic goes here
};

Fridge.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
    console.log("Fridge onLaunch requestId: " + launchRequest.requestId + ", sessionId: " + session.sessionId);
    handleNewFactRequest(response);
};

/**
 * Overridden to show that a subclass can override this function to teardown session state.
 */
Fridge.prototype.eventHandlers.onSessionEnded = function (sessionEndedRequest, session) {
    console.log("Fridge onSessionEnded requestId: " + sessionEndedRequest.requestId
        + ", sessionId: " + session.sessionId);
    // any cleanup logic goes here
};

Fridge.prototype.intentHandlers = {
   GetItemsIntent: function (intent, session, response) {
        handleGetItemsRequest(response);
    },

    AddItemIntent: function (intent, session, response) {
        response.ask("Sorry, Professor Black, this function is currently not implemented.");
    },

    HelpIntent: function (intent, session, response) {
        response.ask("You can ask Fridge to add an item, or to list the items available.");
    }
};


var baseUrl = "http://15291laptop.wv.cc.cmu.edu:5000/"

function handleGetItemsRequest(response) {
  /* var itemResponse = new XMLHttpResponse();
  itemResponse.open( "GET", baseURL + "items", false);
  itemResponse.send(null);
  var items = JSON.parse(itemResponse.responseText);

  var speechOutput = "Here's what's in your fridge: ";
  for (var i = 0; i < items.length; i++)
  {
    item = items[i];
    speechOutput = speechOutput + item["amount"] + " " + item["unit"] + " of " + item["label"];
  } */

  response.tellWithCard("Test", "Fridge", "Test");
}
// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the Fridge skill.
    var fridge = new Fridge();
    fridge.execute(event, context);
};

