from __future__ import unicode_literals

import re
from HTMLParser import HTMLParser

import requests

from horse.bridles.base import CommandBridle


class GoogleSearch(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = "google"
        description = "Search google and display top results"
        help_text = ["Usage: `/horse google <terms>`"]

        display_name = "Google"
        display_icon = (
            "http://www.google.com/trends/resources"
            "/2327917647-google-icon.png"
        )

    api_base = "http://ajax.googleapis.com"
    endpoint = "/ajax/services/search/web"
    default_params = {
        "v": "1.0",
        "q": ""
    }

    display_results = 3
    display_format = "{0}\n---\n{1}"
    display_footer = "_<{url}|{count}> results found in {elapsed}_"

    def execute(self, user, channel, operands):
        if len(operands) > 0:
            results = self.search(operands)
            if results is None:
                return "No results found :("
            elif isinstance(results, basestring):
                return results
            else:
                self.display_response(user, channel, results)
        else:
            return self.help_text

    def build_query(self, operands):
        query = self.default_params.copy()
        query['q'] = "+".join(operands)
        return query

    def search(self, operands):
        url = self.api_base + self.endpoint
        params = self.build_query(operands)
        response = requests.get(url, params=params).json()

        return self.parse_response(operands, response)

    def parse_response(self, operands, response):
        if response['responseStatus'] == 403:
            return "Search API has been deprecated by Google. Horse sad."
        if len(response['responseData']['results']) == 0:
            return None
        return {
            "terms": " ".join(operands),
            "elapsed": float(
                response['responseData']['cursor']['searchResultTime']
            ),
            "count": response['responseData']['cursor']['resultCount'],
            "url": response['responseData']['cursor']['moreResultsUrl'],
            "results": response['responseData']['results']
        }

    def format_result(self, result):
        result['content'] = self.clean_content(result['content'])
        result = "*<{unescapedUrl}|{titleNoFormatting}>*\n{content}".format(
            **result
        )
        return result

    def display_response(self, user, channel, response):
        results = "\n\n".join([
            self.format_result(result)
            for result in response['results'][:self.display_results]
        ])
        footer = self.display_footer.format(
            **response
        )
        self.message(
            channel,
            self.display_format.format(results, footer)
        )

    def clean_content(self, content):
        parser = HTMLParser()
        content = parser.unescape(content)
        content = re.sub(r'<.*?>', '', content)
        content = re.sub(r'\n', '', content)
        if not content:
            return "Summary unavailable"
        return content
