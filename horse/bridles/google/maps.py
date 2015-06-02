from __future__ import absolute_import
from __future__ import unicode_literals

from horse import config
from horse.utils.google import url

from . import search


class GoogleMaps(search.GoogleSearch):

    class Meta(search.GoogleSearch.Meta):
        command = 'map'
        description = "Search google maps and display top results"
        help_text = ["Usage: `/horse map <terms>`"]

    api_base = "https://maps.googleapis.com"
    endpoint = "/maps/api/place/textsearch/json"
    default_params = {
        "query": "",
        "key": config.GAPI_API_TOKEN
    }

    image_endpoint = "/maps/api/staticmap?size=400x300&markers="
    map_url = "https://www.google.co.uk/maps/@"

    def build_query(self, operands):
        query = self.default_params.copy()
        query['query'] = "+".join(operands)
        return query

    def parse_response(self, operands, response):
        if len(response['results']) > 0:
            return {
                "terms": " ".join(operands),
                "results": response['results']
            }
        else:
            return None

    def format_result(self, result):
        result = "*<{0}|{name}>*\n_{formatted_address}_".format(
            self.map_url +
            str(result['geometry']['location']['lat']) +
            str(result['geometry']['location']['lng']),
            **result
        )
        return result

    def display_response(self, user, channel, response):
        results = "\n\n".join([
            self.format_result(result)
            for result in response['results'][:self.display_results]
        ])
        markers = "|".join(
            ["{0},{1}".format(
                result['geometry']['location']['lat'],
                result['geometry']['location']['lng']
            ) for result in response['results'][:self.display_results]]
        )
        footer = url.shorten(self.api_base + self.image_endpoint + markers)
        self.message(channel, results)
        self.message(channel, footer)
