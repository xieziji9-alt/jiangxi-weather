// 江西省市县坐标数据
const LOCATION_NAME_MAP = {
  "nanchang": "南昌市",
  "donghu": "东湖区",
  "xihu": "西湖区",
  "qingyunpu": "青云谱区",
  "qingshanhu": "青山湖区",
  "xinjian": "新建区",
  "nanchang_county": "南昌县",
  "anyi": "安义县",
  "jinxian": "进贤县",
  "jiujiang": "九江市",
  "xunyang": "浔阳区",
  "lianxi": "濂溪区",
  "chaisang": "柴桑区",
  "wuning": "武宁县",
  "xiushui": "修水县",
  "yongxiu": "永修县",
  "dean": "德安县",
  "duchang": "都昌县",
  "hukou": "湖口县",
  "pengze": "彭泽县",
  "ruichang": "瑞昌市",
  "gongqingcheng": "共青城市",
  "lushan": "庐山市",
  "shangrao": "上饶市",
  "xinzhou": "信州区",
  "guangfeng": "广丰区",
  "guangxin": "广信区",
  "yugan": "余干县",
  "poyang": "鄱阳县",
  "wannian": "万年县",
  "wuyuan": "婺源县",
  "dexing": "德兴市",
  "yiyang": "弋阳县",
  "hengfeng": "横峰县",
  "qianshan": "铅山县",
  "yushan": "玉山县",
  "ganzhou": "赣州市",
  "zhanggong": "章贡区",
  "nankang": "南康区",
  "ganxian": "赣县区",
  "xinfeng": "信丰县",
  "dayu": "大余县",
  "shangyou": "上犹县",
  "chongyi": "崇义县",
  "anyuan": "安远县",
  "longnan": "龙南县",
  "dingnan": "定南县",
  "quannan": "全南县",
  "ningdu": "宁都县",
  "yudu": "于都县",
  "xingguo": "兴国县",
  "huichang": "会昌县",
  "xunwu": "寻乌县",
  "shicheng": "石城县",
  "ruijin": "瑞金市",
  "jian": "吉安市",
  "jizhou": "吉州区",
  "qingyuan": "青原区",
  "jishui": "吉水县",
  "jian_county": "吉安县",
  "xingan": "新干县",
  "yongfeng": "永丰县",
  "taihe": "泰和县",
  "suichuan": "遂川县",
  "wanan": "万安县",
  "anfu": "安福县",
  "yongxin": "永新县",
  "jinggangshan": "井冈山市",
  "yichun": "宜春市",
  "yuanzhou": "袁州区",
  "fengxin": "奉新县",
  "wanzai": "万载县",
  "shanggao": "上高县",
  "yifeng": "宜丰县",
  "jing_an": "靖安县",
  "tonggu": "铜鼓县",
  "fengcheng": "丰城市",
  "zhangshu": "樟树市",
  "gaoan": "高安市",
  "fuzhou": "抚州市",
  "linchuan": "临川区",
  "dongxiang": "东乡区",
  "nancheng": "南城县",
  "lichuan": "黎川县",
  "nanfeng": "南丰县",
  "chongren": "崇仁县",
  "lean": "乐安县",
  "yihuang": "宜黄县",
  "jinxi": "金溪县",
  "zixi": "资溪县",
  "guangchang": "广昌县",
  "pingxiang": "萍乡市",
  "anyuan_px": "安源区",
  "xiangdong": "湘东区",
  "lianhua": "莲花县",
  "shangli": "上栗县",
  "luxi": "芦溪县",
  "xinyu": "新余市",
  "yushui": "渝水区",
  "fenyi": "分宜县",
  "yingtan": "鹰潭市",
  "yujiang": "余江区",
  "guixi": "贵溪市",
  "jingdezhen": "景德镇市",
  "changjiang": "昌江区",
  "zhushan": "珠山区",
  "fuliang": "浮梁县",
  "leping": "乐平市"
};

