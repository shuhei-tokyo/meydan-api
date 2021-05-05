import mysql.connector
import configparser
import csv
import math
import logging

class UmabashiraGenerator:
	def __init__(self, csvfile_A):
		self.csvfile_A = csvfile_A

	def getUmabashira(self):
		#ログの設定
		logging.basicConfig()
		logger = logging.getLogger()
		logger.setLevel(logging.INFO)

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

		with open(self.csvfile_A, newline="", encoding="shift-jis") as f:
			results = []
			dataReader = csv.reader(f)
			for row in dataReader:
				#出馬表から各種情報を取得
				result = {}
				#result["datetime"] = row[0]
				result["bracket_num"] = row[22]
				result["horse_num"] = row[3].strip()
				result["horse_name"] = row[7]
				result["sex"] = row[8]
				result["age"] = row[9]
				result["jockey_name"] = row[10]
				result["trainer_name"] = row[12]
				result["belongings"] = row[13]
				result["owner"] = row[14]
				result["breeder"] = row[15]
				result["sire"] = row[16]
				result["blood_mare"] = row[17]
				result["org_horse_master_id_jvd"] = "20" + row[18]
				result["blood_mare_sire"] = row[20]
				result["color"] = row[21]

				#負担重量の '.0' を除去
				if float(row[11]) == math.floor(float(row[11])):
					result["impost"] = math.floor(float(row[11]))
				else:
					result["impost"] = row[11]

				#jockey_idを取得
				sql = "select id from org_jockey_master where name_four_words = %s;"
				cur.execute(sql, (result["jockey_name"], ))
				row = cur.fetchone()
				if row is None:
					result["jockey_id"] = None
					logger.error("'{0}' is not registered in org_jockey_master".format(result["jockey_name"]))
				else:
					result["jockey_id"] = row[0]

				#trainer_id を取得
				sql = "select id from org_trainer_master where name_four_words = %s;"
				cur.execute(sql, (result["trainer_name"], ))
				row = cur.fetchone()
				if row is None:
					result["trainer_id"] = None
					logger.error("'{0}' is not registered in org_trainer_master".format(result["trainer_name"]))
				else:
					result["trainer_id"] = row[0]

				results.append(result)

		cur.close()
		conn.close()
		return results