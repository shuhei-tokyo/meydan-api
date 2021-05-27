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
		race_rename = inifile.get('params_racecard', 'race_rename')
		size_racecard = inifile.get('params_racecard', 'size')
		track_type = inifile.get('params_runningstylestats', 'track_type')
		size_runningstyle = inifile.get('params_runningstylestats', 'size')
		step = inifile.get('params_runningstylestats', 'step')

		#レスポンスの作成
		result = {}
		result['result'] = {}
		result['result']['type'] = "Umabashira"

		#race_infoの取得
		raceInfoGenerator = RaceInfoGenerator.RaceInfoGenerator(txtfile)
		result['result']['race'] = raceInfoGenerator.getRaceInfo()

		#レース名を上書きするとき
		if race_rename != "":
			result['result']['race']['race_name'] = race_rename

		#umabashiraの取得
		umabashiraGenerator = UmabashiraGenerator.UmabashiraGenerator(csvfile)
		result['result']['horse'] = umabashiraGenerator.getUmabashira()

		#typeが指定されるとき
		if 'type' in req.params:
			#type=RaceCard
			if req.params['type'] == "RaceCard":
				for i in range(len(result['result']['horse'])):
					jvdHorseId = result['result']['horse'][i]['org_horse_master_id_jvd']
					url = "http://localhost:8070/v1/RaceCard?jvdHorseId={0}&size={1}".format(jvdHorseId, size_racecard)
					r = requests.get(url)
					res = r.json()
					result['result']['horse'][i]['item'] = res['result']
			#type=RunningStyleStats
			if req.params['type'] == "RunningStyleStats":
				for i in range(len(result['result']['horse'])):
					jvdHorseId = result['result']['horse'][i]['org_horse_master_id_jvd']
					url = "http://localhost:8070/v1/RunningStyleStats?jvdHorseId={0}&size={1}&step={2}&trackType={3}".format(jvdHorseId, size_runningstyle, step, track_type)
					r = requests.get(url)
					res = r.json()
					result['result']['horse'][i]['item'] = res['result']

		resp.body = json.dumps(result, ensure_ascii=False)
