import requests
import os
import lob

google_key = os.environ["GOOGLE_API_KEY"]
lob.api_key = os.environ["LOB_API_KEY"]


class ApiError(Exception):
    pass


def get_user_info():
    """Displays prompts on command line and returns values for each line of
    sender's postal address and the body of their letter.
    """

    print ("\nLooks like you want to send a message to your Representative in "
           "Congress. Let's get started!")

    sender_name = raw_input("\nWhat's your full name? Type it, and then press "
                            "enter. \n\n")

    from_address_1 = raw_input("\nWhat's your street address? If you have an "
                               "apartment code or suite number, leave it out "
                               "for now: we'll get to it next. \n\n")

    from_address_2 = raw_input("\nOkay, if you have an apartment code or suite "
                               "number, enter it here. \n\n")

    from_city = raw_input("\nCity? \n\n")

    from_state = raw_input("\nState? Please capitalize and abbreviate, e.g., "
                           "CA for California. \n\n")

    from_zip = raw_input("\nZip Code? \n\n")

    letter_body = raw_input("\nGreat! Now, what would you like to say in the "
                            "body of your letter? \n\n")

    # FOR TESTING

    # sender_name = "RaeAnne Staab"
    # from_address_1 = "2531 North Routiers Avenue"
    # from_address_2 = ""
    # from_city = "Indianapolis"
    # from_state = "IN"
    # from_zip = "46219"
    # letter_body = "Thanks, Representative!"

    # sender_name = "Joe Schmoe"
    # from_address_1 = "185 Berry Street"
    # from_address_2 = "Suite 170"
    # from_city = "San Francisco"
    # from_state = "CA"
    # from_zip = "94107"
    # letter_body = "This is a test letter for Lob's coding challenge. "
    #                "Thank you legislator"

    # sender_name = "Eva Hesse"
    # from_address_1 = "1000 5th Avenue"
    # from_address_2 = ""
    # from_city = "New York"
    # from_state = "NY"
    # from_zip = "10028"
    # letter_body = "Hey Rep, fund the arts!"

    return sender_name, from_address_1, from_address_2, from_city, from_state, from_zip, letter_body


def get_civic_api_info(user_addr1, user_addr2, user_city, user_state):
    """Takes the first line, second line, city, and state of a mailing address
    provided by user and sends a request to the Google Civic Information API.
    Returns response object containing identifying information for all of the
    legislative officials corresponding to the address in the US government at
    all levels (national, state, municipal, etc.).
    """
    resp = requests.get('https://www.googleapis.com/civicinfo/v2/representative\
        s?key={}&address={}%20{}%20{}%20{}&prettyPrint'.format(google_key,
                                                               user_addr1,
                                                               user_addr2,
                                                               user_city,
                                                               user_state))
    # resp.json()[message] - ?
    if resp.status_code != 200:
        raise ApiError('Google CI: Error code %s. Reason: %s - %s' % (
            resp.status_code, resp.reason, resp.json()['error']['message']))
    return resp.json()


def extract_rep_info(response_object):

    for office in (response_object)['offices']:
        if office['name'].startswith("United States House of Representatives"):
            officials_ids = office['officialIndices']

    rep_name = ((response_object)['officials'])[(officials_ids[0])]['name']
    rep_address = ((response_object)['officials'])[(officials_ids[0])]['address']
    rep_addr1 = rep_address[0]['line1']
    rep_addr2 = rep_address[0].get('line2', "")
    rep_city = rep_address[0]['city']
    rep_state = rep_address[0]['state']
    rep_zip = rep_address[0]['zip']

    return rep_name, rep_addr1, rep_addr2, rep_city, rep_state, rep_zip


def create_sender_address(username,
                          address_line1,
                          address_line2,
                          user_city,
                          user_state,
                          user_zip):

    try:
        sender_address = lob.Address.create(
            name=user_name,
            description='Letter Generator User',
            address_line1=address_line1,
            address_line2=address_line2,
            address_city=user_city,
            address_state=user_state,
            address_country='US',
            address_zip=user_zip
        )

        return sender_address

    except Exception as e:
        raise ApiError("Error: " + str(e) + "\n\tAddress not created.")


def create_letter(letter,
                  sender_address,
                  recip_name,
                  recip_addr1,
                  recip_addr2,
                  recip_city,
                  recip_state,
                  recip_zip):

    try:
        lob.Letter.create(
            description='US House of Representatives Letter',
            to_address={
                'name': recip_name,
                'address_line1': recip_addr1,
                'address_line2': recip_addr2,
                'address_city': recip_city,
                'address_state': recip_state,
                'address_zip': recip_zip,
                'address_country': 'US'
            },
            from_address=sender_address,
            file='<html style="padding-top: 3in; margin: .5in;">'
                 + letter + '</html>',
            color=True
            )

        return letter

    except Exception as e:
        raise ApiError("Error: " + str(e) + "\n\tLetter not created.")

user_name, user_addr1, user_addr2, user_city, user_state, user_zip, letter_body = get_user_info()

response_object = get_civic_api_info(user_addr1,
                                     user_addr2,
                                     user_city,
                                     user_state)

rep_name, rep_addr1, rep_addr2, rep_city, rep_state, rep_zip = extract_rep_info(response_object)

user_address = create_sender_address(user_name,
                                     user_addr1,
                                     user_addr2,
                                     user_city,
                                     user_state,
                                     user_zip)

letter = create_letter(letter_body,
                       user_address,
                       rep_name,
                       rep_addr1,
                       rep_addr2,
                       rep_city,
                       rep_state,
                       rep_zip)

print "\nOkay, great: your letter is on its way!\n"
