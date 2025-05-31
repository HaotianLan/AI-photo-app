// WGS84坐标转换为GCJ02坐标
const PI = 3.14159265358979324
const X_PI = (PI * 3000.0) / 180.0

function transformLat(x, y) {
  let ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x))
  ret += ((20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0) / 3.0
  ret += ((20.0 * Math.sin(y * PI) + 40.0 * Math.sin((y / 3.0) * PI)) * 2.0) / 3.0
  ret += ((160.0 * Math.sin((y / 12.0) * PI) + 320 * Math.sin((y * PI) / 30.0)) * 2.0) / 3.0
  return ret
}

function transformLon(x, y) {
  let ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x))
  ret += ((20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0) / 3.0
  ret += ((20.0 * Math.sin(x * PI) + 40.0 * Math.sin((x / 3.0) * PI)) * 2.0) / 3.0
  ret += ((150.0 * Math.sin((x / 12.0) * PI) + 300.0 * Math.sin((x / 30.0) * PI)) * 2.0) / 3.0
  return ret
}

function delta(lat, lon) {
  let a = 6378245.0 // 卫星椭球坐标投影到平面地图坐标系的投影因子
  let ee = 0.00669342162296594323 // 椭球的偏心率
  let dLat = transformLat(lon - 105.0, lat - 35.0)
  let dLon = transformLon(lon - 105.0, lat - 35.0)
  let radLat = (lat / 180.0) * PI
  let magic = Math.sin(radLat)
  magic = 1 - ee * magic * magic
  let sqrtMagic = Math.sqrt(magic)
  dLat = (dLat * 180.0) / (((a * (1 - ee)) / (magic * sqrtMagic)) * PI)
  dLon = (dLon * 180.0) / ((a / sqrtMagic) * Math.cos(radLat) * PI)
  return { lat: dLat, lon: dLon }
}

// WGS84 转 GCJ02
export function wgs84ToGcj02(lon, lat) {
  if (outOfChina(lat, lon)) {
    return { longitude: lon, latitude: lat }
  }
  let d = delta(lat, lon)
  return {
    longitude: lon + d.lon,
    latitude: lat + d.lat,
  }
}

// 判断是否在中国境内
function outOfChina(lat, lon) {
  if (lon < 72.004 || lon > 137.8347) {
    return true
  }
  if (lat < 0.8293 || lat > 55.8271) {
    return true
  }
  return false
}