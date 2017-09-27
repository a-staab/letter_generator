import requests
import os
import lob

google_key = os.environ["GOOGLE_API_KEY"]
lob.api_key = os.environ["LOB_API_KEY"]


def get_user_info():
    """Displays prompts on command line and returns values for each line of
    sender's postal address and the body of their letter."""

    # print ("\nLooks like you're looking to send a message to your senator. "
    #        "\nLet's get started!")

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

    sender_name = "Joe Schmoe"
    from_address_1 = "185 Berry Street"
    from_address_2 = "Suite 170"
    from_city = "San Francisco"
    from_state = "CA"
    from_zip = "94107"
    letter_body = "This is a longer message. It's longer. So much longer. OMG LONGER. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,"

    # sender_name = "Eva Hesse"
    # from_address_1 = "1000 5th Avenue"
    # from_address_2 = ""
    # from_city = "New York"
    # from_state = "NY"
    # from_zip = "10028"
    # letter_body = "Hey, fund the arts!"

    return sender_name, from_address_1, from_address_2, from_city, from_state, from_zip, letter_body


def get_civic_api_info(user_addr1, user_addr2, user_city, user_state):
# headers = {' ': ' '} (if passing, add as argument after URL)
    resp = requests.get('https://www.googleapis.com/civicinfo/v2/representatives?key={}&address={}%20{}%20{}%20{}&prettyPrint'.format(google_key, user_addr1, user_addr2, user_city, user_state))
    # resp.json()[message] - ?
    if resp.status_code != 200:
        raise ApiError('Google CI: Error code %s. Reason: %s - %s' % (resp.status_code, resp.reason, resp.json()['error']['message']))
    return resp.json()


user_name, user_addr1, user_addr2, user_city, user_state, user_zip, letter_body = get_user_info()
response_object = get_civic_api_info(user_addr1, user_addr2, user_city, user_state)


def extract_rep_info(response_object):
    # verified_user_address = response_object['normalizedInput']

    for office in (response_object)['offices']:
        if office['name'].startswith("United States House of Representatives"):
            officials_ids = office['officialIndices']

    rep_name = ((response_object)['officials'])[(officials_ids[0])]['name']
    rep_address = ((response_object)['officials'])[(officials_ids[0])]['address']
    rep_addr1 = rep_address[0]['line1']
    rep_city = rep_address[0]['city']
    rep_state = rep_address[0]['state']
    rep_zip = rep_address[0]['zip']

    return rep_name, rep_addr1, rep_city, rep_state, rep_zip

rep_name, rep_addr1, rep_city, rep_state, rep_zip = extract_rep_info(response_object)


def create_sender_address(username, address_line1, address_line2, user_city, user_state, user_zip):

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

user_address = create_sender_address(user_name, user_addr1, user_addr2, user_city, user_state, user_zip)


def create_letter(letter, sender_address, recip_name, recip_addr1, recip_city, recip_state, recip_zip):

    lob.Letter.create(
        description='US House of Representatives Letter',
        to_address={
            'name': recip_name,
            'address_line1': recip_addr1,
            'address_city': recip_city,
            'address_state': recip_state,
            'address_zip': recip_zip,
            'address_country': 'US'
        },
        from_address=sender_address,
        file='<html style="padding-top: 3in; margin: .5in;">' + letter + '</html>',
        color=True
        )

    return letter

letter = create_letter(letter_body, user_address, rep_name, rep_addr1, rep_city, rep_state, rep_zip)
print letter


class ApiError(Exception):
    pass
