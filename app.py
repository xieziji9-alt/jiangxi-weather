from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Tuple

import requests
from flask import Flask, jsonify, render_template, request


class WeatherServiceError(RuntimeError):
    """Raised when the remote weather service cannot be reached or parsed."""


app = Flask(__name__)


@dataclass(frozen=True)
class Location:
    id: str
    province: str
    city: str
    latitude: float
    longitude: float


_LOCATION_NAME_MAP: Dict[str, Tuple[str, str]] = {
    "nanchang": ("\u6c5f\u897f\u7701", "\u5357\u660c\u5e02"),
    "nanchang_donghu": ("\u6c5f\u897f\u7701", "\u4e1c\u6e56\u533a"),
    "nanchang_xihu": ("\u6c5f\u897f\u7701", "\u897f\u6e56\u533a"),
    "nanchang_qingyunpu": ("\u6c5f\u897f\u7701", "\u9752\u4e91\u8c31\u533a"),
    "nanchang_honggutan": ("\u6c5f\u897f\u7701", "\u7ea2\u8c37\u6ee9\u533a"),
    "nanchang_qingshanhu": ("\u6c5f\u897f\u7701", "\u9752\u5c71\u6e56\u533a"),
    "nanchang_xinjian": ("\u6c5f\u897f\u7701", "\u65b0\u5efa\u533a"),
    "nanchang_nanchangxian": ("\u6c5f\u897f\u7701", "\u5357\u660c\u53bf"),
    "nanchang_anyi": ("\u6c5f\u897f\u7701", "\u5b89\u4e49\u53bf"),
    "nanchang_jinxian": ("\u6c5f\u897f\u7701", "\u8fdb\u8d24\u53bf"),
    "jingdezhen": ("\u6c5f\u897f\u7701", "\u666f\u5fb7\u9547\u5e02"),
    "jingdezhen_changjiang": ("\u6c5f\u897f\u7701", "\u660c\u6c5f\u533a"),
    "jingdezhen_zhushan": ("\u6c5f\u897f\u7701", "\u73e0\u5c71\u533a"),
    "jingdezhen_fuliang": ("\u6c5f\u897f\u7701", "\u6d6e\u6881\u53bf"),
    "jingdezhen_leping": ("\u6c5f\u897f\u7701", "\u4e50\u5e73\u5e02"),
    "pingxiang": ("\u6c5f\u897f\u7701", "\u840d\u4e61\u5e02"),
    "pingxiang_anyuan": ("\u6c5f\u897f\u7701", "\u5b89\u6e90\u533a"),
    "pingxiang_xiangdong": ("\u6c5f\u897f\u7701", "\u6e58\u4e1c\u533a"),
    "pingxiang_lianhua": ("\u6c5f\u897f\u7701", "\u83b2\u82b1\u53bf"),
    "pingxiang_shangli": ("\u6c5f\u897f\u7701", "\u4e0a\u6817\u53bf"),
    "pingxiang_luxi": ("\u6c5f\u897f\u7701", "\u82a6\u6eaa\u53bf"),
    "jiujiang": ("\u6c5f\u897f\u7701", "\u4e5d\u6c5f\u5e02"),
    "jiujiang_lianxi": ("\u6c5f\u897f\u7701", "\u6fc2\u6eaa\u533a"),
    "jiujiang_xunyang": ("\u6c5f\u897f\u7701", "\u6d54\u9633\u533a"),
    "jiujiang_chaishang": ("\u6c5f\u897f\u7701", "\u67f4\u6851\u533a"),
    "jiujiang_wuning": ("\u6c5f\u897f\u7701", "\u6b66\u5b81\u53bf"),
    "jiujiang_xiushui": ("\u6c5f\u897f\u7701", "\u4fee\u6c34\u53bf"),
    "jiujiang_yongxiu": ("\u6c5f\u897f\u7701", "\u6c38\u4fee\u53bf"),
    "jiujiang_dean": ("\u6c5f\u897f\u7701", "\u5fb7\u5b89\u53bf"),
    "jiujiang_duchang": ("\u6c5f\u897f\u7701", "\u90fd\u660c\u53bf"),
    "jiujiang_hukou": ("\u6c5f\u897f\u7701", "\u6e56\u53e3\u53bf"),
    "jiujiang_pengze": ("\u6c5f\u897f\u7701", "\u5f6d\u6cfd\u53bf"),
    "jiujiang_ruichang": ("\u6c5f\u897f\u7701", "\u745e\u660c\u5e02"),
    "jiujiang_gongqing": ("\u6c5f\u897f\u7701", "\u5171\u9752\u57ce\u5e02"),
    "jiujiang_lushan": ("\u6c5f\u897f\u7701", "\u5e90\u5c71\u5e02"),
    "xinyu": ("\u6c5f\u897f\u7701", "\u65b0\u4f59\u5e02"),
    "xinyu_yushui": ("\u6c5f\u897f\u7701", "\u6e1d\u6c34\u533a"),
    "xinyu_fenyi": ("\u6c5f\u897f\u7701", "\u5206\u5b9c\u53bf"),
    "yingtan": ("\u6c5f\u897f\u7701", "\u9e70\u6f6d\u5e02"),
    "yingtan_yuehu": ("\u6c5f\u897f\u7701", "\u6708\u6e56\u533a"),
    "yingtan_yujiang": ("\u6c5f\u897f\u7701", "\u4f59\u6c5f\u533a"),
    "yingtan_guixi": ("\u6c5f\u897f\u7701", "\u8d35\u6eaa\u5e02"),
    "ganzhou": ("\u6c5f\u897f\u7701", "\u8d63\u5dde\u5e02"),
    "ganzhou_zhanggong": ("\u6c5f\u897f\u7701", "\u7ae0\u8d21\u533a"),
    "ganzhou_nankang": ("\u6c5f\u897f\u7701", "\u5357\u5eb7\u533a"),
    "ganzhou_ganxian": ("\u6c5f\u897f\u7701", "\u8d63\u53bf\u533a"),
    "ganzhou_xinfeng": ("\u6c5f\u897f\u7701", "\u4fe1\u4e30\u53bf"),
    "ganzhou_dayu": ("\u6c5f\u897f\u7701", "\u5927\u4f59\u53bf"),
    "ganzhou_shangyou": ("\u6c5f\u897f\u7701", "\u4e0a\u72b9\u53bf"),
    "ganzhou_chongyi": ("\u6c5f\u897f\u7701", "\u5d07\u4e49\u53bf"),
    "ganzhou_anyuan": ("\u6c5f\u897f\u7701", "\u5b89\u8fdc\u53bf"),
    "ganzhou_longnan": ("\u6c5f\u897f\u7701", "\u9f99\u5357\u5e02"),
    "ganzhou_dingnan": ("\u6c5f\u897f\u7701", "\u5b9a\u5357\u53bf"),
    "ganzhou_quannan": ("\u6c5f\u897f\u7701", "\u5168\u5357\u53bf"),
    "ganzhou_ningdu": ("\u6c5f\u897f\u7701", "\u5b81\u90fd\u53bf"),
    "ganzhou_yudu": ("\u6c5f\u897f\u7701", "\u4e8e\u90fd\u53bf"),
    "ganzhou_xingguo": ("\u6c5f\u897f\u7701", "\u5174\u56fd\u53bf"),
    "ganzhou_huichang": ("\u6c5f\u897f\u7701", "\u4f1a\u660c\u53bf"),
    "ganzhou_xunwu": ("\u6c5f\u897f\u7701", "\u5bfb\u4e4c\u53bf"),
    "ganzhou_shicheng": ("\u6c5f\u897f\u7701", "\u77f3\u57ce\u53bf"),
    "ganzhou_ruijin": ("\u6c5f\u897f\u7701", "\u745e\u91d1\u5e02"),
    "jian": ("\u6c5f\u897f\u7701", "\u5409\u5b89\u5e02"),
    "jian_jizhou": ("\u6c5f\u897f\u7701", "\u5409\u5dde\u533a"),
    "jian_qingyuan": ("\u6c5f\u897f\u7701", "\u9752\u539f\u533a"),
    "jian_jianxian": ("\u6c5f\u897f\u7701", "\u5409\u5b89\u53bf"),
    "jian_jishui": ("\u6c5f\u897f\u7701", "\u5409\u6c34\u53bf"),
    "jian_xiajiang": ("\u6c5f\u897f\u7701", "\u5ce1\u6c5f\u53bf"),
    "jian_xingan": ("\u6c5f\u897f\u7701", "\u65b0\u5e72\u53bf"),
    "jian_yongfeng": ("\u6c5f\u897f\u7701", "\u6c38\u4e30\u53bf"),
    "jian_taihe": ("\u6c5f\u897f\u7701", "\u6cf0\u548c\u53bf"),
    "jian_suichuan": ("\u6c5f\u897f\u7701", "\u9042\u5ddd\u53bf"),
    "jian_wanan": ("\u6c5f\u897f\u7701", "\u4e07\u5b89\u53bf"),
    "jian_anfu": ("\u6c5f\u897f\u7701", "\u5b89\u798f\u53bf"),
    "jian_yongxin": ("\u6c5f\u897f\u7701", "\u6c38\u65b0\u53bf"),
    "jian_jinggangshan": ("\u6c5f\u897f\u7701", "\u4e95\u5188\u5c71\u5e02"),
    "yichun": ("\u6c5f\u897f\u7701", "\u5b9c\u6625\u5e02"),
    "yichun_yuanzhou": ("\u6c5f\u897f\u7701", "\u8881\u5dde\u533a"),
    "yichun_fengxin": ("\u6c5f\u897f\u7701", "\u5949\u65b0\u53bf"),
    "yichun_wanzai": ("\u6c5f\u897f\u7701", "\u4e07\u8f7d\u53bf"),
    "yichun_shanggao": ("\u6c5f\u897f\u7701", "\u4e0a\u9ad8\u53bf"),
    "yichun_yifeng": ("\u6c5f\u897f\u7701", "\u5b9c\u4e30\u53bf"),
    "yichun_jingan": ("\u6c5f\u897f\u7701", "\u9756\u5b89\u53bf"),
    "yichun_tonggu": ("\u6c5f\u897f\u7701", "\u94dc\u9f13\u53bf"),
    "yichun_fengcheng": ("\u6c5f\u897f\u7701", "\u4e30\u57ce\u5e02"),
    "yichun_zhangshu": ("\u6c5f\u897f\u7701", "\u6a1f\u6811\u5e02"),
    "yichun_gaoan": ("\u6c5f\u897f\u7701", "\u9ad8\u5b89\u5e02"),
    "fuzhou": ("\u6c5f\u897f\u7701", "\u629a\u5dde\u5e02"),
    "fuzhou_linchuan": ("\u6c5f\u897f\u7701", "\u4e34\u5ddd\u533a"),
    "fuzhou_dongxiang": ("\u6c5f\u897f\u7701", "\u4e1c\u4e61\u533a"),
    "fuzhou_nancheng": ("\u6c5f\u897f\u7701", "\u5357\u57ce\u53bf"),
    "fuzhou_lichuan": ("\u6c5f\u897f\u7701", "\u9ece\u5ddd\u53bf"),
    "fuzhou_nanfeng": ("\u6c5f\u897f\u7701", "\u5357\u4e30\u53bf"),
    "fuzhou_chongren": ("\u6c5f\u897f\u7701", "\u5d07\u4ec1\u53bf"),
    "fuzhou_lean": ("\u6c5f\u897f\u7701", "\u4e50\u5b89\u53bf"),
    "fuzhou_yihuang": ("\u6c5f\u897f\u7701", "\u5b9c\u9ec4\u53bf"),
    "fuzhou_jinxi": ("\u6c5f\u897f\u7701", "\u91d1\u6eaa\u53bf"),
    "fuzhou_zixi": ("\u6c5f\u897f\u7701", "\u8d44\u6eaa\u53bf"),
    "fuzhou_guangchang": ("\u6c5f\u897f\u7701", "\u5e7f\u660c\u53bf"),
    "shangrao": ("\u6c5f\u897f\u7701", "\u4e0a\u9976\u5e02"),
    "shangrao_xinzhou": ("\u6c5f\u897f\u7701", "\u4fe1\u5dde\u533a"),
    "shangrao_guangfeng": ("\u6c5f\u897f\u7701", "\u5e7f\u4e30\u533a"),
    "shangrao_guangxin": ("\u6c5f\u897f\u7701", "\u5e7f\u4fe1\u533a"),
    "shangrao_yushan": ("\u6c5f\u897f\u7701", "\u7389\u5c71\u53bf"),
    "shangrao_qianshan": ("\u6c5f\u897f\u7701", "\u94c5\u5c71\u53bf"),
    "shangrao_hengfeng": ("\u6c5f\u897f\u7701", "\u6a2a\u5cf0\u53bf"),
    "shangrao_yiyang": ("\u6c5f\u897f\u7701", "\u5f0b\u9633\u53bf"),
    "shangrao_yugan": ("\u6c5f\u897f\u7701", "\u4f59\u5e72\u53bf"),
    "shangrao_poyang": ("\u6c5f\u897f\u7701", "\u9131\u9633\u53bf"),
    "shangrao_wannian": ("\u6c5f\u897f\u7701", "\u4e07\u5e74\u53bf"),
    "shangrao_wuyuan": ("\u6c5f\u897f\u7701", "\u5a7a\u6e90\u53bf"),
    "shangrao_dexing": ("\u6c5f\u897f\u7701", "\u5fb7\u5174\u5e02"),
}

