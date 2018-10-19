"""
RxPY example running a Tornado server doing search queries against
Wikipedia to populate the autocomplete dropdown in the web UI. Start
using `python autocomplete.py` and navigate your web browser to
http://localhost:8080
Uses the RxPY AsyncIOScheduler (Python 3.4 is required)
"""

import os
import rx
asyncio = rx.config['asyncio']

from rx.subjects import Subject
from rx.concurrency import AsyncIOScheduler
from time import sleep


scheduler = AsyncIOScheduler()


def search_wikipedia(term):
    """Search Wikipedia for a given term"""
    url = 'http://en.wikipedia.org/w/api.php'

    params = {
        "action": 'opensearch',
        "search": term,
        "format": 'json'
    }
    # Must set a user agent for non-browser requests to Wikipedia
    user_agent = "RxPY/1.0 (https://github.com/dbrattli/RxPY; dag@brattli.net) Tornado/4.0.1"

    url = url_concat(url, params)

    http_client = AsyncHTTPClient()
    return http_client.fetch(url, method='GET', user_agent=user_agent)


class WSHandler():
    def open(self):
        print("WebSocket opened")

        # A Subject is both an observable and observer, so we can both subscribe
        # to it and also feed (send) it with new values
        self.subject = Subject()

        # Get all distinct key up events from the input and only fire if long enough and distinct
        searcher = (self.subject
                 .map(lambda x: x["term"])
                 # Only if the text is longer than 2 characters
                 .filter(lambda text: len(text) > 2)
                 .debounce(750)                       # Pause for 750ms
                 .distinct_until_changed()            # Only if the value has changed
                 .flat_map_latest(search_wikipedia)
                 )

        def handle_response(x):
            print(x.body)

        def on_error(ex):
            print(ex)

        searcher.subscribe(handle_response, on_error, scheduler=scheduler)

    def on_message(self, message):
        obj = json_decode(message)
        self.subject.on_next(obj)


def main():
    AsyncIOMainLoop().install()
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
