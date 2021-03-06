import requests
import datetime
from lxml import etree

dict = {'枣庄': '101121401', '綦江': '101043300', '湖州': '101210201', '临夏': '101161101', '福州': '101230101',
        '天门': '101201501', '龙岩': '101230701', '新余': '101241001', '渭南': '101110501', '南平': '101230901',
        '奉贤': '101021000', '白山': '101060901', '宜昌': '101200901', '平谷': '101011500', '昭通': '101291001',
        '长治': '101100501', '荣昌': '101042700', '内江': '101271201', '眉山': '101271501', '果洛': '101150501',
        '琼中': '101310208', '玉溪': '101290701', '静海': '101030900', '湛江': '101281001', '涪陵': '101041400',
        '信阳': '101180601', '博乐': '101131601', '北京城区': '101012200', '天水': '101160901', '杭州': '101210101',
        '上饶': '101240301', '昌吉': '101130401', '阿拉尔': '101130701', '凯里': '101260501', '莆田': '101230401',
        '云阳': '101041700', '合肥': '101220101', '万盛': '101040600', '宁德': '101230301', '塔城': '101131101',
        '彭水': '101043200', '泉州': '101230501', '武清': '101030200', '北海': '101301301', '成都': '101270101',
        '阿坝': '101271901', '南川': '101040400', '东方': '101310202', '武都': '101161001', '昌都': '101140501',
        '郴州': '101250501', '临河': '101080801', '延吉': '101060301', '酉阳': '101043400', '哈尔滨': '101050101',
        '铜梁': '101042800', '厦门': '101230201', '吐鲁番': '101130501', '汕尾': '101282101', '鸡西': '101051101',
        '大兴安岭': '101050701', '三明': '101230801', '伊春': '101050801', '雅安': '101271701', '忻州': '101101001',
        '常德': '101250601', '珠海': '101280701', '平凉': '101160301', '盐城': '101190701', '宝山': '101020300',
        '南昌': '101240101', '菏泽': '101121001', '崇左': '101300201', '吕梁': '101101100', '十堰': '101201101',
        '衡水': '101090801', '浦东': '101021300', '沈阳': '101070101', '高雄': '101340201', '日照': '101121501',
        '黄石': '101200601', '红河': '101290301', '武汉': '101200101', '武隆': '101043100', '娄底': '101250801',
        '渝北': '101040700', '扬州': '101190601', '北京': '101010100', '六盘水': '101260801', '巢湖': '101221601',
        '津南': '101031000', '沧州': '101090701', '安阳': '101180201', '塘沽': '101031100', '临汾': '101100701',
        '保亭': '101310214', '大同': '101100201', '汤河口': '101011800', '荆州': '101200801', '海南': '101150401',
        '许昌': '101180401', '秦皇岛': '101091101', '拉萨': '101140101', '顺义': '101010400', '合作': '101161201',
        '黄南': '101150301', '张家界': '101251101', '定安': '101310209', '温州': '101210701', '齐齐哈尔': '101050201',
        '双鸭山': '101051301', '贺州': '101300701', '泰州': '101191201', '梅州': '101280401', '张掖': '101160701',
        '阿里': '101140701', '本溪': '101070501', '秀山': '101043600', '威海': '101121301', '淮安': '101190901',
        '遂宁': '101270701', '定西': '101160201', '晋中': '101100401', '包头': '101080201', '乌海': '101080301',
        '璧山': '101042900', '荆门': '101201401', '德州': '101120401', '锦州': '101070701', '晋江': '101230509',
        '宝鸡': '101110901', '台北县': '101340101', '白银': '101161301', '景德镇': '101240801', '周口': '101181401',
        '固原': '101170401', '兴义': '101260906', '佳木斯': '101050401', '临沧': '101291101', '商丘': '101181001',
        '密云': '101011300', '丰台': '101010900', '丽江': '101291401', '大兴': '101011100', '林芝': '101140401',
        '芜湖': '101220301', '焦作': '101181101', '阿克苏': '101130801', '儋州': '101310205', '新乡': '101180301',
        '永州': '101251401', '九江': '101240201', '中卫': '101170501', '邢台': '101090901', '和田': '101131301',
        '密云上甸子': '101011900', '石河子': '101130301', '潍坊': '101120601', '铜陵': '101221301', '咸宁': '101200701',
        '遵义': '101260201', '玉树': '101150601', '琼山': '101310102', '常州': '101191101', '赤峰': '101080601',
        '南通': '101190501', '铜川': '101111001', '汉沽': '101030800', '海北': '101150801', '平顶山': '101180501',
        '崇明': '101021100', '攀枝花': '101270201', '贵港': '101300801', '酒泉': '101160801', '沙坪坝': '101043700',
        '铁岭': '101071101', '山南': '101140301', '汉中': '101110801', '丰都': '101043000', '西沙': '101310217',
        '城口': '101041600', '库尔勒': '101130601', '甘孜': '101271801', '桂林': '101300501', '门头沟': '101011400',
        '澄迈': '101310204', '开封': '101180801', '辽源': '101060701', '奉节': '101041900', '吴忠': '101170301',
        '贵阳': '101260101', '黄山': '101221001', '莱芜': '101121601', '太原': '101100101', '潮州': '101281501',
        '惠州': '101280301', '达州': '101270601', '通辽': '101080501', '防城港': '101301401', '延安': '101110300',
        '辽阳': '101071001', '濮阳': '101181301', '长沙': '101250101', '乌鲁木齐': '101130101', '德阳': '101272001',
        '黔阳': '101251301', '广州': '101280101', '香格里拉': '101291301', '西安': '101110101', '商洛': '101110601',
        '乐东': '101310221', '云浮': '101281401', '玉林': '101300901', '淮南': '101220401', '泸州': '101271001',
        '吉首': '101251501', '自贡': '101270301', '临沂': '101120901', '乐山': '101271401', '合川': '101040300',
        '天津': '101030100', '屯昌': '101310210', '曲靖': '101290401', '文昌': '101310212', '阜阳': '101220801',
        '昆明': '101290101', '南沙岛': '101310220', '梁平': '101042300', '宁河': '101030700', '济宁': '101120701',
        '巫溪': '101041800', '海口': '101310101', '益阳': '101250700', '唐山': '101090501', '通化': '101060501',
        '连云港': '101191001', '嘉兴': '101210301', '陵水': '101310216', '呼伦贝尔': '101081000', '武威': '101160501',
        '松江': '101020900', '喀什': '101130901', '五指山': '101310222', '聊城': '101121701', '安庆': '101220601',
        '大足': '101042600', '凉山': '101271601', '张家口': '101090301', '河源': '101281201', '巴南': '101040900',
        '松原': '101060801', '昌平': '101010700', '吉安': '101240601', '衢州': '101211001', '保山': '101290501',
        '北碚': '101040800', '广安': '101270801', '延庆': '101010800', '庆阳': '101160401', '随州': '101201301',
        '黄冈': '101200501', '海淀': '101010200', '万宁': '101310215', '克拉玛依': '101130201', '廊坊': '101090601',
        '烟台': '101120501', '邵阳': '101250901', '亳州': '101220901', '无锡': '101190201', '钦州': '101301101',
        '垫江': '101042200', '怀化': '101251201', '六安': '101221501', '清远': '101281301', '北辰': '101030600',
        '鹰潭': '101241101', '深圳': '101280601', '大庆': '101050901', '文山': '101290601', '滁州': '101221101',
        '鄂州': '101200301', '舟山': '101211101', '吉林': '101060201', '宜宾': '101271101', '营口': '101070801',
        '宿州': '101220701', '百色': '101301001', '运城': '101100801', '阳江': '101281801', '梧州': '101300601',
        '河池': '101301201', '万州龙宝': '101041300', '西青': '101030500', '徐家汇': '101021200', '朔州': '101100901',
        '蓟县': '101031400', '南充': '101270501', '金华': '101210901', '白沙': '101310207', '丹东': '101070601',
        '马鞍山': '101220501', '神农架': '101201201', '忠县': '101042400', '徐州': '101190801', '临高': '101310203',
        '霞云岭': '101012100', '阿图什': '101131501', '湘潭': '101250201', '恩施': '101201001', '鄂尔多斯': '101080701',
        '昌江': '101310206', '抚顺': '101070401', '宿迁': '101191301', '楚雄': '101290801', '那曲': '101140601',
        '阜新': '101070901', '榆林': '101110401', '咸阳': '101110200', '金昌': '101160601', '茂名': '101282001',
        '南阳': '101180701', '长寿': '101041000', '佛爷顶': '101011700', '江门': '101281101', '黑河': '101050601',
        '安康': '101110701', '怒江': '101291201', '三门峡': '101181701', '宁波': '101210401', '景洪': '101291601',
        '襄樊': '101200201', '肇庆': '101280901', '衡阳': '101250401', '郑州': '101180101', '宣城': '101221401',
        '锡林浩特': '101080901', '都匀': '101260401', '铜仁': '101260601', '普洱': '101290901', '中山': '101281701',
        '黔江': '101041100', '青岛': '101120201', '保定': '101090201', '重庆': '101040100', '揭阳': '101281901',
        '海东': '101150201', '斋堂': '101012000', '阳泉': '101100301', '伊宁': '101131001', '济源': '101181801',
        '汕头': '101280501', '台州': '101210601', '绵阳': '101270401', '洛阳': '101180901', '资阳': '101271301',
        '漯河': '101181501', '房山': '101011200', '来宾': '101300401', '嘉峪关': '101161401', '泰安': '101120801',
        '柳州': '101300301', '江津': '101040500', '白城': '101060601', '开县': '101041500', '通州': '101010600',
        '呼和浩特': '101080101', '淮北': '101221201', '驻马店': '101181601', '石家庄': '101090101', '朝阳': '101010300',
        '漳州': '101230601', '孝感': '101200401', '萍乡': '101240901', '闵行': '101020200', '南宁': '101300101',
        '葫芦岛': '101071401', '西宁': '101150101', '毕节': '101260701', '南汇': '101020600', '宜春': '101240501',
        '石柱': '101042500', '石嘴山': '101170201', '七台河': '101051002', '鞍山': '101070301', '阿勒泰': '101131401',
        '盘锦': '101071301', '邯郸': '101091001', '绍兴': '101210501', '潜江': '101201701', '德宏': '101291501',
        '南京': '101190101', '大港': '101031200', '阿拉善左旗': '101081201', '巴中': '101270901', '永川': '101040200',
        '石景山': '101011000', '潼南': '101042100', '东丽': '101030400', '宝坻': '101030300', '长春': '101060101',
        '镇江': '101190301', '万州天城': '101041200', '巫山': '101042000', '岳阳': '101251001', '赣州': '101240701',
        '日喀则': '101140201', '东莞': '101281601', '鹤岗': '101051201', '青浦': '101020800', '四平': '101060401',
        '抚州': '101240401', '池州': '101221701', '丽水': '101210801', '东营': '101121201', '淄博': '101120301',
        '哈密': '101131201', '苏州': '101190401', '大连': '101070201', '蚌埠': '101220201', '三亚': '101310201',
        '佛山': '101280800', '鹤壁': '101181201', '广元': '101272101', '上海': '101020100', '济南': '101120101',
        '集宁': '101080401', '晋城': '101100601', '嘉定': '101020500', '承德': '101090402', '兰州': '101160101',
        '琼海': '101310211', '银川': '101170101', '海西': '101150701', '株洲': '101250301', '牡丹江': '101050301',
        '怀柔': '101010500', '安顺': '101260301', '韶关': '101280201', '乌兰浩特': '101081101', '绥化': '101050501',
        '金山': '101020700', '仙桃': '101201601', '台中': '101340401', '大理': '101290201', '滨州': '101121101',
        '八达岭': '101011600'}