_LOCATION_COORDS: List[Tuple[str, float, float]] = [
    ("nanchang", 28.682, 115.858),
    ("nanchang_donghu", 28.691, 115.899),
    ("nanchang_xihu", 28.656, 115.877),
    ("nanchang_qingyunpu", 28.626, 115.915),
    ("nanchang_honggutan", 28.705, 115.823),
    ("nanchang_qingshanhu", 28.704, 115.959),
    ("nanchang_xinjian", 28.872, 115.820),
    ("nanchang_nanchangxian", 28.542, 115.942),
    ("nanchang_anyi", 28.837, 115.553),
    ("nanchang_jinxian", 28.365, 116.268),
    ("jingdezhen", 29.268, 117.201),
    ("jingdezhen_changjiang", 29.267, 117.205),
    ("jingdezhen_zhushan", 29.303, 117.214),
    ("jingdezhen_fuliang", 29.711, 117.214),
    ("jingdezhen_leping", 28.979, 117.129),
    ("pingxiang", 27.628, 113.854),
    ("pingxiang_anyuan", 27.625, 113.883),
    ("pingxiang_xiangdong", 27.639, 113.732),
    ("pingxiang_lianhua", 27.128, 113.959),
    ("pingxiang_shangli", 27.877, 113.795),
    ("pingxiang_luxi", 27.628, 114.041),
    ("jiujiang", 29.707, 116.002),
    ("jiujiang_lianxi", 29.672, 116.007),
    ("jiujiang_xunyang", 29.734, 115.988),
    ("jiujiang_chaishang", 29.608, 115.915),
    ("jiujiang_wuning", 29.267, 115.103),
    ("jiujiang_xiushui", 29.024, 114.573),
    ("jiujiang_yongxiu", 29.019, 115.823),
    ("jiujiang_dean", 29.327, 115.762),
    ("jiujiang_duchang", 29.274, 116.189),
    ("jiujiang_hukou", 29.738, 116.244),
    ("jiujiang_pengze", 29.896, 116.548),
    ("jiujiang_ruichang", 29.676, 115.674),
    ("jiujiang_gongqing", 29.248, 115.805),
    ("jiujiang_lushan", 29.456, 116.045),
    ("xinyu", 27.817, 114.917),
    ("xinyu_yushui", 27.801, 114.938),
    ("xinyu_fenyi", 27.813, 114.668),
    ("yingtan", 28.241, 117.071),
    ("yingtan_yuehu", 28.239, 117.034),
    ("yingtan_yujiang", 28.207, 116.837),
    ("yingtan_guixi", 28.292, 117.214),
    ("ganzhou", 25.831, 114.940),
    ("ganzhou_zhanggong", 25.856, 114.938),
    ("ganzhou_nankang", 25.654, 114.765),
    ("ganzhou_ganxian", 25.862, 115.018),
    ("ganzhou_xinfeng", 25.386, 114.934),
    ("ganzhou_dayu", 25.395, 114.356),
    ("ganzhou_shangyou", 25.793, 114.540),
    ("ganzhou_chongyi", 25.681, 114.307),
    ("ganzhou_anyuan", 25.135, 115.392),
    ("ganzhou_longnan", 24.912, 114.792),
    ("ganzhou_dingnan", 24.784, 115.028),
    ("ganzhou_quannan", 24.742, 114.531),
    ("ganzhou_ningdu", 26.477, 116.017),
    ("ganzhou_yudu", 25.955, 115.417),
    ("ganzhou_xingguo", 26.321, 115.363),
    ("ganzhou_huichang", 25.600, 115.791),
    ("ganzhou_xunwu", 24.960, 115.651),
    ("ganzhou_shicheng", 26.326, 116.344),
    ("ganzhou_ruijin", 25.885, 116.028),
    ("jian", 27.117, 114.971),
    ("jian_jizhou", 27.117, 114.993),
    ("jian_qingyuan", 27.097, 114.962),
    ("jian_jianxian", 27.041, 114.907),
    ("jian_jishui", 27.213, 115.134),
    ("jian_xiajiang", 27.582, 115.322),
    ("jian_xingan", 27.740, 115.399),
    ("jian_yongfeng", 27.317, 115.435),
    ("jian_taihe", 26.806, 114.909),
    ("jian_suichuan", 26.323, 114.516),
    ("jian_wanan", 26.458, 114.786),
    ("jian_anfu", 27.393, 114.620),
    ("jian_yongxin", 26.944, 114.240),
    ("jian_jinggangshan", 26.570, 114.165),
    ("yichun", 27.804, 114.383),
    ("yichun_yuanzhou", 27.809, 114.389),
    ("yichun_fengxin", 28.688, 115.389),
    ("yichun_wanzai", 28.105, 114.444),
    ("yichun_shanggao", 28.238, 114.933),
    ("yichun_yifeng", 28.394, 114.787),
    ("yichun_jingan", 28.861, 115.361),
    ("yichun_tonggu", 28.525, 114.370),
    ("yichun_fengcheng", 28.159, 115.771),
    ("yichun_zhangshu", 28.055, 115.546),
    ("yichun_gaoan", 28.420, 115.372),
    ("fuzhou", 27.951, 116.358),
    ("fuzhou_linchuan", 27.946, 116.311),
    ("fuzhou_dongxiang", 28.236, 116.603),
    ("fuzhou_nancheng", 27.558, 116.638),
    ("fuzhou_lichuan", 27.282, 116.907),
    ("fuzhou_nanfeng", 27.219, 116.531),
    ("fuzhou_chongren", 27.760, 116.059),
    ("fuzhou_lean", 27.428, 115.830),
    ("fuzhou_yihuang", 27.546, 116.236),
    ("fuzhou_jinxi", 27.918, 116.756),
    ("fuzhou_zixi", 27.706, 117.061),
    ("fuzhou_guangchang", 26.838, 116.335),
    ("shangrao", 28.444, 117.963),
    ("shangrao_xinzhou", 28.431, 117.971),
    ("shangrao_guangfeng", 28.437, 118.196),
    ("shangrao_guangxin", 28.448, 117.906),
    ("shangrao_yushan", 28.682, 118.244),
    ("shangrao_qianshan", 28.315, 117.711),
    ("shangrao_hengfeng", 28.407, 117.596),
    ("shangrao_yiyang", 28.395, 117.449),
    ("shangrao_yugan", 28.700, 116.695),
    ("shangrao_poyang", 29.008, 116.695),
    ("shangrao_wannian", 28.707, 117.066),
    ("shangrao_wuyuan", 29.247, 117.861),
    ("shangrao_dexing", 28.947, 117.578),
]

