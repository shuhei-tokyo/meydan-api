import json
import mysql.connector
from datetime import datetime

class ListRaceResult:
	def on_get(self, req, resp):
		result = {}
		if 'raceId' in req.params:
			#クエリパラメータを取得
			raceId = req.params['raceId']

			#ローカルのDBの場合
			conn = mysql.connector.connect(
				host = 'localhost',
				port = 3306,
				user = 'root',
				password = '',
				database = 'meydan'
			)
			cur = conn.cursor(buffered=True)

			#info
			sql = (
				'select '
					'org_race_master.datetime, '
					'jvd_course_master.name_two_words as course_name, '
					'org_race_master.num_series, '
					'org_race_master.count_day, '
					'org_race_master.num_race, '
					'org_race_master.distance, '
					'org_race_master.count_corners, '
					'jvd_weather_master.name as weather, '
					'jvd_track_condition_master.name as track_condition, '
					'org_race_master.name, '
					'org_race_master.short_name, '
					'jvd_grade_master.name as grade, '
					'target_race_class_master.name as class, '
					'target_track_type_master.name as track_type, '
					'jvd_race_weight_regulation_master.name as race_weight_regulation, '
					'jvd_race_breed_qualification_master.name as race_breed_qualification, '
					'jvd_race_mark_master.name as race_mark, '
					'race_result.time '
				'from race_result '
					'left join org_race_master '
						'on race_result.org_race_master_id = org_race_master.id '
					'left join jvd_course_master '
						'on org_race_master.jvd_course_master_id = jvd_course_master.id '
					'left join jvd_weather_master '
						'on org_race_master.jvd_weather_master_id = jvd_weather_master.id '
					'left join jvd_track_condition_master '
						'on org_race_master.jvd_track_condition_master_id = jvd_track_condition_master.id '
					'left join jvd_grade_master '
						'on org_race_master.jvd_grade_master_id = jvd_grade_master.id '
					'left join target_race_class_master '
						'on org_race_master.target_race_class_master_id = target_race_class_master.id '
					'left join target_track_type_master '
						'on org_race_master.target_track_type_master_id = target_track_type_master.id '
					'left join jvd_race_weight_regulation_master '
						'on org_race_master.jvd_race_weight_regulation_master_id = jvd_race_weight_regulation_master.id '
					'left join jvd_race_breed_qualification_master '
						'on org_race_master.jvd_race_breed_qualification_master_id = jvd_race_breed_qualification_master.id '
					'left join jvd_race_mark_master '
						'on org_race_master.jvd_race_mark_master_id = jvd_race_mark_master.id '
				'where race_result.org_race_master_id = %s '
				'order by race_result.order_of_arrival; '
			)
			cur.execute(sql, (raceId, ))
			row = cur.fetchone()
			race_info = {}
			race_info['datetime'] = row[0].isoformat()
			race_info['course_name'] = row[1]
			race_info['num_series'] = row[2]
			race_info['count_day'] = row[3]
			race_info['num_race'] = row[4]
			race_info['distance'] = row[5]
			race_info['count_corners'] = row[6]
			race_info['weather'] = row[7]
			race_info['track_condition'] = row[8]
			race_info['name'] = row[9]
			race_info['short_name'] = row[10]
			race_info['grade'] = row[11]
			race_info['class'] = row[12]
			race_info['track_type'] = row[13]
			race_info['race_weight_regulation'] = row[14]
			race_info['race_breed_qualification'] = row[15]
			race_info['race_mark'] = row[16]
			race_info['time'] = row[17]
			result['info'] = race_info

			#result
			result['result'] = []
			sql = (
				'select '
					'race_result.horse_num, '
					'race_result.bracket_num, '
					'org_horse_master.name as horse_name, '
					'jvd_gender_master.name as horse_gender, '
					'race_result.horse_age, '
					'org_jockey_master.name as jockey_name, '
					'race_result.impost, '
					'org_trainer_master.name as trainer_name, '
					'race_result.order_of_corners_1, '
					'race_result.order_of_corners_2, '
					'race_result.order_of_corners_3, '
					'race_result.order_of_corners_4, '
					'race_result.order_of_arrival, '
					'race_result.order_of_arrival_confirmed, '
					'jvd_accident_master.name_two_words as accident_name, '
					'race_result.time_3f, '
					'race_result.order_of_time_3f, '
					'race_result.odds_win, '
					'race_result.time_margin '
				'from race_result '
					'left join org_horse_master '
						'on race_result.org_horse_master_id = org_horse_master.id '
					'left join jvd_gender_master '
						'on race_result.jvd_gender_master_id = jvd_gender_master.id '
					'left join org_jockey_master '
						'on race_result.org_jockey_master_id = org_jockey_master.id '
					'left join org_trainer_master '
						'on race_result.org_trainer_master_id = org_trainer_master.id '
					'left join jvd_accident_master '
						'on race_result.jvd_accident_master_id = jvd_accident_master.id '
				'where race_result.org_race_master_id = %s '
				'order by race_result.order_of_arrival; '
			)
			cur.execute(sql, (raceId, ))
			rows = cur.fetchall()

			for row in rows:
				race = {}
				race['horse_num'] = row[0]
				race['bracket_num'] = row[1]
				race['horse_name'] = row[2]
				race['horse_gender'] = row[3][0]
				race['horse_age'] = row[4]
				race['jockey_name'] = row[5]
				race['impost'] = row[6]
				race['trainer_name'] = row[7]
				race['order_of_corners_1'] = row[8]
				race['order_of_corners_2'] = row[9]
				race['order_of_corners_3'] = row[10]
				race['order_of_corners_4'] = row[11]
				race['order_of_arrival'] = row[12]
				race['order_of_arrival_confirmed'] = row[13]
				race['accident_name'] = row[14]
				race['time_3f'] = row[15]
				race['order_of_time_3f'] = row[16]
				race['odds_win'] = row[17]
				race['time_margin'] = row[18]
				result['result'].append(race)
			cur.close()
			conn.close()

		#bad request
		else:
			result['message'] = "bad request"

		resp.body = json.dumps(result, ensure_ascii=False)

