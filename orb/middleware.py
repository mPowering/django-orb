
from orb.forms import HeaderSearchForm


class SearchFormMiddleware(object):

    def process_request(self, request):

        form = HeaderSearchForm()

        # attach the form to the request so it can be accessed within the
        # templates
        request.search_form = form
