from googleapiclient.discovery import build
from KEYS import GOOGLE_DEV_API, SEARCH_ENGINE_ID

def search_google(query):
    try:
        # From https://github.com/googleapis/google-api-python-client/blob/main/samples/customsearch/main.py
        service = build(
            "customsearch", "v1", developerKey=GOOGLE_DEV_API
        )

        res = (
            service.cse()
            .list(
                q=query,
                cx=SEARCH_ENGINE_ID,
            )
            .execute() )
        
        return res['items'][0]
    except:
        return 'failed search'