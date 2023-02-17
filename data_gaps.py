import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search script',
            add_help=True)

    parser.add_argument('--company_id', dest='company_id', required=True)
    parser.add_argument('--serial', dest='serial', required=True)
    parser.add_argument('--device_type', dest='device_type', required=True)
    parser.add_argument('--timezone', dest='timezone', required=True)
    parser.add_argument('--company_slug', dest='company_slug', required=True)
    parser.add_argument('--fr', dest='fr', required=True)
    parser.add_argument('--to', dest='to', required=True)
    #parser.add_argument('--env', dest='env')
    
    args = parser.parse_args()

    search = 'search --env production --company {} --serials {} --tz {} --from \"{}\" --to \"{}\" --token_file /Users/gustafgroning/.ssh/bo_token'.format(
        args.company_slug, args.serial, args.timezone, args.fr, args.to)


#   URL HANDLING
#    print(str(args.fr))
    from_for_url = str(args.fr).replace("-", "/")
    from_no_time = from_for_url.split(" ")[0]
    
    to_for_url = str(args.to).replace('-', '/')
    to_no_time = to_for_url.split(" ")[0]
#    print(from_no_time, to_no_time)

    URL = 'sigicom.infralogin.com/boapi/v0/company/{}/device/{}/{}/spool/date/from/{}/to/{}/action/republish'.format(
        args.company_id, args.device_type, args.serial, from_no_time, to_no_time 
    )
    
    print('\n')
    print(search,)
    print('\n')
    print(URL)
    


# sigicom.infralogin.com/boapi/v0/company/COMPANY_ID/device/DEVICE_TYPE/SERIAL_NUMBER/spool/date/from/YYYY/MM/DD/to/YYYY/MM/DD

# search --env ENV --company COMPANY_SLUG --serials DEVICE_NUMBER --tz TIMEZONE --from "YYYY-MM-DD HH:MM" --to "YYYY-MM-DD HH:MM" --token_file BO_TOKEN_FILE_PATH
# search --env production --token_file ~/.ssh/bopass --from "2022-12-14 00:00" --to "2022-12-14 23:59" --tz "Europe/Copenhagen" --timer true --company cptestdk --draw true --serials 10926

# python3 data_gaps.py --timezone --serial --company_slug --fr "" --to "" --company_id --device_type 


# GABBES
# search --env production --token_file ~/.ssh/bopass --from "2023-01-03 07:00" --to "2023-01-03 10:00" --tz "America/Toronto" --timer true --company soldataus --draw true --serials 110195
# MINE
# search --env production --company soldataus --serials 110195 --tz America/Toronto --from "2023-01-03 08:00" --to "2023-01-03 09:00" --token_file /Users/gustafgroning/.ssh/bo_token

