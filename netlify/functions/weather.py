import json
import requests
from typing import NamedTuple, Optional
from datetime import datetime

class Location(NamedTuple):
    id: str
    province: str
    city: str
    latitude: float
    longitude: float

# 江西省市县坐标数据
_LOCATION_NAME_MAP = {
    "nanchang": "\u5357\u660c\u5e02",
    "donghu": "\u4e1c\u6e56\u533a",
    "xihu": "\u897f\u6e56\u533a",
    "qingyunpu": "\u9752\u4e91\u8c31\u533a",
    "qingshanhu": "\u9752\u5c71\u6e56\u533a",
    "xinjian": "\u65b0\u5efa\u533a",
    "nanchang_county": "\u5357\u660c\u53bf",
    "anyi": "\u5b89\u4e49\u53bf",
    "jinxian": "\u8fdb\u8d24\u53bf",
    "jiujiang": "\u4e5d\u6c5f\u5e02",
    "xunyang": "\u6d54\u9633\u533a",
    "lianxi": "\u6fe2\u6eaa\u533a",
    "chaisang": "\u67f4\u6851\u533a",
    "wuning": "\u6b66\u5b81\u53bf",
    "xiushui": "\u4fee\u6c34\u53bf",
    "yongxiu": "\u6c38\u4fee\u53bf",
    "dean": "\u5fb7\u5b89\u53bf",
    "duchang": "\u90fd\u660c\u53bf",
    "hukou": "\u6e56\u53e3\u53bf",
    "pengze": "\u5f6d\u6cfd\u53bf",
    "ruichang": "\u745e\u660c\u5e02",
    "gongqingcheng": "\u5171\u9752\u57ce\u5e02",
    "lushan": "\u5e90\u5c71\u5e02",
    "shangrao": "\u4e0a\u9976\u5e02",
    "xinzhou": "\u4fe1\u5dde\u533a",
    "guangfeng": "\u5e7f\u4e30\u533a",
    "guangxin": "\u5e7f\u4fe1\u533a",
    "yugan": "\u4f59\u5e72\u53bf",
    "poyang": "\u9131\u9633\u53bf",
    "wannian": "\u4e07\u5e74\u53bf",
    "wuyuan": "\u5a7a\u6e90\u53bf",
    "dexing": "\u5fb7\u5174\u5e02",
    "yiyang": "\u5f0b\u9633\u53bf",
    "hengfeng": "\u6a2a\u5cf0\u53bf",
    "qianshan": "\u94c5\u5c71\u53bf",
    "yushan": "\u7389\u5c71\u53bf",
    "ganzhou": "\u8d63\u5dde\u5e02",
    "zhanggong": "\u7ae0\u8d21\u533a",
    "nankang": "\u5357\u5eb7\u533a",
    "ganxian": "\u8d63\u53bf\u533a",
    "xinfeng": "\u4fe1\u4e30\u53bf",
    "dayu": "\u5927\u4f59\u53bf",
    "shangyou": "\u4e0a\u7336\u53bf",
    "chongyi": "\u5d07\u4e49\u53bf",
    "anyuan": "\u5b89\u8fdc\u53bf",
    "longnan": "\u9f99\u5357\u53bf",
    "dingnan": "\u5b9a\u5357\u53bf",
    "quannan": "\u5168\u5357\u53bf",
    "ningdu": "\u5b81\u90fd\u53bf",
    "yudu": "\u4e8e\u90fd\u53bf",
    "xingguo": "\u5174\u56fd\u53bf",
    "huichang": "\u4f1a\u660c\u53bf",
    "xunwu": "\u5bfb\u4e4c\u53bf",
    "shicheng": "\u77f3\u57ce\u53bf",
    "ruijin": "\u745e\u91d1\u5e02",
    "jian": "\u5409\u5b89\u5e02",
    "jizhou": "\u5409\u5dde\u533a",
    "qingyuan": "\u9752\u539f\u533a",
    "jishui": "\u5409\u6c34\u53bf",
    "jian_county": "\u5409\u5b89\u53bf",
    "xingan": "\u65b0\u5e72\u53bf",
    "yongfeng": "\u6c38\u4e30\u53bf",
    "taihe": "\u6cf0\u548c\u53bf",
    "suichuan": "\u9042\u5ddd\u53bf",
    "wanan": "\u4e07\u5b89\u53bf",
    "anfu": "\u5b89\u798f\u53bf",
    "yongxin": "\u6c38\u65b0\u53bf",
    "jinggangshan": "\u4e95\u5188\u5c71\u5e02",
    "yichun": "\u5b9c\u6625\u5e02",
    "yuanzhou": "\u8881\u5dde\u533a",
    "fengxin": "\u5949\u65b0\u53bf",
    "wanzai": "\u4e07\u8f7d\u53bf",
    "shanggao": "\u4e0a\u9ad8\u53bf",
    "yifeng": "\u5b9c\u4e30\u53bf",
    "jing_an": "\u9756\u5b89\u53bf",
    "tonggu": "\u94dc\u9f13\u53bf",
    "fengcheng": "\u4e30\u57ce\u5e02",
    "zhangshu": "\u6a1f\u6811\u5e02",
    "gaoan": "\u9ad8\u5b89\u5e02",
    "fuzhou": "\u629a\u5dde\u5e02",
    "linchuan": "\u4e34\u5ddd\u533a",
    "dongxiang": "\u4e1c\u4e61\u533a",
    "nancheng": "\u5357\u57ce\u53bf",
    "lichuan": "\u9ece\u5ddd\u53bf",
    "nanfeng": "\u5357\u4e30\u53bf",
    "chongren": "\u5d07\u4ec1\u53bf",
    "lean": "\u4e50\u5b89\u53bf",
    "yihuang": "\u5b9c\u9ec4\u53bf",
    "jinxi": "\u91d1\u6eaa\u53bf",
    "zixi": "\u8d44\u6eaa\u53bf",
    "guangchang": "\u5e7f\u660c\u53bf",
    "pingxiang": "\u840d\u4e61\u5e02",
    "anyuan_px": "\u5b89\u6e90\u533a",
    "xiangdong": "\u6e58\u4e1c\u533a",
    "lianhua": "\u83b2\u82b1\u53bf",
    "shangli": "\u4e0a\u6817\u53bf",
    "luxi": "\u82a6\u6eaa\u53bf",
    "xinyu": "\u65b0\u4f59\u5e02",
    "yushui": "\u6e1d\u6c34\u533a",
    "fenyi": "\u5206\u5b9c\u53bf",
    "yingtan": "\u9e70\u6f6d\u5e02",
    "yujiang": "\u4f59\u6c5f\u533a",
    "guixi": "\u8d35\u6eaa\u5e02",
    "jingdezhen": "\u666f\u5fb7\u9547\u5e02",
    "changjiang": "\u660c\u6c5f\u533a",
    "zhushan": "\u73e0\u5c71\u533a",
    "fuliang": "\u6d6e\u6881\u53bf",
    "leping": "\u4e50\u5e73\u5e02"
}

