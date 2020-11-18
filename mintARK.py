import requests, json, csv, sys


def getARK(luna_url, title, rights, type):
    auth_token = ''

    url="https://libapps.colorado.edu/ark:/"

    data={"resolve_url": luna_url ,"metadata":{"mods": {"titleInfo":[{"title": title}],"typeOfResource": type, "accessCondition": rights}},"generated_by":"radio","status": "active"}
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
         for row in reader:
             luna_url = row['lnexp_PAGEURL']
             title = row['Title#1']
             rights = row['Access Condition#1']
             type = row['Type of Resource#1']
             ark = getARK(luna_url, title, rights, type)
             row['Identifier ARK'] = 'https://ark.colorado.edu/ark:/' + ark
             writer.writerow(row)


# make this a safe-ish cli script
if __name__ == '__main__':
    main()
