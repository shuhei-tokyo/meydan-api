import json
import mysql.connector
import configparser
from datetime import datetime

class RunningStyleStats:
    def on_get(self, req, resp):
        runningStyleStats = {}
        
        if 'jvdHorseId' in req.params and 'size' in req.params:
            #クエリパラメータの取得
            jvdHorseId = req.params['jvdHorseId']
            size = int(req.params['size'])

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
                        '    and org_race_master.target_track_type_master_id in (1,5) '
                        'and jvd_accident_master.id in (1,5,6,7,8) '
                        'order by org_race_master.datetime desc limit %s '
                    ') as tmp '
                    'group by tmp.target_running_style_master_id '
                ') as result '
                    'on target_running_style_master.id = result.target_running_style_master_id '
                'order by target_running_style_master.id; '
            )

            cur.execute(sql, (jvdHorseId, size))
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

        else:
            #パラメータ異常のとき
            runningStyleStats['message'] = "bad request"

        resp.body = json.dumps(runningStyleStats, ensure_ascii=False)

