from aiohttp import web


class Handler:
    version_str = 'unknown'

    @staticmethod
    def check_version_file():
        try:
            with open('version.txt', 'r') as version_file:
                print('\nVersion: ', end='')
                new_version_str = ''
                for line in version_file:
                    new_version_str += line
                    print(line)
                return new_version_str
        except IOError:
            print("An IOError has occurred!")

    def __init__(self):
        self.version_str = self.check_version_file()
        print('Check server 0.1')

    async def latest(self, request):
        return web.Response(text=self.version_str)

    async def update_handle(self, request):
        vers = self.check_version_file()
        if vers != self.version_str:  # very stupid method, but..
            print('Old version:', self.version_str)
            self.version_str = vers
        return web.Response(text=vers)

    async def handle(self, request):
        version = request.match_info.get('version', "unknown")
        text = 'Latest version: ' + self.version_str
        text += '\nCurrent version: ' + version
        if self.version_str != 'unknown' and version != 'favicon.ico':
            print(text)
        return web.Response(text=text)


if __name__ == '__main__':
    handler = Handler()
    app = web.Application()
    app.add_routes([web.get('/', handler.latest),
                    web.get('/check/{version}', handler.handle),
                    web.get('/update_version', handler.update_handle)])
    web.run_app(app)
