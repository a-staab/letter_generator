import requests
import os
import pprint


google_key = os.environ["API_KEY"]


def get_user_info():
    """Displays prompts on command line and returns values for each line of
    sender's postal address and the body of their letter."""

    print ("\nLooks like you're looking to send a message to your senator. "
           "\nLet's get started!")

    # sender_name = raw_input("\nWhat's your full name? Type it, and then press"
    #                         " enter. ")

    # from_address_1 = raw_input("\nWhat's your street address? If you have an"
    #                            " apartment code or suite number, leave it out"
    #                            " for now: we'll get to it next. ")

    # from_address_2 = raw_input("\nOkay, if you have an apartment code or suite"
    #                            " number, enter it here. ")

    # from_city = raw_input("\nCity? ")

    # from_state = raw_input("\nState? Please capitalize and abbreviate, e.g., CA"
    #                        " for California. ")

    # from_zip = raw_input("\nZip Code? ")

    # letter_body = raw_input("\nGreat! Now, what would you like to say in the"
    #                         " body of your letter? ")

    # FOR TESTING

    # sender_name = "RaeAnne Staab"
    # from_address_1 = "2531 North Routiers Avenue"
    # from_address_2 = ""
    # from_city = "Indianapolis"
    # from_state = "IN"
    # from_zip = "46219"
    # letter_body = "Thanks, Mayor!"

    # sender_name = "Joe Schmoe"
    # from_address_1 = "1510 North Street"
    # from_address_2 = "Suite 170"
    # from_city = "San Francisco"
    # from_state = "CA"
    # from_zip = "91101"
    # letter_body = "Thanks Lob!"

    sender_name = "Eva Hesse"
    from_address_1 = "1000 5th Avenue"
    from_address_2 = ""
    from_city = "New York"
    from_state = "NY"
    from_zip = "10028"
    letter_body = "Hey, fund the arts!"

    return sender_name, from_address_1, from_address_2, from_city, from_state, from_zip, letter_body


def get_all_rep_info(user_addr1, user_addr2, user_city, user_state):
# headers = {' ': ' '} (if passing, add as argument after URL)
    resp = requests.get('https://www.googleapis.com/civicinfo/v2/representatives?key={}&address={}%20{}%20{}%20{}&prettyPrint'.format(google_key, user_addr1, user_addr2, user_city, user_state))
    # resp.json()[message] - ?
    if resp.status_code != 200:
        raise ApiError('Google CI: Error code %s. Reason: %s - %s' % (resp.status_code, resp.reason, resp.json()['error']['message']))
    return resp.json()


class ApiError(Exception):
    pass

user_name, user_addr1, user_addr2, user_city, user_state, user_zip, letter_body = get_user_info()
response_object = get_all_rep_info(user_addr1, user_addr2, user_city, user_state)

verified_user_address = response_object['normalizedInput']

for office in (response_object)['offices']:
    # if office['name'] == "Mayor":
    if office['name'].startswith("United States House of Representatives"):
        officials_ids = office['officialIndices']

# neg_offset = 0
# for office in (response_object)['offices']:
#     if len(office['officialIndices']) > len(index_list) and office['officialIndices'][-1] < index_list[0]:
#         for item in range(len(office['officialIndices']) - 1):
#             neg_offset += 1

# pprint.pprint((response_object)['officials'])

pprint.pprint(((response_object)['officials'])[(officials_ids[0])])

# for office in rep_info['offices']:
#     if rep_info['offices']['name'] == 'Mayor':
#         print rep_info['offices']['officialIndices']

# From Name: Joe Schmoe
# From Address Line 1: 185 Berry Street
# From Address Line 2: Suite 170
# From City: San Francisco
# From State: CA
# From Zip Code: 94107
# Message: This is a test letter for Lob's coding challenge. Thank you legislator.
