from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

import feedparser


corona_ticker_and_maps_articles = [
    'https://www.zeit.de/wissen/aktuelle-corona-zahlen-karte-deutschland-landkreise',
    'https://www.zeit.de/wissen/gesundheit/corona-zahlen-europa-weltweit-aktuell-karte',
    'https://www.zeit.de/politik/ausland/2021-11/corona-weltweit-omikron-news-live'
]


def build_url(feed):
    url = 'http://newsfeed.zeit.de/'

    feed = feed.lower()

    if feed == 'all' or feed == 'alle inhalte':
        return url + 'all'
    elif feed == 'mobilität':
        feed = 'mobilitaet'
    elif feed == 'zeit campus online':
        feed = 'campus'
    elif feed == 'zeit magazin online':
        feed = 'zeit-magazin'
    elif feed == 'zeit online arbeit':
        feed = 'arbeit'

    return url + feed + '/index'


class ZeitOnlineExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def add_newest_zeit_online_articles(self, items):
        url = build_url(self.feed)
        print(url)
        NewsFeed = feedparser.parse(url)


        for entry in NewsFeed.entries[:10]:

            if self.is_corona_ticker_and_maps_included == 'False' and entry.link in corona_ticker_and_maps_articles:
                continue

            if len(items) == 5:
                return

            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=entry.title,
                                             description=entry.description,
                                             on_enter=OpenUrlAction(entry.link)))


    def on_event(self, event, extension):
        items = []
        entered_feed = event.get_query()[4:] # remove beginning "zon "
        print("1111 " + str(entered_feed))
        self.feed = entered_feed if entered_feed else extension.preferences['default_feed']
        self.is_corona_ticker_and_maps_included = extension.preferences['is_corona_ticker_and_maps_included']
        self.add_newest_zeit_online_articles(items)

        return RenderResultListAction(items)


if __name__ == '__main__':
    ZeitOnlineExtension().run()