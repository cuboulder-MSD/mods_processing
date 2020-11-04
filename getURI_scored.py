def get_topic_uri(doc):
    # print(doc)
    results = []
    jsonDocs = {}
    for term in doc['topics']:

        term= term.lower()
        url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'

        r = requests.get(url)
        r.raise_for_status()
        rjson = r.json()
        # print(r.text)
        jsonDocs = rjson['response']['docs']
        maxScore = 0.0
        fastValues = None
        for x in jsonDocs:
            # print(x)
            suggest = x['suggestall'][0]
            suggestLower = x['suggestall'][0].lower()
            fastID = x['idroot']

            score=fuzz.token_sort_ratio(term,suggestLower)
            if score > 80 and score > maxScore:
                maxScore = score
                fastValues = fastID, suggest
                results.append(fastValues)
    # print(results)
    return results
