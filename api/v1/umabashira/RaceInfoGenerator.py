import mojimoji

class RaceInfoGenerator:
	def __init__(self, txtfile_D):
		self.txtfile_D = txtfile_D

	def getRaceInfo(self):
		#テキストファイルの読み込み
		text_data = open(self.txtfile_D, "r", encoding = 'shift-jis')
		lines = text_data.readlines()
		text_data.close()

		#レスポンスの作成
		result = {}

		#line[0]
		tmp = lines[0].split(")")
		result['date'] = tmp[0].replace(" ", "")[:-2]
		result['course_name'] = tmp[1].strip().split(" ")[0][2:4]
		result['datetime'] = result['date'] + tmp[1].strip().split(" ")[1][:5]
		year = result['date'].split('年')[0]
		month = result['date'].split('年')[1].split('月')[0].zfill(2)
		day = result['date'].split('年')[1].split('月')[1].split('日')[0].zfill(2)
		result['datetime_iso'] = year + "-" + month + "-" + day + " " + tmp[1].strip().split(" ")[1][:5] + ":00"

		#line[1]
		tmp = lines[1].split(' ')
		result['race_num'] = mojimoji.zen_to_han(tmp[0].split('Ｒ')[0])
		result['race_name'] = tmp[2][:-1]

		#line[2]
		tmp = lines[2].split(' ')
		result['track_type'] = tmp[3]
		result['distance'] = tmp[4].split('m')[0]
		result['headcount'] = tmp[7][:-3]
		result['race_class'] = mojimoji.zen_to_han(tmp[0], kana=False)

		#内・外回り情報の追加
		if len(tmp[4].split('・')) == 2:
			result['track_type'] += tmp[4].split('・')[1] + "回り"

		#一般競走は race_name が null になるので記述
		if result['race_name'] == "":
			result['race_name'] = result['race_class'].split('(')[0]

		return result