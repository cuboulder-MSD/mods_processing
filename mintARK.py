import requests, json, csv, sys, uuid
from datetime import datetime

def chooseURL():
    urls = {"prod": "https://libapps.colorado.edu/ark:/", "test": "https://test-libapps.colorado.edu/ark:/"}
    user_response = input("Do you want to run on prod or test? [prod/test]").lower()
    if user_response not in urls:
        raise RuntimeError("%s is not a valid env" % user_response)

    url = urls[user_response]
    return url

    # return ark


def getARK(url, luna_url, title, rights, type, user, batchRef, date):
    auth_token = ''


    data={"resolve_url": luna_url , "batch_ref": batchRef, "date_minted": date, "metadata":{"mods": {"titleInfo":[{"title": title}],"typeOfResource": type, "accessCondition": rights}},"generated_by": user,"status": "active"}
    # print(data)

    headers={"Content-Type":"application/json","Authorization":"Token " + auth_token}

    req= requests.post(url,json.dumps(data),headers=headers)

    rjson = req.json()

    print(req.json())

    ark = rjson['results'][0]['ark']

    return ark
    # print(ark)


def main():
    # Grab our infile_path and outfile_path from the cli
    infile_path = sys.argv[1]
    outfile_path = sys.argv[2]

    with open(infile_path, newline='' ) as csvfile, open(outfile_path, "w") as outfile:
         reader = csv.DictReader(csvfile)
         fields = reader.fieldnames
         fields.append('Identifier ARK')
         writer = csv.DictWriter(outfile, fieldnames=fields)
         writer.writeheader()
         user = input("who are you?").lower()
         batchRef = input('give me a collection reference (e.g. snow, nsidc, zss, bent-hyde)') + '_' + str(uuid.uuid4())
         date = datetime.today().strftime('%Y-%m-%d')


         url = chooseURL()

         for row in reader:

             luna_url = row['lnexp_PAGEURL']
             title = row['Title#1']
             rights = row['Access Condition#1']
             type = row['Type of Resource#1']

             ark = getARK(url, luna_url, title, rights, type, user, batchRef, date)
             row['Identifier ARK'] = 'https://ark.colorado.edu/ark:/' + ark
             writer.writerow(row)


# make this a safe-ish cli script
if __name__ == '__main__':
    main()
