# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, send_from_directory, make_response, Response
import magic
import os
import yaml

with open("configuration.yaml", "r", encoding="utf-8") as f:
    dataMapsd = yaml.safe_load(f)


app = Flask(__name__)

if dataMapsd["configuration"]["Storage"] == "mysql":
    import pymysql
    ismysql = True
    connsx = pymysql.connect(host=dataMapsd["configuration"]["mysql"]["host"], user=dataMapsd["configuration"]["mysql"]["user"], passwd=dataMapsd["configuration"]["mysql"]["passwd"], db='jncloud',
                             port=dataMapsd["configuration"]["mysql"]["port"], charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
else:
    import json
    ismysql = False

app.config['MAX_CONTENT_LENGTH'] = dataMapsd["configuration"]["maxsize"] * 1024 * 1024

app.config['JSON_AS_ASCII'] = False

ALLOWED_EXTENSIONS = set(dataMapsd["configuration"]["type"])


def allowed_file(filename):
    return '.' in filename and \
           str.lower(filename.rsplit('.', 1)[1]) in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html',  cloudname=dataMapsd["configuration"]["name"])


@app.route('/tc/<filename>')
def uploaded_file(filename):
    if ismysql:
        cur = connsx.cursor()
        cur.connection.ping()
        sql = "SELECT * FROM `tuchuan` WHERE name = %s"
        cur.execute(sql, filename)
        data = cur.fetchall()
        cur.close()
        store_path = 'uploads/'+data[0]["md5"]
    else:
        with open("filelist.json", 'r') as f:
            cur = json.load(f)
        for i in cur:
            if i["name"] == filename:
                store_path = 'uploads/'+i["md5"]
                break
    minetpye = magic.from_file(store_path, mime=True)
    if "video" in minetpye and (not request.args.get("download")):
        response = make_response(send_from_directory('uploads',
                                                     data[0]["md5"]))
    else:
        def send_chunk():
            with open(store_path, 'rb') as target_file:
                while True:
                    chunk = target_file.read(1024 * 1024)  # 每次读取20M
                    if not chunk:
                        break
                    yield chunk
        response = Response(send_chunk())
        response.headers['content-length'] = os.stat(str(store_path)).st_size
    if request.args.get("download"):
        response.headers["Content-Type"] = "application/octet-stream"
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=filename.encode('utf-8')
        )
    else:
        if str.lower(filename.rsplit('.', 1)[1]) == "mp3":
            response.headers["Content-Type"] = "audio/mpeg"
        else:
            response.headers["Content-Type"] = minetpye
    return response


@app.route('/icon/<filename>', methods=['GET'])
def icon(filename):
    response = make_response(send_from_directory(
        'icon', filename+'.png'))
    response.headers["Content-Type"] = "image/png"
    return response


@app.route('/tclist', methods=['GET'])
def tclist():
    if (not request.args.get("limit")) or (not request.args.get("offset")):
        return jsonify({"err": "参数欠缺", "author": "junian"})
    else:
        if ismysql:
            curxsd = connsx.cursor()
            curxsd.connection.ping()
            sql = "SELECT name,date FROM `tuchuan` order by id desc limit %s offset %s"
            curxsd.execute(sql, (int(request.args.get("limit")),
                                 int(request.args.get("offset"))))
            datasds = curxsd.fetchall()
            curxsd.close()
        else:
            with open("filelist.json", 'r') as f:
                xsdawe = json.load(f)
                xsdawe.reverse()
                datasds = xsdawe[int(request.args.get("offset")):int(request.args.get("offset"))+int(request.args.get("limit"))]
                print(datasds)
        sdwewqrt = []
        for ix in datasds:
            if len(ix["name"]) >= 24:
                xsdwok = ix["name"][0:18]+"..."
            else:
                xsdwok = ix["name"]
            sdwewqrt.append(
                {
                    "name": xsdwok, "date": ix["date"], "url": str.lower(ix["name"].rsplit('.', 1)[1]), "down": ix["name"]
                }
            )
        return jsonify(sdwewqrt)


@app.route('/uploads', methods=['POST', "PUT"])
def upload_files():
    file = request.files['file']
    if file and allowed_file(file.filename):
        import hashlib
        import time
        md5Name = hashlib.md5(file.read()).hexdigest()
        if not md5Name in os.listdir('uploads'):
            file.seek(0)
            file.save(os.path.join('uploads', md5Name))
        if ismysql:
            curxsd = connsx.cursor()
            curxsd.connection.ping()
            sql = "SELECT * FROM `tuchuan` WHERE name = %s limit 1"
            curxsd.execute(sql, file.filename)
            datasds = curxsd.fetchall()
            if datasds == ():
                sql = "INSERT INTO `tuchuan`(`md5`,`name`,`date`) VALUE(%s,%s,%s)"
                curxsd.execute(sql, (md5Name, file.filename,
                                     time.strftime("%Y/%m/%d %H:%M:%S")))
                connsx.commit()
            curxsd.close()
        else:
            with open("filelist.json", 'r') as f:
                datasds = json.load(f)
                datasds.append({"md5": md5Name, "name": file.filename,
                                "date": time.strftime("%Y/%m/%d %H:%M:%S")})
                with open("filelist.json", 'w') as f:
                    json.dump(datasds, f)
        result = {
            "result": file.filename,
            "author": "junian",
            "update": time.strftime("%Y/%m/%d %H:%M:%S")
        }
        return jsonify(result)
    else:
        return jsonify({"result": '文件类型不支持！'})


if '__main__' == __name__:
    app.run(debug=True)
