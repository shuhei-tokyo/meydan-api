import json
import mysql.connector
import configparser
from datetime import datetime

class RaceCard:
	def on_get(self, req, resp):
		raceCard = {}
		
		if 'jvdHorseId' in req.params and 'size' in req.params:
			#クエリパラメータの取得
			jvdHorseId = req.params['jvdHorseId']
			size = int(req.params['size'])

			#レスポンス
			raceCard['result'] = {}
			raceCard['result']['type'] = 'RaceCard'
			raceCard['result']['items'] = []

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
			sql =(
				'select '
					'race_result.id_jvd, '
					'target_race_class_master.id, '
					'org_race_master.datetime, '
					'org_race_master.name, '
					'org_race_master.short_name, '
					'org_race_master.headcount, '
					'race_result.bracket_num, '
					'race_result.horse_num, '
					'jvd_course_master.name_two_words, '
					'org_race_master.distance, '
					'target_track_type_master.name, '
					'jvd_track_condition_master.name, '
					'org_jockey_master.name_four_words, '
					'race_result.horse_weight, '
					'race_result.horse_weight_gain_and_loss, '
					'race_result.impost, '
					'race_result.time_3f, '
					'race_result.order_of_time_3f, '
					'race_result.order_of_corners_1, '
					'race_result.order_of_corners_2, '
					'race_result.order_of_corners_3, '
					'race_result.order_of_corners_4, '
					'race_result.order_of_arrival, '
					'race_result.order_of_arrival_confirmed '
				'from race_result '
				'left join org_race_master '
					'on race_result.org_race_master_id = org_race_master.id '
				'left join target_race_class_master '
					'on org_race_master.target_race_class_master_id = target_race_class_master.id '
				'left join jvd_course_master '
					'on org_race_master.jvd_course_master_id = jvd_course_master.id '
				'left join jvd_track_condition_master '
					'on org_race_master.jvd_track_condition_master_id = jvd_track_condition_master.id '
				'left join target_track_type_master '
					'on org_race_master.target_track_type_master_id = target_track_type_master.id '
				'left join org_jockey_master '
					'on race_result.org_jockey_master_id = org_jockey_master.id '
				'left join org_horse_master '
					'on race_result.org_horse_master_id = org_horse_master.id '
				'where org_horse_master.id_jvd = %s '
				'order by org_race_master.datetime desc '
				'limit %s; '
			)

			cur.execute(sql, (jvdHorseId, size))
			rows = cur.fetchall()
			for row in rows:
				result = {}
				result['id'] = row[0]
				result['race_class_id'] = row[1]
				result['datetime'] = row[2].isoformat()
				result['race_name'] = row[3]
				result['race_short_name'] = row[4]
				result['headcount'] = row[5]
				result['bracket_num'] = row[6]
				result['horse_num'] = row[7]
				result['course_name'] = row[8]
				result['distance'] = row[9]
				result['track_type'] = row[10]
				result['track_condition'] = row[11]
				result['jockey_name'] = row[12]
				result['horse_weight'] = row[13]
				result['horse_weight_gain_and_loss'] = row[14]
				result['impost'] = row[15]
				result['time_3f'] = row[16]
				result['order_if_time_3f'] = row[17]
				result['order_of_corners_1'] = row[18]
				result['order_of_corners_2'] = row[19]
				result['order_of_corners_3'] = row[20]
				result['order_of_corners_4'] = row[21]
				result['order_of_arrival'] = row[22]
				result['order_of_arrival_confirmed'] = row[23]
				raceCard['result']['items'].append(result)
			cur.close()
			conn.close()

		else:
			#パラメータ異常のとき
			raceCard['message'] = "bad request"

		resp.body = json.dumps(raceCard, ensure_ascii=False)