JIANGXI_LOCATIONS: List[Location] = [
    Location(
        id=loc_id,
        province=_LOCATION_NAME_MAP[loc_id][0],
        city=_LOCATION_NAME_MAP[loc_id][1],
        latitude=lat,
        longitude=lon,
    )
    for loc_id, lat, lon in _LOCATION_COORDS
]


WEATHER_CODE_DESCRIPTIONS: Dict[int, str] = {
    0: "\u6674\u6717",
    1: "\u5c11\u4e91",
    2: "\u591a\u4e91",
    3: "\u9634\u5929",
    45: "\u6709\u96fe",
    48: "\u96fe\u51c7",
    51: "\u6bdb\u6bdb\u96e8",
    53: "\u4e2d\u7b49\u6bdb\u6bdb\u96e8",
    55: "\u5927\u6bdb\u6bdb\u96e8",
    56: "\u51bb\u6bdb\u6bdb\u96e8",
    57: "\u5f3a\u51bb\u6bdb\u6bdb\u96e8",
    61: "\u5c0f\u96e8",
    63: "\u4e2d\u96e8",
    65: "\u5927\u96e8",
    66: "\u51bb\u96e8",
    67: "\u5f3a\u51bb\u96e8",
    71: "\u5c0f\u96ea",
    73: "\u4e2d\u96ea",
    75: "\u5927\u96ea",
    77: "\u96ea\u7c92",
    80: "\u96f6\u661f\u5c0f\u9635\u96e8",
    81: "\u96f6\u661f\u4e2d\u9635\u96e8",
    82: "\u96f6\u661f\u5927\u9635\u96e8",
    85: "\u5c0f\u9635\u96ea",
    86: "\u5927\u9635\u96ea",
    95: "\u96f7\u9635\u96e8",
    96: "\u96f7\u9635\u96e8\u4f34\u6709\u5c0f\u51b0\u96f9",
    99: "\u96f7\u9635\u96e8\u4f34\u6709\u5927\u51b0\u96f9",
}


