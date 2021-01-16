import json
import mysql.connector

class SearchRace:
	def on_get(self, req, resp):
		results = []
		if 'name' in req.params and 'dateFrom' in req.params and 'dateTo' in req.params:
			#クエリパラメータを取得
			name = "%{}%".format(req.params['name'])
			dateFrom = req.params['dateFrom']
			dateTo = req.params['dateTo']

			#ローカルのDBの場合
			conn = mysql.connector.connect(
				host = 'localhost',
				port = 3306,
				user = 'root',
				password = '',
				database = 'meydan'
			)
			cur = conn.cursor(buffered=True)

			sql = (
			    "select * from org_race_master "
			    "where org_race_master.name like %s "
			    "and org_race_master.datetime between %s and %s "
			    "and org_race_master.jra = 1;"
			)
			cur.execute(sql, (name, dateFrom, dateTo))
			rows = cur.fetchall()
			for row in rows:
			    race = {}
			    race['raceId'] = row[0]
			    race['datetime'] = row[2].isoformat()
			    race['short_name'] = row[7]
			    race['name'] = row[8]
			    results.append(race)

		#bad request
		else:
			results = {}
			results['message'] = "bad request"

		resp.body = json.dumps(results, ensure_ascii=False)

