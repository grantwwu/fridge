def handler(event, context):


# GetItemsIntent

# Alexa, ask fridge helper what I have
#   You have ...


# AddItemIntent

# Alexa, tell fridge helper to add {number} {unit} of {item}
#   Taking picture...
#   Added <number> <unit> <item>

# Alexa, tell fridge helper to add {number} {item}
#   Taking picture...
#   Added <number> <item>

# Alexa, tell fridge helper to add some {item}
#   Taking picture and weighing item...
#   Added <weight> of <item>.


# RemoveItemIntent

# Alexa, tell fridge helper to remove {number} {units} of {item}
#   Removed <number> <units> of <item>

# Alexa, tell fridge helper to remove {number} {item}
#   Removed <number> <item>


# UpdateItemIntent

# Alexa, tell fridge helper I now have {number} {units} of {item}
#   Quantity of <item> updated to <number> <units>

# Alexa, tell fridge helper I now have {number} {item}
#   Quantity of <item> updated to <number>

# Alexa, ask fridge helper to update how much {item} I have
#   Updated weight of <item> to <number> kilograms


# DeleteItemIntent

# Alexa, tell fridge helper I'm out of {item}


# CheckExpirationFutureIntent

# Alexa, ask fridge helper what expires within the next {duration}
#   ... is expired.
#   ... will expire in <duration>.
#   etc.

# Alexa, ask fridge helper what expires soon (see above, with timespan of 1 week)


# CheckExpirationIntent

# Alexa, ask fridge helper what's expired (see above, with timespan of 0)


# CheckRunningLowIntent

# Alexa, ask fridge helper what I'm running out of.
#   You only have <>...


# Alexa, ask fridge helper can I make {recipe}?
#   You have everything you need to make <recipe>
#   OR
#   You are missing ...
