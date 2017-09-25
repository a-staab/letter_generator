import requests


def get_user_info():
    """Displays prompts on command line and returns values for each line of
    sender's postal address and the body of their letter."""

    print "\n\nLooks like you're looking to send a message to your senator. \
    Let's get started!\n"

    sender_name = raw_input("What's your full name? Type it, and then press \
    enter. ")

    from_address_1 = raw_input("What's your street address? If you have an \
    apartment code or suite number, leave it out for now: we'll get to it \
    next. ")

    from_address_2 = raw_input("Okay, if you have an apartment code or suite \
    number, enter it here. ")

    from_city = raw_input("City? ")

    from_state = raw_input("State? Please capitalize and abbreviate, e.g., CA \
    for California. ")

    from_zip = raw_input("Zip Code? ")

    letter_body = raw_input("Great! Now, what would you like to say in the \
    body of your letter? ")

    return sender_name, from_address_1, from_address_2, from_city, from_state,
    from_zip, letter_body

print get_user_info()

# resp = requests.get('url_for_getting_senators_mailing_address')
# if resp.status_code != 200:
#     raise Civic_API_Error('GET /endpoint/ %s' % (resp.status_code))
# for address in resp.json():
#     # output in appropriate format




# From Name: Joe Schmoe
# From Address Line 1: 185 Berry Street
# From Address Line 2: Suite 170
# From City: San Francisco
# From State: CA
# From Zip Code: 94107
# Message: This is a test letter for Lob's coding challenge. Thank you legislator.
