# gunicorn index:app
import falcon
import ListRaceResult
import SearchRace

class CORSMiddleware:
	def process_request(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')

app = falcon.API(middleware=[CORSMiddleware()])
app.add_route('/list/race/result', ListRaceResult.ListRaceResult())
app.add_route('/search/race', SearchRace.SearchRace())
