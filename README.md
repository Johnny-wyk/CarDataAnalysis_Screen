# CarDataAnalysis_Screen
基于 Vue,ECharts , DataV 构建直观的图表和大屏，展示新能源汽车销售趋势、品牌份额、市场分布
1.数据采集模块
利用 Request 爬虫技术采集新能源汽车的市场销售数据，包括品牌、车型、销量、价格等关键信息。
2.数据可视化模块
利用 ECharts 实现数据的图表展示，如折线图、柱状图、饼图等；
基于 DataV 构建大屏可视化界面，展示实时数据分析结果和市场趋势。
3.用户交互模块
前端使用 Vue 框架，实现数据查询、动态交互和自定义图表展示功能，提升用户体验。

![image](https://github.com/user-attachments/assets/0c1810b2-334e-4a63-9690-6e9a975b2308)

项目环境：Vue-cli-5.x、DataV-2.7.3、Echarts-4.6.0、Webpack-4.0、Npm-9.x、Node-v18。
启动项目需要提前安装好 `nodejs` 与 `pnpm`,下载项目后在项目主目录下运行 `pnpm` 拉取依赖包。安装完依赖包之后然后使用 `vue-cli` 或者直接使用命令`npm run serve`，就可以启动项目，启动项目后需要手动全屏（按 F11）。如果编译项目的时候提示没有 DataV 框架的依赖，输入 `npm install @jiaminghi/data-view` 或者 `yarn add @jiaminghi/data-view` 进行手动安装。
