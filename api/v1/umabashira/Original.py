import json
import configparser
import UmabashiraGenerator
import RaceInfoGenerator

class Original:
	def on_get(self, req, resp):
		#設定ファイルの読み込み
		inifile = configparser.ConfigParser()
		inifile.read('./config.ini', 'UTF-8')
		csvfile = inifile.get('jvdfile', 'csvfile_A')
		txtfile = inifile.get('jvdfile', 'txtfile_D')

		#レスポンスの作成
		result = {}

		#umabashiraの取得
		umabashiraGenerator = UmabashiraGenerator.UmabashiraGenerator(csvfile)
		result['umabashira'] = umabashiraGenerator.getUmabashira()

		#race_infoの取得
		raceInfoGenerator = RaceInfoGenerator.RaceInfoGenerator(txtfile)
		result['race_info'] = raceInfoGenerator.getRaceInfo()

		resp.body = json.dumps(result, ensure_ascii=False)
