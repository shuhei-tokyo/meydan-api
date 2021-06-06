import json
import requests
import configparser
import UmabashiraGenerator
import RaceInfoGenerator

class Umabashira:
	def on_get(self, req, resp):
		#設定ファイルの読み込み
		inifile = configparser.ConfigParser()
		inifile.read('./config.ini', 'UTF-8')
		csvfile = inifile.get('jvdfile', 'csvfile_A')
		txtfile = inifile.get('jvdfile', 'txtfile_D')

		params = {}
		params['racecard'] = {}
		params['racecard']['race_rename'] = inifile.get('params_racecard', 'race_rename')
		params['racecard']['size'] = inifile.get('params_racecard', 'size')
		params['runningstylestats'] = {}
		params['runningstylestats']['track_type'] = inifile.get('params_runningstylestats', 'track_type')
		params['runningstylestats']['size'] = inifile.get('params_runningstylestats', 'size')
		params['runningstylestats']['step'] = inifile.get('params_runningstylestats', 'step')
		params['raceresultstats'] = {}
		params['raceresultstats']['track_type'] = inifile.get('params_raceresultstats', 'track_type')
		params['raceresultstats']['course_id'] = inifile.get('params_raceresultstats', 'course_id')

		#レスポンスの作成
		result = {}
		result['result'] = {}
		result['result']['type'] = "Umabashira"

		#race_infoの取得
		raceInfoGenerator = RaceInfoGenerator.RaceInfoGenerator(txtfile)
		result['result']['race'] = raceInfoGenerator.getRaceInfo()

		#レース名を上書きするとき
		if params['racecard']['race_rename'] != "":
			result['result']['race']['race_name'] = params['racecard']['race_rename']

		#umabashiraの取得
		umabashiraGenerator = UmabashiraGenerator.UmabashiraGenerator(csvfile)
		result['result']['horse'] = umabashiraGenerator.getUmabashira()

		#typeが指定されるとき
		if 'type' in req.params:
			#type=RaceCard
			if req.params['type'] == "RaceCard":
				for i in range(len(result['result']['horse'])):
					jvdHorseId = result['result']['horse'][i]['org_horse_master_id_jvd']
					url = "http://localhost:8070/v1/RaceCard?jvdHorseId={0}&size={1}".format(jvdHorseId, params['racecard']['size'])
					r = requests.get(url)
					res = r.json()
					result['result']['horse'][i]['item'] = res['result']
			#type=RunningStyleStats
			if req.params['type'] == "RunningStyleStats":
				for i in range(len(result['result']['horse'])):
					jvdHorseId = result['result']['horse'][i]['org_horse_master_id_jvd']
					url = "http://localhost:8070/v1/RunningStyleStats?jvdHorseId={0}&size={1}&step={2}&trackType={3}".format(jvdHorseId, params['runningstylestats']['size'], params['runningstylestats']['step'], params['runningstylestats']['track_type'])
					r = requests.get(url)
					res = r.json()
					result['result']['horse'][i]['item'] = res['result']
			#type=RaceResultStats
			if req.params['type'] == "RaceResultStats":
				for i in range(len(result['result']['horse'])):
					jvdHorseId = result['result']['horse'][i]['org_horse_master_id_jvd']
					url = "http://localhost:8070/v1/RaceResultStats?jvdHorseId={0}&courseId={1}&trackType={2}".format(jvdHorseId, params['raceresultstats']['course_id'], params['raceresultstats']['track_type'])
					r = requests.get(url)
					res = r.json()
					result['result']['horse'][i]['item'] = res['result']


		resp.body = json.dumps(result, ensure_ascii=False)
