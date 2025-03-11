<template>
  <div>
    <!-- <Chart :cdata="cdata" /> -->
    <div ref="chart" style="width: 100%;height: 480px" v-bind:key="cdata.lineData"
    @mouseenter="startAction" @mouseleave="cancelAction"></div>
  </div>
</template>

<script>
//import Chart from './chart.vue'
export default {
  data () {
    return {
      isHover:true,
      cdata: {
        category: [
          "市区",
          "万州",
          "江北",
          "南岸",
          "北碚",
          "綦南",
          "长寿",
          "永川",
          "璧山",
          "江津",
          "城口",
          "大足",
          "垫江",
          "丰都",
          "奉节",
          "合川",
          "江津区",
          "开州",
          "南川",
          "彭水",
          "黔江",
          "石柱",
          "铜梁",
          "潼南",
          "巫山",
          "巫溪",
          "武隆",
          "秀山",
          "酉阳",
          "云阳",
          "忠县",
          "川东",
          "检修"
        ],
        lineData: [
          18092,
          20728,
          24045,
          28348,
          32808,
          36097,
          39867,
          44715,
          48444,
          50415,
          56061,
          62677,
          59521,
          67560,
          18092,
          20728,
          24045,
          28348,
          32808,
          36097,
          39867,
          44715,
          48444,
          50415,
          36097,
          39867,
          44715,
          48444,
          50415,
          50061,
          32677,
          49521,
          32808
        ],
        barData: [
          4600,
          5000,
          5500,
          6500,
          7500,
          8500,
          9900,
          12500,
          14000,
          21500,
          23200,
          24450,
          25250,
          33300,
          4600,
          5000,
          5500,
          6500,
          7500,
          8500,
          9900,
          22500,
          14000,
          21500,
          8500,
          9900,
          12500,
          14000,
          21500,
          23200,
          24450,
          25250,
          7500
        ],
        rateData: []
      }
    };
  },
  components: {
    //Chart,
  },
  async mounted () {
    const res = await this.$http.get('myApp/bottomLeft')
    this.$set(this.cdata,'category',res.data.brandList)
    this.$set(this.cdata,'lineData',res.data.priceList)
    this.$set(this.cdata,'barData',res.data.volumeList)
    //this.setData();
    //this.initChart();
  },
  updated() {
    this.initChart();
    this.stratDateUpdateInterval();
  },
  methods: {
    // 根据自己的业务情况修改
    // setData () {
    //   for (let i = 0; i < this.cdata.barData.length -1; i++) {
    //     let rate = this.cdata.barData[i] / this.cdata.lineData[i];
    //     this.cdata.rateData.push(rate.toFixed(2));
    //   }
    // },
    startAction(){
      this.isHover = false
    },
    cancelAction(){
      this.isHover = true
    },
    initChart(){
      this.myChart = this.$echarts.init(this.$refs.chart);

      const option={
          tooltip: {
            trigger: "axis",
            backgroundColor: "rgba(255,255,255,0.1)",
            axisPointer: {
              type: "shadow",
              label: {
                show: true,
                backgroundColor: "#7B7DDC"
              }
            }
          },
          dataZone:[
            {
              type:"slider",
              start:0,
              end:95,
              show:false
            }
          ],
          legend: {
            data: ["已贯通", "计划贯通", "贯通率"],
            textStyle: {
              color: "#B4B4B4"
            },
            top: "0%"
          },
          grid: {
            x: "8%",
            width: "88%",
            y: "4%"
          },
          xAxis: {
            data: this.cdata.category,
            axisLine: {
              lineStyle: {
                color: "#B4B4B4"
              }
            },
            axisLabel:{
              show:true,
              interval:0
            },
            axisTick: {
              show: false
            }
          },
          yAxis: [
            {
              splitLine: { show: false },
              axisLine: {
                lineStyle: {
                  color: "#B4B4B4"
                }
              },

              axisLabel: {
                formatter: "{value} "
              }
            },
            {
              splitLine: { show: false },
              axisLine: {
                lineStyle: {
                  color: "#B4B4B4"
                }
              },
              axisLabel: {
                formatter: "{value} "
              }
            }
          ],
          series: [
            {
              name: "贯通率",
              type: "line",
              smooth: true,
              showAllSymbol: true,
              symbol: "emptyCircle",
              symbolSize: 8,
              yAxisIndex: 1,
              itemStyle: {
                normal: {
                  color: "#F02FC2"
                }
              },
              data: this.cdata.lineData
            },
            {
              name: "已贯通",
              type: "bar",
              barWidth: 10,
              itemStyle: {
                normal: {
                  barBorderRadius: 5,
                  color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: "#956FD4" },
                    { offset: 1, color: "#3EACE5" }
                  ])
                }
              },
              data: this.cdata.barData
            },

          ]
        }
        this.myChart.setOption(option);
    },
    changeData(x){
      var st = x[0]
      for(var i =0;i<x.length-1;i++){
        x[i] = x[i+1]
      }
      x[x.length-1] =st
    },
    updateBarChart(){
      if(this.isHover == true){
        this.changeData(this.cdata.category)
      this.changeData(this.cdata.lineData)
      this.changeData(this.cdata.barData)
      console.log(this.cdata.category)
      this.myChart.setOption({
        xAxis:{
          data:this.cdata.category
        },
        series:[
          {
            data:this.cdata.lineData
          },
          {
            data:this.cdata.barData
          }
        ]
      })
      }else{
        clearInterval(this.timer)
      }
    },
    stratDateUpdateInterval(){
      if(this.isHover == true){
        const interval =3000
        clearInterval(this.timer)
        setInterval(this.updateBarChart,interval)
      }
    }
  }
};
</script>

<style lang="scss" scoped>
</style>