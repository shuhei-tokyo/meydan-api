# gunicorn index:app
import falcon
import RaceCard

class CORSMiddleware:
	def process_request(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')

app = falcon.API(middleware=[CORSMiddleware()])
app.add_route('/v1/indiv/raceCard', RaceCard.RaceCard())
