from flask import Flask, request, render_template
import pymysql
import weather

app = Flask(__name__)
app.jinja_env.variable_start_string = '(('
app.jinja_env.variable_end_string = '))'


def connect_sql(sql):
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='demo', charset='utf8')
        cs1 = con.cursor()
        cs1.execute(sql)
        result = cs1.fetchall()
        con.close()
        cs1.close()
    except Exception as e:
        print(e)
        return ()
    return result


@app.route('/')
def index():
    wea = weather.get_weather(str(request.remote_addr))
    return render_template('index.html',weather = wea)


@app.route('/baidu', methods=['post', 'get'])
def baidu():
    baidu_time = request.values.get('baidu_time')
    baidu_avg = request.values.get('baidu_avg')
    avg_temp_html = []
    datas_html = []
    if baidu_time != None:
        if len(baidu_time) <= 2:
            sql = "select city,avg(lat),avg(lng),avg({}) from `2018` where date like '{}%' group by city;".format(
                baidu_avg, baidu_time)
            result = connect_sql(sql)
            for i in result:
                dict = {}
                dict['lat'] = i[1]
                dict['lng'] = i[2]
                dict['count'] = str(i[3])
                avg_temp_html.append(dict)
        else:
            baidu_time = baidu_time.split(',')
            baidu_time = "date like'" + "%' or date like '".join(baidu_time) + "%'"
            sql = "select city,avg(lat),avg(lng),avg({}) from `2018` where {} group by city;".format(baidu_avg,
                                                                                                     baidu_time)
            result = connect_sql(sql)
            for i in result:
                dict = {}
                dict['lat'] = i[1]
                dict['lng'] = i[2]
                dict['count'] = str(i[3])
                avg_temp_html.append(dict)
    result1 = connect_sql('select * from travel_location')
    for j in result1:
        dict1 = {}
        dict1['name'] = j[1]
        dict1['address'] = j[2]
        dict1['lat'] = j[3]
        dict1['lng'] = j[4]
        datas_html.append(dict1)
    return render_template('baidu_map.html', avg_temp_html=avg_temp_html, datas_html=datas_html)


if __name__ == '__main__':
    # print(app.url_map)
    app.run(host="0.0.0.0", port = 8080)
