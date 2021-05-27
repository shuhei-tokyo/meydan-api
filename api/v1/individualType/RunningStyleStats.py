import json
import mysql.connector
import configparser
from datetime import datetime

class RunningStyleStats:
    def on_get(self, req, resp):
        runningStyleStats = {}
        
        if 'jvdHorseId' in req.params and 'size' in req.params and 'trackType' in req.params and 'step' in req.params:
            #クエリパラメータの取得
            jvdHorseId = req.params['jvdHorseId']
            size = int(req.params['size'])
            step = int(req.params['step'])
            trackType = req.params['trackType']
            target_track_type_master_id = []
            if trackType == 'turf':
                target_track_type_master_id = [1, 5]
            elif trackType == 'dirt':
                target_track_type_master_id = [2, 6] #6は配列の長さを揃えるためのダミー(該当データなし)
            elif trackType == 'steepleChase':
                target_track_type_master_id = [3, 4]

            #レスポンスの作成
            runningStyleStats['result'] = {}

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
                    'target_running_style_master.id, '
                    'target_running_style_master.name, '
                    'ifnull(result.count, 0) as count '
                'from target_running_style_master '
                'left join ( '
                    'select '
                        'tmp.target_running_style_master_id, '
                        'count(*) as count '
                    'from ( '
                        'select '
                        '    race_result.target_running_style_master_id '
                        'from race_result '
                        'left join org_race_master '
                        '    on race_result.org_race_master_id = org_race_master.id '
                        'left join jvd_accident_master '
                        '    on race_result.jvd_accident_master_id = jvd_accident_master.id '
                        'left join org_horse_master '
                        '    on race_result.org_horse_master_id = org_horse_master.id '
                        'where org_horse_master.id_jvd = %s '
                        '    and org_race_master.target_track_type_master_id in (%s,%s) '
                        'and jvd_accident_master.id in (1,5,6,7,8) '
                        'order by org_race_master.datetime desc limit %s '
                    ') as tmp '
                    'group by tmp.target_running_style_master_id '
                ') as result '
                    'on target_running_style_master.id = result.target_running_style_master_id '
                'order by target_running_style_master.id; '
            )

            cur.execute(sql, (jvdHorseId, target_track_type_master_id[0], target_track_type_master_id[1], size))
            rows = cur.fetchall()
            runningStyleStats['result']['type'] = "RunningStyleStats"
            runningStyleStats['result']['element'] = []

            for row in rows:     
                element = {}
                element['id'] = row[0]
                element['name'] = row[1]
                element['count'] = row[2]
                runningStyleStats['result']['element'].append(element)

            cur.close()
            conn.close()

            if step == 4:
                #先行 = 先行 + マクリ
                runningStyleStats['result']['element'][1]['count'] = runningStyleStats['result']['element'][1]['count'] + runningStyleStats['result']['element'][4]['count']
                #差し = 差し + 中団
                runningStyleStats['result']['element'][2]['count'] = runningStyleStats['result']['element'][2]['count'] + runningStyleStats['result']['element'][5]['count']
                #追い込み = 追い込み + 後方
                runningStyleStats['result']['element'][3]['count'] = runningStyleStats['result']['element'][3]['count'] + runningStyleStats['result']['element'][6]['count']
                #マクリ、中団、後方、その他を削除
                del runningStyleStats['result']['element'][4:]

        else:
            #パラメータ異常のとき
            runningStyleStats['message'] = "bad request"

        resp.body = json.dumps(runningStyleStats, ensure_ascii=False)

