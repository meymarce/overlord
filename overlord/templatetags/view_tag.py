from django.template import Library, Node, TemplateSyntaxError, Variable
from django.conf import settings
from django.core import urlresolvers

import hashlib
import re

register = Library()


class ViewNode(Node):

    def __init__(self, parser, token):
        self.args = []
        self.kwargs = {}
        tokens = token.split_contents()
        if len(tokens) < 2:
            raise TemplateSyntaxError("%r tag requires one or more arguments" % token.contents.split()[0])

        tag_name = tokens.pop(0)
        self.url_or_view = tokens.pop(0)
        for token in tokens:
            equals = token.find("=")
            if equals == -1:
                self.args.append(token)
            else:
                self.kwargs[str(token[:equals])] = token[equals + 1:]

    def render(self, context):
        print('render view tag...')
        if 'request' not in context:
            return ""
        request = context['request']

        # get the url for the view
        url = Variable(self.url_or_view).resolve(context)
        if not settings.USE_AJAX_REQUESTS:
            # do not load the whole template, just the content, like an ajax request
            #request.is_ajax = True # not needed since the jQuery.get() is implying this
            urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
            resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
            # get the view function
            view, args, kwargs = resolver.resolve(url)

            try:
                if callable(view):
                    ret = view(context['request'], *args, **kwargs).render()
                    return ret.rendered_content
                raise Exception("%r is not callable" % view)
            except:
                if settings.TEMPLATE_DEBUG:
                    raise
        else:
            print('return js code for jquery')
            return """<div id="%(div_id)s">loading ...</div>
<script>
$.get( "%(url)s", function( data ) {
  $( "#%(div_id)s" ).html( data );
});
</script>""" % {'div_id': url.replace("/", ""), 'url': url}
        return ""

register.tag('view', ViewNode)