def _format_time(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return value


def _weather_description(code: int | None) -> str:
    return WEATHER_CODE_DESCRIPTIONS.get(code or -1, "\u5929\u6c14\u72b6\u51b5\u672a\u77e5")


def fetch_weather(location: Location) -> Dict[str, Any]:
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current_weather": True,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "weathercode",
        ],
        "timezone": "Asia/Shanghai",
        "forecast_days": 5,
    }
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise WeatherServiceError("\u5929\u6c14\u670d\u52a1\u6682\u65f6\u4e0d\u53ef\u7528\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002") from exc

    if "current_weather" not in payload or "daily" not in payload:
        raise WeatherServiceError("\u5929\u6c14\u6570\u636e\u4e0d\u5b8c\u6574\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5\u3002")

    current = payload["current_weather"]
    daily = payload["daily"]

    daily_forecast: List[Dict[str, Any]] = []
    days = min(
        len(daily.get("time", [])),
        len(daily.get("temperature_2m_max", [])),
        len(daily.get("temperature_2m_min", [])),
        len(daily.get("precipitation_probability_max", [])),
        len(daily.get("weathercode", [])),
    )
    for idx in range(days):
        code = daily["weathercode"][idx]
        daily_forecast.append(
            {
                "date": daily["time"][idx],
                "temperature_max": daily["temperature_2m_max"][idx],
                "temperature_min": daily["temperature_2m_min"][idx],
                "precipitation_probability": daily["precipitation_probability_max"][idx],
                "weathercode": code,
                "weather": _weather_description(code),
            }
        )

    return {
        "current": {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "winddirection": current.get("winddirection"),
            "weathercode": current.get("weathercode"),
            "weather": _weather_description(current.get("weathercode")),
            "time": _format_time(current.get("time")),
        },
        "daily": daily_forecast,
    }


