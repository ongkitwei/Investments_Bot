import finnhub
import json
import requests

def getTopMarketNews():
    try:
        finnhub_client = finnhub.Client(api_key="d1no9l1r01qovv8kh4n0d1no9l1r01qovv8kh4ng")
        urlLink = []
        noOfNews = 0
        # allNews = json.dumps(finnhub_client.general_news('general', min_id=0), indent=2)
        rawNews = finnhub_client.general_news('general', min_id=0)

        for x in rawNews:
            if x["source"] == "CNBC":
                if noOfNews < 3:
                    urlLink.append({"headline": x["headline"], "url": x["url"]})
                    noOfNews+=1
                else:
                    break
        print(urlLink)
        return urlLink
    except requests.exceptions.ReadTimeout:
            print("⚠️ Finnhub request timed out. Skipping news fetch.")
            return []

    except Exception as e:
        print(f"⚠️ Unexpected error fetching news: {e}")
        return []