_LOCATION_COORDS = [
    ("nanchang", 28.6820, 115.8579),
    ("donghu", 28.6850, 115.8990),
    ("xihu", 28.6560, 115.8770),
    ("qingyunpu", 28.6210, 115.9250),
    ("qingshanhu", 28.6820, 115.9620),
    ("xinjian", 28.6920, 115.8150),
    ("nanchang_county", 28.5450, 115.9430),
    ("anyi", 28.8450, 115.5480),
    ("jinxian", 28.3760, 116.2360),
    ("jiujiang", 29.7050, 116.0010),
    ("xunyang", 29.7280, 115.9900),
    ("lianxi", 29.6700, 115.9850),
    ("chaisang", 29.6000, 115.9110),
    ("wuning", 29.2560, 115.1010),
    ("xiushui", 29.0250, 114.5470),
    ("yongxiu", 29.0220, 115.8090),
    ("dean", 29.3170, 115.7560),
    ("duchang", 29.2730, 116.1740),
    ("hukou", 29.7410, 116.2150),
    ("pengze", 29.8960, 116.5490),
    ("ruichang", 29.6740, 115.6810),
    ("gongqingcheng", 29.2460, 115.8040),
    ("lushan", 29.4490, 115.9820),
    ("shangrao", 28.4540, 117.9430),
    ("xinzhou", 28.4330, 117.9670),
    ("guangfeng", 28.4350, 118.1910),
    ("guangxin", 28.3190, 117.9750),
    ("yugan", 28.6950, 116.6940),
    ("poyang", 29.0110, 116.6730),
    ("wannian", 28.6950, 117.0690),
    ("wuyuan", 29.2450, 117.8610),
    ("dexing", 28.9470, 117.5790),
    ("yiyang", 28.3790, 117.8080),
    ("hengfeng", 28.4070, 117.5960),
    ("qianshan", 28.3090, 117.2080),
    ("yushan", 28.6820, 118.2450),
    ("ganzhou", 25.8310, 114.9340),
    ("zhanggong", 25.8170, 114.9350),
    ("nankang", 25.6630, 114.7650),
    ("ganxian", 25.8460, 115.0120),
    ("xinfeng", 25.7690, 114.2090),
    ("dayu", 25.1140, 114.3620),
    ("shangyou", 25.8880, 114.5500),
    ("chongyi", 25.6810, 114.3080),
    ("anyuan", 24.9220, 115.3930),
    ("longnan", 24.9110, 114.7890),
    ("dingnan", 24.7840, 115.0280),
    ("quannan", 24.7420, 114.5300),
    ("ningdu", 26.4700, 116.0090),
    ("yudu", 25.9520, 115.4140),
    ("xingguo", 26.3380, 115.3630),
    ("huichang", 25.5840, 115.7860),
    ("xunwu", 24.9540, 115.6490),
    ("shicheng", 26.3150, 116.3440),
    ("ruijin", 25.8850, 116.0270),
    ("jian", 27.1170, 114.9860),
    ("jizhou", 27.1110, 115.0070),
    ("qingyuan", 27.0860, 114.9780),
    ("jishui", 27.2290, 115.1350),
    ("jian_county", 27.0390, 114.9990),
    ("xingan", 27.3880, 115.3960),
    ("yongfeng", 27.3180, 115.4410),
    ("taihe", 26.7910, 114.9090),
    ("suichuan", 26.3130, 114.5200),
    ("wanan", 26.4580, 114.7860),
    ("anfu", 27.3930, 114.6200),
    ("yongxin", 26.9450, 114.2430),
    ("jinggangshan", 26.7480, 114.2890),
    ("yichun", 27.8150, 114.4170),
    ("yuanzhou", 27.7970, 114.4230),
    ("fengxin", 28.7770, 115.4000),
    ("wanzai", 28.1060, 114.4450),
    ("shanggao", 28.2330, 114.9250),
    ("yifeng", 28.3920, 114.7800),
    ("jing_an", 28.8620, 115.3620),
    ("tonggu", 28.5230, 114.3710),
    ("fengcheng", 28.1920, 115.7710),
    ("zhangshu", 28.0530, 115.5460),
    ("gaoan", 28.4170, 115.3750),
    ("fuzhou", 27.9490, 116.3580),
    ("linchuan", 27.9770, 116.3130),
    ("dongxiang", 28.2360, 116.5900),
    ("nancheng", 27.5540, 116.6380),
    ("lichuan", 27.4180, 116.9080),
    ("nanfeng", 27.2180, 116.5250),
    ("chongren", 27.7540, 116.0750),
    ("lean", 27.4280, 115.8300),
    ("yihuang", 27.5540, 116.2360),
    ("jinxi", 27.9450, 116.7550),
    ("zixi", 27.7340, 117.0610),
    ("guangchang", 26.8440, 116.3370),
    ("pingxiang", 27.6230, 113.8520),
    ("anyuan_px", 27.6150, 113.8700),
    ("xiangdong", 27.6390, 113.7200),
    ("lianhua", 27.1270, 113.9620),
    ("shangli", 27.8800, 114.0100),
    ("luxi", 27.6290, 114.0290),
    ("xinyu", 27.8180, 114.9170),
    ("yushui", 27.8170, 114.9440),
    ("fenyi", 27.8150, 114.6750),
    ("yingtan", 28.2380, 117.0330),
    ("yujiang", 28.2150, 116.8180),
    ("guixi", 28.2920, 117.2120),
    ("jingdezhen", 29.2686, 117.1786),
    ("changjiang", 29.2730, 117.1860),
    ("zhushan", 29.3010, 117.2150),
    ("fuliang", 29.3380, 117.2150),
    ("leping", 28.9620, 117.1300)
}

