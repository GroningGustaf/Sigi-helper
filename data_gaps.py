import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search script',
            add_help=True)

    parser.add_argument('--company_id', dest='company_id', required=True)
    parser.add_argument('--serial', dest='serial', required=True)
    parser.add_argument('--device_type', dest='device_type')
    parser.add_argument('--timezone', dest='timezone', required=True)
    parser.add_argument('--company_slug', dest='company_slug', required=True)
    # parser.add_argument('--env', dest='env')
    parser.add_argument('--fr', dest='fr', required=True)
    parser.add_argument('--to', dest='to', required=True)
    
    args = parser.parse_args()

    search = 'search --env production --company {} --serials {} --tz {} --from \"{}\" --to \"{}\" --token_file /Users/gustafgroning/.ssh/bo_token'.format(
        args.company_slug, args.serial, args.timezone, args.fr, args.to)


#   URL HANDLING
    from_for_url = str(args.fr).replace("-", "/")
    from_no_time = from_for_url.split(" ")[0]

    to_for_url = str(args.to).replace('-', '/')
    to_no_time = to_for_url.split(" ")[0]
    print(from_no_time, to_no_time)

    URL = 'sigicom.infralogin.com/boapi/v0/company/{}/device/{}/{}/spool/date/from/{}/to/{}'.format(
        args.company_id, args.device_type, args.serial, from_no_time, to_no_time 
    )
    
    print('\n')
    print('search string:', search,)
    print('\n')
    print("URL string:", URL)
    


# sigicom.infralogin.com/boapi/v0/company/COMPANY_ID/device/DEVICE_TYPE/SERIAL_NUMBER/spool/date/from/YYYY/MM/DD/to/YYYY/MM/DD

# search --env ENV --company COMPANY_SLUG --serials DEVICE_NUMBER --tz TIMEZONE --from "YYYY-MM-DD HH:MM" --to "YYYY-MM-DD HH:MM" --token_file BO_TOKEN_FILE_PATH