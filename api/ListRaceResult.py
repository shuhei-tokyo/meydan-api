import json
import configparser
import mysql.connector
from datetime import datetime

class ListRaceResult:
	def on_get(self, req, resp):
		result = {}

		#クエリパラメータを取得
		raceId = None
		if 'raceId' in req.params:
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

		#sql
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
		result['race_info'] = race_info

		cur.close()
		conn.close()
		resp.body = json.dumps(result, ensure_ascii=False)
