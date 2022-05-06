var seasonsBar = echarts.init(document.getElementById('seasonsbar'));
seasonsBar.setOption({
    
    tooltip: {},
    xAxis: {
        data: ['春', '夏', '秋', '冬']
    },
    yAxis: {},
    series: [
        {
            type: 'bar',
            data: [2394, 231, 1565, 158],
            itemStyle: {
                normal: {
                    color: function (params) {
                        var colorList = [

                            'green', 'red', 'orange', 'lightblue'

                        ];

                        return colorList[params.dataIndex]
                    }
                }
            }
        }
            
    ]
});
    