var map = new BMap.Map("container"); // 创建地图实例

var point = new BMap.Point(114.315035, 30.600954);
map.centerAndZoom(point, 6); // 初始化地图，设置中心点坐标和地图级别
map.setCurrentCity("武汉");
map.addControl(new BMap.MapTypeControl());
map.enableScrollWheelZoom(); // 允许滚轮缩放

// 列表，每一项是一个json，json的项依次为纬度、经度、权重
// [{'lat':31.247482648, 'lng':117.23726383682, 'count':32.45362}]
var avg_points = ((avg_temp_html | tojson | safe));
// var avg_points = [{
// 	'lat': 31.247482648,
// 	'lng': 117.23726383682,
// 	'count': 32.45362
// }];
// [{'name':'武汉黄鹤楼', 'address':'湖北省武汉市', 'lat': 30.550317764282227, 'lng': 114.30904388427734}]
var travel_points = ((datas_html | tojson | safe));
// var travel_points = [{
// 	'name': '武汉黄鹤楼',
// 	'address': '湖北省武汉市',
// 	'lat': 30.550317764282227,
// 	'lng': 114.30904388427734
// }];

if(!isSupportCanvas()) {
	alert('热力图目前只支持有canvas支持的浏览器,您所使用的浏览器不能使用热力图功能~')
}
//详细的参数,可以查看heatmap.js的文档 https://github.com/pa7/heatmap.js/blob/master/README.md
//参数说明如下:
/* visible 热力图是否显示,默认为true
 * opacity 热力的透明度,1-100
 * radius 势力图的每个点的半径大小
 * gradient  {JSON} 热力图的渐变区间 . gradient如下所示
 *	{
        .2:'rgb(0, 255, 255)',
        .5:'rgb(0, 110, 255)',
        .8:'rgb(100, 0, 255)'
    }
    其中 key 表示插值的位置, 0~1.
        value 为颜色值.
 */
heatmapOverlay = new BMapLib.HeatmapOverlay({
	"radius": 30
});
map.addOverlay(heatmapOverlay);
heatmapOverlay.setDataSet({
	data: avg_points,
	max: 50
});

// 开启热力图
function openHeatmap() {
	heatmapOverlay.show();
}

// 关闭热力图
function closeHeatmap() {
	heatmapOverlay.hide();
}

// 默认开启热力图
openHeatmap();

function setGradient() {
	/*格式如下所示:
       {
             0:'rgb(102, 255, 0)',
             .5:'rgb(255, 170, 0)',
             1:'rgb(255, 0, 0)'
       }*/
	var gradient = {};
	var colors = document.querySelectorAll("input[type='color']");
	colors = [].slice.call(colors, 0);
	colors.forEach(function(ele) {
		gradient[ele.getAttribute("data-key")] = ele.value;
	});
	heatmapOverlay.setOptions({
		"gradient": gradient
	});
}

//判断浏览区是否支持canvas
function isSupportCanvas() {
	var elem = document.createElement('canvas');
	return !!(elem.getContext && elem.getContext('2d'));
}

// 添加标记的方法
function addMarker(travel_points) {
	//循环建立标注点
	for(var i = 0, travel_pointsLen = travel_points.length; i < travel_pointsLen; i++) {
		var point = new BMap.Point(travel_points[i].lng, travel_points[i].lat); //将标注点转化成地图上的点
		var marker = new BMap.Marker(point); //将点转化成标注点

		map.addOverlay(marker); //将标注点添加到地图上
		//添加监听事件
		(function() {
			var thePoint = travel_points[i];
			marker.addEventListener("click",
				function() {
					showInfo(this, thePoint);
				});
		})();
	}
}

// 清除标记的方法
function clearMarker() {
	// 隐藏推荐的景点
	document.getElementById("info").style.display = "none";
	//修改content的宽度
	document.getElementById("content").style.width = "80%";
	//修改main的宽度
	document.getElementById("main").style.width = "100%";
	var len = map.getOverlays().length;
	for(var j = 0; j < len; j++) {
		if(map.getOverlays()[j].toString() === "[object Marker]") {
			map.removeOverlay(map.getOverlays()[j]);
		}
	}
	if(map.getOverlays().length > 2) {
		clearMarker()
	}
}

// 点击标记之后显示的信息
function showInfo(thisMarker, point) {
	//获取点的信息
	var sContent =
		'<ul style="margin:0 0 5px 0;padding:0.2em 0">' +
		'<li style="line-height: 26px;font-size: 15px;">' +
		'<span style="width: 50px;display: inline-block;">景点：</span>' + point.name + '</li>' +
		'<li style="line-height: 26px;font-size: 15px;">' +
		'<span style="width: 50px;display: inline-block;">地址：</span>' + point.address + '</li>' +
		'</ul>';
	var infoWindow = new BMap.InfoWindow(sContent); //创建信息窗口对象
	thisMarker.openInfoWindow(infoWindow); //图片加载完后重绘infoWindow
	console.log(123);
	// 显示推荐的景点
	document.getElementById("info").style.display = "block";
	//修改content的宽度
	document.getElementById("content").style.width = "100%";
	//修改main的宽度
	document.getElementById("main").style.width = "72%";
}

// 开启景点标记
function mark_on() {
	addMarker(travel_points);
	// change_mark_image()
}

// 修改标记样式
function change_mark_image() {
	// 修改标记样式
	var spanlist = document.querySelectorAll('#container > div:nth-child(1) > div:nth-child(2) > div:nth-child(5) > span');
	for(var i = 0; i < spanlist.length; i++) {
		spanlist[i].getElementsByTagName('div')[0].getElementsByTagName('img')[0].src = 'static/image.png';
	}
}

// 关闭景点标记
function mark_off() {
	clearMarker();
}