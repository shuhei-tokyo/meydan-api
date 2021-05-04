# gunicorn index:app
import falcon
import Original

class CORSMiddleware:
	def process_request(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')

app = falcon.API(middleware=[CORSMiddleware()])
app.add_route('/v1/umabashira/original', Original.Original())
