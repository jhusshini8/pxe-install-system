<template>
  <div :class="className" :style="{height:height,width:width}"></div>
</template>

<script>
  import echarts from 'echarts'
  require('echarts/theme/macarons') // echarts theme
  import { debounce } from '@/utils'
  import { fetchbread } from '@/api/remote-search'
  export default {
    props: {
      className: {
        type: String,
        default: 'chart'
      },
      width: {
        type: String,
        default: '100%'
      },
      height: {
        type: String,
        default: '300px'
      }
    },
    data() {
      return {
        chart: null
      }
    },
    mounted() {
      this.initChart()
      this.__resizeHanlder = debounce(() => {
        if (this.chart) {
          this.chart.resize()
        }
      }, 100)
      window.addEventListener('resize', this.__resizeHanlder)
    },
    beforeDestroy() {
      if (!this.chart) {
        return
      }
      window.removeEventListener('resize', this.__resizeHanlder)
      this.chart.dispose()
      this.chart = null
    },
    methods: {
      initChart() {
        this.chart = echarts.init(this.$el, 'macarons')
          this.setOptions()
      },
      setOptions() {
        fetchbread().then(response => {
          // console.log(JSON.parse(JSON.stringify(response.temp)))
          this.chart.setOption({
            tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
              left: 'center',
              bottom: '10',
              // data: ['Industries', 'Technology', 'Forex', 'Gold', 'Forecasts']
              data:  response.data
            },
            calculable: true,
            series: [
              {
                name: '安装操作系统比例',
                type: 'pie',
                roseType: 'radius',
                radius: [15, 95],
                center: ['50%', '38%'],
                // data: [{'name':'centos7.8','value': 300},{'name':'centos6.4','value': 300}, {'name':'centos6.8','value': 300}],
                // data: [{'name':'centos7.8','value': 300}, {'name':'centos6.4','value': 300},{'name':'centos6.8','value': 300}]
                data:response.temp,
                animationEasing: 'cubicInOut',
                animationDuration: 2600
              }
            ]
          })
        });
      }
    }
  }
</script>