JIANGXI_LOCATIONS = [
    Location(
        id=loc_id,
        province="\u6c5f\u897f\u7701",
        city=_LOCATION_NAME_MAP[loc_id],
        latitude=lat,
        longitude=lon
    )
    for loc_id, lat, lon in _LOCATION_COORDS
]

WEATHER_CODE_DESCRIPTIONS = {
    0: "\u6674\u5929",
    1: "\u4e3b\u8981\u6674\u5929",
    2: "\u90e8\u5206\u591a\u4e91",
    3: "\u9634\u5929",
    45: "\u96fe",
    48: "\u51bb\u96fe",
    51: "\u5c0f\u96e8",
    53: "\u4e2d\u96e8",
    55: "\u5927\u96e8",
    56: "\u51bb\u96e8",
    57: "\u5927\u51bb\u96e8",
    61: "\u5c0f\u96e8",
    63: "\u4e2d\u96e8",
    65: "\u5927\u96e8",
    66: "\u51bb\u96e8",
    67: "\u5927\u51bb\u96e8",
    71: "\u5c0f\u96ea",
    73: "\u4e2d\u96ea",
    75: "\u5927\u96ea",
    77: "\u96ea\u7c92",
    80: "\u9635\u96e8",
    81: "\u4e2d\u9635\u96e8",
    82: "\u5927\u9635\u96e8",
    85: "\u5c0f\u9635\u96ea",
    86: "\u5927\u9635\u96ea",
    95: "\u96f7\u9635\u96e8",
    96: "\u96f7\u9635\u96e8\u4f34\u51b0\u96f9",
    99: "\u5927\u96f7\u9635\u96e8\u4f34\u51b0\u96f9"
}

