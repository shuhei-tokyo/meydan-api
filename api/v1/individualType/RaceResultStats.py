import json
import mysql.connector
import configparser
from datetime import datetime

class RaceResultStats:
	def on_get(self, req, resp):
		raceResultStats = {}
		#レスポンスの作成
		raceResultStats['result'] = {}
		raceResultStats['result']['type'] = "RaceResultStats"

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

		#tmpテーブルの作成
		sql_create_tmp = 'create temporary table tmp (order_of_arrival int); '
		sql_insert_into_tmp = 'insert into tmp (order_of_arrival) values (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18); '
		cur.execute(sql_create_tmp)
		cur.execute(sql_insert_into_tmp)

		#sql
		sql_start = (
			'select '
				'tmp.order_of_arrival, '
				'ifnull(result.count, 0) '
			'from tmp '
			'left join ( '
				'select '
					'race_result.order_of_arrival_confirmed, '
					'count(*) as count '
				'from  race_result '
				'left join org_race_master '
					'on race_result.org_race_master_id = org_race_master.id '
				'left join jvd_course_master '
					'on org_race_master.jvd_course_master_id = jvd_course_master.id '
				'left join target_track_type_master '
					'on org_race_master.target_track_type_master_id = target_track_type_master.id '
				'left join org_horse_master '
					'on race_result.org_horse_master_id = org_horse_master.id '
				'left join org_jockey_master '
					'on race_result.org_jockey_master_id = org_jockey_master.id '
				'left join org_trainer_master '
					'on race_result.org_trainer_master_id = org_trainer_master.id '
				'where race_result.jvd_accident_master_id in (1,5,6,7,8) '
		)

		sql_filter = ""
		if 'jvdHorseId' in req.params:
			jvdHorseId = req.params['jvdHorseId']
			raceResultStats['result']['jvdHorseId'] = jvdHorseId
			sql_tmp = "and org_horse_master.id_jvd = "
			sql_filter = "{0}{1}{2} ".format(sql_filter, sql_tmp, jvdHorseId)

		if 'courseId' in req.params:
			courseId = req.params['courseId']
			raceResultStats['result']['courseId'] = courseId
			sql_tmp = "and jvd_course_master.id_jvd = "
			sql_filter = "{0}{1}{2} ".format(sql_filter, sql_tmp, courseId)

		if 'trackType' in req.params:
			trackType = req.params['trackType']
			raceResultStats['result']['trackType'] = trackType
			target_track_type_master_id = []
			if trackType == 'turf':
				target_track_type_master_id = [1, 5]
			elif trackType == 'dirt':
				target_track_type_master_id = [2, 6] #6は配列の長さを揃えるためのダミー(該当データなし)
			elif trackType == 'steepleChase':
				target_track_type_master_id = [3, 4]
			sql_tmp = "and target_track_type_master.id in ({0}, {1}) ".format(target_track_type_master_id[0], target_track_type_master_id[1])
			sql_filter = "{0}{1} ".format(sql_filter, sql_tmp)

		sql_end = (
				'group by race_result.order_of_arrival_confirmed '
			') as result '
				'on tmp.order_of_arrival = result.order_of_arrival_confirmed '
				'order by tmp.order_of_arrival; '
		)
		sql = "{0}{1}{2}".format(sql_start, sql_filter, sql_end)
		cur.execute(sql)
		raceResultStats['result']['element'] = [
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
				raceResultStats['result']['element'][0]['count'] = raceResultStats['result']['element'][0]['count'] + row[1]
			elif row[0] == 2:
				raceResultStats['result']['element'][1]['count'] = raceResultStats['result']['element'][1]['count'] + row[1]
			elif row[0] == 3:
				raceResultStats['result']['element'][2]['count'] = raceResultStats['result']['element'][2]['count'] + row[1]
			else:
				raceResultStats['result']['element'][3]['count'] = raceResultStats['result']['element'][3]['count'] + row[1]

		cur.close()
		conn.close()

		resp.body = json.dumps(raceResultStats, ensure_ascii=False)

