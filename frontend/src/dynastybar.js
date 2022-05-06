var seasonsBar = echarts.init(document.getElementById('dynastiesbar'));
seasonsBar.setOption({
    
    tooltip: {},
    xAxis: {
        data: ['先秦', '两汉', '魏晋', '南北朝', '隋代','唐代','五代','宋代','金朝','元代','明代','清代','近现代','未知']
    },
    yAxis: {},
    series: [
        {
            type: 'bar',
            data: [441, 221, 138, 161, 11, 2395, 160, 2139, 47, 286, 207, 437, 125, 30],
            itemStyle: {
                normal: {
                    color: function (params) {

                        var colorList = [

                            '#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B',

                            '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',

                            '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'

                        ];

                        return colorList[params.dataIndex]
                    }
                }
            }
        }
    ]
});
