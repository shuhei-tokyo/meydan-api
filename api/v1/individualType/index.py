import falcon
import RaceCard
import RunningStyleStats
import RaceResultStats

class CORSMiddleware:
	def process_request(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')

app = falcon.API(middleware=[CORSMiddleware()])
app.add_route('/v1/RaceCard', RaceCard.RaceCard())
app.add_route('/v1/RunningStyleStats', RunningStyleStats.RunningStyleStats())
app.add_route('/v1/RaceResultStats', RaceResultStats.RaceResultStats())
