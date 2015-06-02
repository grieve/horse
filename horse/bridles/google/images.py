from . import search


class GoogleImagesSearch(search.GoogleSearch):

    class Meta(search.GoogleSearch.Meta):
        command = 'images'
        description = "Search google images and display top result"
        help_text = ["Usage: `/horse images <terms>`"]

    endpoint = "/ajax/services/search/images"
    display_results = 1
    display_format = "{0}{1}"
    display_footer = ""

    def format_result(self, result):
        return result['unescapedUrl']


class GoogleGifSearch(GoogleImagesSearch):

    class Meta(GoogleImagesSearch.Meta):
        command = 'images-gif'
        description = "Search google images and display top animated result"
        help_text = ["Usage: `/horse images-gif <terms>`"]

    endpoint = "/ajax/services/search/images"
    default_params = {
        "v": "1.0",
        "imgtype": "animated",
        "q": ""
    }