const LOCATION_COORDS = {
  "nanchang": [28.6820, 115.8579],
  "donghu": [28.6850, 115.8990],
  "xihu": [28.6560, 115.8770],
  "qingyunpu": [28.6210, 115.9250],
  "qingshanhu": [28.6820, 115.9620],
  "xinjian": [28.6920, 115.8150],
  "nanchang_county": [28.5450, 115.9430],
  "anyi": [28.8450, 115.5480],
  "jinxian": [28.3760, 116.2360],
  "jiujiang": [29.7050, 116.0010],
  "xunyang": [29.7280, 115.9900],
  "lianxi": [29.6700, 115.9850],
  "chaisang": [29.6000, 115.9110],
  "wuning": [29.2560, 115.1010],
  "xiushui": [29.0250, 114.5470],
  "yongxiu": [29.0220, 115.8090],
  "dean": [29.3170, 115.7560],
  "duchang": [29.2730, 116.1740],
  "hukou": [29.7410, 116.2150],
  "pengze": [29.8960, 116.5490],
  "ruichang": [29.6740, 115.6810],
  "gongqingcheng": [29.2460, 115.8040],
  "lushan": [29.4490, 115.9820],
  "shangrao": [28.4540, 117.9430],
  "xinzhou": [28.4330, 117.9670],
  "guangfeng": [28.4350, 118.1910],
  "guangxin": [28.3190, 117.9750],
  "yugan": [28.6950, 116.6940],
  "poyang": [29.0110, 116.6730],
  "wannian": [28.6950, 117.0690],
  "wuyuan": [29.2450, 117.8610],
  "dexing": [28.9470, 117.5790],
  "yiyang": [28.3790, 117.8080],
  "hengfeng": [28.4070, 117.5960],
  "qianshan": [28.3090, 117.2080],
  "yushan": [28.6820, 118.2450],
  "ganzhou": [25.8310, 114.9340],
  "zhanggong": [25.8170, 114.9350],
  "nankang": [25.6630, 114.7650],
  "ganxian": [25.8460, 115.0120],
  "xinfeng": [25.7690, 114.2090],
  "dayu": [25.1140, 114.3620],
  "shangyou": [25.8880, 114.5500],
  "chongyi": [25.6810, 114.3080],
  "anyuan": [24.9220, 115.3930],
  "longnan": [24.9110, 114.7890],
  "dingnan": [24.7840, 115.0280],
  "quannan": [24.7420, 114.5300],
  "ningdu": [26.4700, 116.0090],
  "yudu": [25.9520, 115.4140],
  "xingguo": [26.3380, 115.3630],
  "huichang": [25.5840, 115.7860],
  "xunwu": [24.9540, 115.6490],
  "shicheng": [26.3150, 116.3440],
  "ruijin": [25.8850, 116.0270],
  "jian": [27.1170, 114.9860],
  "jizhou": [27.1110, 115.0070],
  "qingyuan": [27.0860, 114.9780],
  "jishui": [27.2290, 115.1350],
  "jian_county": [27.0390, 114.9990],
  "xingan": [27.3880, 115.3960],
  "yongfeng": [27.3180, 115.4410],
  "taihe": [26.7910, 114.9090],
  "suichuan": [26.3130, 114.5200],
  "wanan": [26.4580, 114.7860],
  "anfu": [27.3930, 114.6200],
  "yongxin": [26.9450, 114.2430],
  "jinggangshan": [26.7480, 114.2890],
  "yichun": [27.8150, 114.4170],
  "yuanzhou": [27.7970, 114.4230],
  "fengxin": [28.7770, 115.4000],
  "wanzai": [28.1060, 114.4450],
  "shanggao": [28.2330, 114.9250],
  "yifeng": [28.3920, 114.7800],
  "jing_an": [28.8620, 115.3620],
  "tonggu": [28.5230, 114.3710],
  "fengcheng": [28.1920, 115.7710],
  "zhangshu": [28.0530, 115.5460],
  "gaoan": [28.4170, 115.3750],
  "fuzhou": [27.9490, 116.3580],
  "linchuan": [27.9770, 116.3130],
  "dongxiang": [28.2360, 116.5900],
  "nancheng": [27.5540, 116.6380],
  "lichuan": [27.4180, 116.9080],
  "nanfeng": [27.2180, 116.5250],
  "chongren": [27.7540, 116.0750],
  "lean": [27.4280, 115.8300],
  "yihuang": [27.5540, 116.2360],
  "jinxi": [27.9450, 116.7550],
  "zixi": [27.7340, 117.0610],
  "guangchang": [26.8440, 116.3370],
  "pingxiang": [27.6230, 113.8520],
  "anyuan_px": [27.6150, 113.8700],
  "xiangdong": [27.6390, 113.7200],
  "lianhua": [27.1270, 113.9620],
  "shangli": [27.8800, 114.0100],
  "luxi": [27.6290, 114.0290],
  "xinyu": [27.8180, 114.9170],
  "yushui": [27.8170, 114.9440],
  "fenyi": [27.8150, 114.6750],
  "yingtan": [28.2380, 117.0330],
  "yujiang": [28.2150, 116.8180],
  "guixi": [28.2920, 117.2120],
  "jingdezhen": [29.2686, 117.1786],
  "changjiang": [29.2730, 117.1860],
  "zhushan": [29.3010, 117.2150],
  "fuliang": [29.3380, 117.2150],
  "leping": [28.9620, 117.1300]
};