def get_weather(ip):
    try:
        # url = 'http://api.map.baidu.com/location/ip?ip={}&ak=eqszdP67odvzdVRyzSMsbGPRzhTIgna3&coor=bd09ll'
        # r = requests.get(url.format(ip))
        # city = r.json()['content']['address_detail']['city']
        city = '武汉'
        # print(city)
        city_code = dict.get(city)
        if city_code == None:
            return ''
        url = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(city_code)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        weather = html.xpath('//div[@class="t"]/ul[@class="clearfix"]')[0]
        time = weather.xpath('./li/h1/text()')  # 时间
        wea = weather.xpath('./li/p[@class="wea"]/@title')  # 天气
        wind_direction = weather.xpath('./li/p[@class="win"]/span/@title')  # 风向
        wind_size = weather.xpath('./li/p[@class="win"]/span/text()')  # 风大小
        temperature = weather.xpath('./li/p[@class="tem"]/span/text()')  # 气温

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hour = date[11:13]
        if int(hour) > 18:
            key = 1
        else:
            key = 0
        return city + ':' + time[key] + ' ' + wea[key] + ' ' + wind_direction[key] + wind_size[key] + ' ' + temperature[
            key] + '℃'
    except Exception as e:
        print(e)
        return ''

if __name__ == '__main__':


    ip = '192.168.13.31'

    url = 'http://api.map.baidu.com/location/ip?ip={}&ak=eqszdP67odvzdVRyzSMsbGPRzhTIgna3&coor=bd09ll'
    r = requests.get(url.format(ip))
    print(r.json()['content']['address_detail']['city'])