def _find_location(city_id: str | None) -> Location | None:
    if not city_id:
        return None
    city_id = city_id.lower()
    for location in JIANGXI_LOCATIONS:
        if location.id == city_id:
            return location
    return None


@app.route("/")
def index() -> str:
    locations_sorted = sorted(JIANGXI_LOCATIONS, key=lambda c: (c.province, c.city))
    default_location = locations_sorted[0]
    initial_forecast = None
    load_error = None
    try:
        initial_forecast = fetch_weather(default_location)
    except WeatherServiceError as exc:
        load_error = str(exc)

    locations_json = [asdict(location) for location in locations_sorted]

    return render_template(
        "index.html",
        locations=locations_sorted,
        locations_json=locations_json,
        default_location=default_location,
        initial_forecast=initial_forecast,
        load_error=load_error,
    )


@app.get("/api/weather")
def api_weather():
    city_id = request.args.get("city")
    location = _find_location(city_id)
    if not location:
        return jsonify({"error": "\u8bf7\u9009\u62e9\u6709\u6548\u7684\u57ce\u5e02\u6216\u53bf\u533a\u3002"}), 400
    try:
        forecast = fetch_weather(location)
    except WeatherServiceError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(
        {
            "city": {
                "province": location.province,
                "city": location.city,
                "id": location.id,
                "latitude": location.latitude,
                "longitude": location.longitude,
            },
            "forecast": forecast,
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)