def fetch_weather(location: Location) -> Optional[dict]:
    """Fetch weather data from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "Asia/Shanghai",
        "forecast_days": 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        weather_code = current.get("weather_code", 0)
        weather_desc = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "\u672a\u77e5")
        
        forecast = []
        if daily:
            dates = daily.get("time", [])
            codes = daily.get("weather_code", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            
            for i in range(min(5, len(dates))):
                day_code = codes[i] if i < len(codes) else 0
                day_desc = WEATHER_CODE_DESCRIPTIONS.get(day_code, "\u672a\u77e5")
                forecast.append({
                    "date": dates[i],
                    "weather": day_desc,
                    "max_temp": round(max_temps[i], 1) if i < len(max_temps) else None,
                    "min_temp": round(min_temps[i], 1) if i < len(min_temps) else None
                })
        
        return {
            "location": {
                "province": location.province,
                "city": location.city
            },
            "current": {
                "temperature": round(current.get("temperature_2m", 0), 1),
                "feels_like": round(current.get("apparent_temperature", 0), 1),
                "humidity": current.get("relative_humidity_2m", 0),
                "wind_speed": round(current.get("wind_speed_10m", 0), 1),
                "weather": weather_desc,
                "weather_code": weather_code
            },
            "forecast": forecast
        }
    except Exception as e:
        return None

def handler(event, context):
    """Netlify Function handler."""
    # Parse query parameters
    params = event.get("queryStringParameters", {})
    location_id = params.get("location_id", "nanchang")
    
    # Find location
    location = None
    for loc in JIANGXI_LOCATIONS:
        if loc.id == location_id:
            location = loc
            break
    
    if not location:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Location not found"}, ensure_ascii=False)
        }
    
    # Fetch weather
    weather_data = fetch_weather(location)
    
    if not weather_data:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Failed to fetch weather data"}, ensure_ascii=False)
        }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(weather_data, ensure_ascii=False)
    }

