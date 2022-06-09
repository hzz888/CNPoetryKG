var JosnList = [{ "name": "李白", "value": "387" }, { "name": "苏轼", "value": "267" }, { "name": "杜甫", "value": "206" }, { "name": "纳兰性德", "value": "147" }, { "name": "辛弃疾", "value": "130" }, { "name": "白居易", "value": "116" }, { "name": "吴文英", "value": "110" }, { "name": "李商隐", "value": "103" }, { "name": "陆游", "value": "94" }, { "name": "王维", "value": "93" }, { "name": "柳宗元", "value": "90" }, { "name": "陶渊明", "value": "78" }, { "name": "欧阳修", "value": "76" }, { "name": "温庭筠", "value": "73" }, { "name": "李贺", "value": "68" }, { "name": "柳永", "value": "65" }, { "name": "刘禹锡", "value": "63" }, { "name": "韩愈", "value": "63" }, { "name": "岑参", "value": "60" }, { "name": "杜牧", "value": "59" }, { "name": "晏几道", "value": "57" }, { "name": "李清照", "value": "54" }, { "name": "孟浩然", "value": "49" }, { "name": "王安石", "value": "49" }, { "name": "黄庭坚", "value": "49" }, { "name": "毛泽东", "value": "43" }, { "name": "周邦彦", "value": "43" }, { "name": "秦观", "value": "43" }, { "name": "姜夔", "value": "42" }, { "name": "韦庄", "value": "41" }, { "name": "元好问", "value": "36" }, { "name": "王国维", "value": "35" }, { "name": "杨万里", "value": "34" }, { "name": "李煜", "value": "34" }, { "name": "范成大", "value": "33" }, { "name": "高适", "value": "31" }, { "name": "王昌龄", "value": "30" }, { "name": "屈原", "value": "29" }, { "name": "贺铸", "value": "29" }, { "name": "韦应物", "value": "28" }, { "name": "晏殊", "value": "27" }, { "name": "曹雪芹", "value": "26" }, { "name": "张可久", "value": "25" }, { "name": "王建", "value": "23" }, { "name": "左丘明", "value": "23" }, { "name": "鲁迅", "value": "23" }, { "name": "乔吉", "value": "23" }, { "name": "马致远", "value": "20" }, { "name": "王勃", "value": "20" }];
var optionFour = {
    tooltip: {
        show: true
    },
    series: [{
        name: '诗人词云',
        type: 'wordCloud',
        sizeRange: [30, 50],//文字范围
        //文本旋转范围，文本将通过rotationStep45在[-90,90]范围内随机旋转
        rotationRange: [-45, 90],
        rotationStep: 45,
        textRotation: [0, 45, 90, -45],
        //形状
        shape: 'circle',
        layoutAnimation: true,
        textStyle: {

            color: function () {
                return 'rgb(' + [
                    Math.round(Math.random() * 200),
                    Math.round(Math.random() * 200),
                    Math.round(Math.random() * 100)
                ].join(',') + ')';
            },

            //悬停上去的字体的阴影设置
            emphasis: {
                textStyle: {
                    shadowBlur: 10,
                    shadowColor: '#333'
                }

            }
        },
        data: JosnList
    }]
};
var doubleWordChart = echarts.init(document.getElementById('authorcloud'));
//使用制定的配置项和数据显示图表
doubleWordChart.setOption(optionFour);