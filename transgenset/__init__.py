
class Producer(object):
    def __init__(self, context, template):
        self.context = context
        self.template = template

    def next_message(self):
        return self.template.render(self.context)
