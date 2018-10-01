import optparse


class Options:

    def __init__(self):
        parser = optparse.OptionParser()

        parser.add_option('-r', '--realtime',
                          action="store_true", dest="realtime",
                          help="Run in realtime", default=False)

        parser.add_option('-l', '--headless',
                          action="store_true", dest="headless",
                          help="Run in headless mode", default=False)

        parser.add_option('-m', '--model',
                          action="store", dest="model",
                          help="Model to use", default=False)

        parser.add_option('-t', '--times', type="int",
                          action="store", dest="times",
                          help="How often to run", default=1)

        options, args = parser.parse_args()
        self.options = options
        self.args = args

    def __getattr__(self, name):
        return self.options.__getattribute__(name)
