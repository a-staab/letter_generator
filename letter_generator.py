import requests
import os
import lob


google_key = os.environ["GOOGLE_API_KEY"]
lob.api_key = os.environ["LOB_API_KEY"]


class ApiError(Exception):
    pass


def get_user_info():
    """Displays prompts on command line and returns values for each line of
    a postal address and the body of a letter provided by the user.
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

    return (sender_name,
            from_address_1,
            from_address_2,
            from_city,
            from_state,
            from_zip,
            letter_body)


def get_civic_api_info(user_addr1, user_addr2, user_city, user_state):
    """Takes the first line, second line, city, and state of a mailing address
    provided by user and sends a request to the Google Civic Information API.
    Returns response object containing identifying information for all of the
    legislative officials corresponding to the address in the US government at
    all levels (national, state, municipal, etc.).
    """
    resp = requests.get("https://www.googleapis.com/civicinfo/v2/representa"
                        "tives?key={}&address={}%20{}%20{}%20{}".format(
                            google_key, user_addr1, user_addr2, user_city,
                            user_state))

    if resp.status_code != 200:
        raise ApiError('Google CI: Error code %s. Reason: %s - %s' % (
            resp.status_code, resp.reason, resp.json()['error']['message']))
    return resp.json()


def extract_rep_info(response_object):
    """Takes a response object from the Google Civic API; returns the full name
    and first line, second line, city, state, and zip code for the address of
    the first House of Representatives member found in the response object.
    """

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
    """Takes a full name and the first line, second line, city, state, and zip
    code and sends a POST request to the Lob API to create an address. If
    successful, returns the corresponding, standardized address.
    """

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
    """Takes a string representing the body of a letter, a JSON string providing
    a return address, and the recipient's name and the first line, second line,
    city, state, and zip code of their mailing address; if successful, prints
    'Okay, great: your letter is on its way!'
    """

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

        print "\nOkay, great: your letter is on its way!\n"
        return letter

    except Exception as e:
        raise ApiError("Error: " + str(e) + "\n\tLetter not created.")


(
    user_name,
    user_addr1,
    user_addr2,
    user_city,
    user_state,
    user_zip,
    letter_body) = get_user_info()

response_object = get_civic_api_info(user_addr1,
                                     user_addr2,
                                     user_city,
                                     user_state)
(
    rep_name,
    rep_addr1,
    rep_addr2,
    rep_city,
    rep_state,
    rep_zip) = extract_rep_info(response_object)

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