const WEATHER_CODE_DESCRIPTIONS = {
  0: "晴天",
  1: "主要晴天",
  2: "部分多云",
  3: "阴天",
  45: "雾",
  48: "冻雾",
  51: "小雨",
  53: "中雨",
  55: "大雨",
  56: "冻雨",
  57: "大冻雨",
  61: "小雨",
  63: "中雨",
  65: "大雨",
  66: "冻雨",
  67: "大冻雨",
  71: "小雪",
  73: "中雪",
  75: "大雪",
  77: "雪粒",
  80: "阵雨",
  81: "中阵雨",
  82: "大阵雨",
  85: "小阵雪",
  86: "大阵雪",
  95: "雷阵雨",
  96: "雷阵雨伴冰雹",
  99: "大雷阵雨伴冰雹"
};

async function fetchWeather(locationId) {
  const coords = LOCATION_COORDS[locationId];
  const cityName = LOCATION_NAME_MAP[locationId];
  
  if (!coords || !cityName) {
    return null;
  }
  
  const [latitude, longitude] = coords;
  
  const url = new URL('https://api.open-meteo.com/v1/forecast');
  url.searchParams.append('latitude', latitude);
  url.searchParams.append('longitude', longitude);
  url.searchParams.append('current', 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m');
  url.searchParams.append('daily', 'weather_code,temperature_2m_max,temperature_2m_min');
  url.searchParams.append('timezone', 'Asia/Shanghai');
  url.searchParams.append('forecast_days', '5');
  
  try {
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error('Failed to fetch weather data');
    }
    
    const data = await response.json();
    const current = data.current || {};
    const daily = data.daily || {};
    
    const weatherCode = current.weather_code || 0;
    const weatherDesc = WEATHER_CODE_DESCRIPTIONS[weatherCode] || "未知";
    
    const forecast = [];
    if (daily.time) {
      const dates = daily.time;
      const codes = daily.weather_code || [];
      const maxTemps = daily.temperature_2m_max || [];
      const minTemps = daily.temperature_2m_min || [];
      
      for (let i = 0; i < Math.min(5, dates.length); i++) {
        const dayCode = codes[i] || 0;
        const dayDesc = WEATHER_CODE_DESCRIPTIONS[dayCode] || "未知";
        forecast.push({
          date: dates[i],
          weather: dayDesc,
          max_temp: maxTemps[i] ? Math.round(maxTemps[i] * 10) / 10 : null,
          min_temp: minTemps[i] ? Math.round(minTemps[i] * 10) / 10 : null
        });
      }
    }
    
    return {
      location: {
        province: "江西省",
        city: cityName
      },
      current: {
        temperature: Math.round((current.temperature_2m || 0) * 10) / 10,
        feels_like: Math.round((current.apparent_temperature || 0) * 10) / 10,
        humidity: current.relative_humidity_2m || 0,
        wind_speed: Math.round((current.wind_speed_10m || 0) * 10) / 10,
        weather: weatherDesc,
        weather_code: weatherCode
      },
      forecast: forecast
    };
  } catch (error) {
    console.error('Error fetching weather:', error);
    return null;
  }
}

exports.handler = async (event, context) => {
  // Parse query parameters
  const locationId = event.queryStringParameters?.location_id || 'nanchang';
  
  // Fetch weather
  const weatherData = await fetchWeather(locationId);
  
  if (!weatherData) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ error: 'Failed to fetch weather data' })
    };
  }
  
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*'
    },
    body: JSON.stringify(weatherData)
  };
};

