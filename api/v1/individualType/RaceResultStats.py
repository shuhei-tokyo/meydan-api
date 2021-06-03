import json
import mysql.connector
import configparser
from datetime import datetime

class RaceResultStats:
	def on_get(self, req, resp):
		raceResultStats = {}
		
		if 'jvdHorseId' in req.params and 'courseId' in req.params:
			#クエリパラメータの取得
			jvdHorseId = req.params['jvdHorseId']
			courseId = int(req.params['courseId'])

			#レスポンスの作成
			raceResultStats['result'] = []

			#設定ファイルの読み込み
			inifile = configparser.ConfigParser()
			inifile.read('./config.ini', 'utf-8')
			host = inifile.get('mysql', 'host')
			port = inifile.get('mysql', 'port')
			user = inifile.get('mysql', 'user')
			password = inifile.get('mysql', 'password')
			database = inifile.get('mysql', 'database')

			#DBに接続
			conn = mysql.connector.connect(
				host = host,
				port = port,
				user = user,
				password = password,
				database = database
			)
			cur = conn.cursor(buffered=True)

			#sql
			sql_create_tmp = 'create temporary table tmp (order_of_arrival int); '
			sql_insert_into_tmp = 'insert into tmp (order_of_arrival) values (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18); '
			sql_result = (
				'select '
				    'tmp.order_of_arrival, '
				    'ifnull(result.count, 0) '
				'from tmp '
				'left join ( '
				    'select '
				        'race_result.order_of_arrival, '
				        'count(*) as count '
				    'from  race_result '
				    'left join org_race_master '
				        'on race_result.org_race_master_id = org_race_master.id '
				    'left join jvd_course_master '
				        'on org_race_master.jvd_course_master_id = jvd_course_master.id '
				    'left join org_horse_master '
						'on race_result.org_horse_master_id = org_horse_master.id '
					'where org_horse_master.id_jvd = %s '
				    'and jvd_course_master.id_jvd = %s '
				    'and org_race_master.target_track_type_master_id in (1,5) '
				    'group by race_result.order_of_arrival '
				') as result '
				    'on tmp.order_of_arrival = result.order_of_arrival '
				    'order by tmp.order_of_arrival; '
			)
			cur.execute(sql_create_tmp)
			cur.execute(sql_insert_into_tmp)
			cur.execute(sql_result, (jvdHorseId, courseId))
			raceResultStats['result'] = [
				{
					"name": "1着",
					"count": 0
				},
				{
					"name": "2着",
					"count": 0
				},
				{
					"name": "3着",
					"count": 0
				},
				{
					"name": "その他",
					"count": 0
				}
			]
			rows = cur.fetchall()
			for row in rows:
				if row[0] == 1:
					raceResultStats['result'][0]['count'] = raceResultStats['result'][0]['count'] + row[1]
				elif row[0] == 2:
					raceResultStats['result'][1]['count'] = raceResultStats['result'][1]['count'] + row[1]
				elif row[0] == 3:
					raceResultStats['result'][2]['count'] = raceResultStats['result'][2]['count'] + row[1]
				else:
					raceResultStats['result'][3]['count'] = raceResultStats['result'][3]['count'] + row[1]

			cur.close()
			conn.close()

		else:
			#パラメータ異常のとき
			raceResultStats['message'] = "bad request"

		resp.body = json.dumps(raceResultStats, ensure_ascii=False)

