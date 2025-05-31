import axios from 'axios'
import { wgs84ToGcj02 } from '@/utils/coordTransform'

const API_BASE_URL = 'http://localhost:5001/api'

const defaultOptions = {
  enableHighAccuracy: true, // 启用高精度
  timeout: 5000, // 超时时间5秒
  maximumAge: 0, // 禁用缓存
}

export async function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('浏览器不支持地理位置获取'))
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log('GPS定位成功：', position)
        // 转换为高德坐标系
        const gcj02Coords = wgs84ToGcj02(position.coords.longitude, position.coords.latitude)
        console.log('转换为高德坐标系：', gcj02Coords)
        resolve({
          longitude: gcj02Coords.longitude,
          latitude: gcj02Coords.latitude,
          accuracy: position.coords.accuracy,
        })
      },
      (error) => {
        let errorMessage = '获取位置失败: '
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage += '请允许网站访问位置信息'
            break
          case error.POSITION_UNAVAILABLE:
            errorMessage += '位置信息不可用'
            break
          case error.TIMEOUT:
            errorMessage += '获取位置超时'
            break
          default:
            errorMessage += error.message
        }
        reject(new Error(errorMessage))
      },
      defaultOptions
    )
  })
}

// 添加位置监听功能
export function watchLocation(onSuccess, onError) {
  if (!navigator.geolocation) {
    onError(new Error('浏览器不支持地理位置获取'))
    return null
  }

  return navigator.geolocation.watchPosition(
    (position) => {
      const gcj02Coords = wgs84ToGcj02(position.coords.longitude, position.coords.latitude)
      onSuccess({
        longitude: gcj02Coords.longitude,
        latitude: gcj02Coords.latitude,
        accuracy: position.coords.accuracy,
      })
    },
    (error) => {
      let errorMessage = '位置监听错误: '
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage += '请允许网站访问位置信息'
          break
        case error.POSITION_UNAVAILABLE:
          errorMessage += '位置信息不可用'
          break
        case error.TIMEOUT:
          errorMessage += '获取位置超时'
          break
        default:
          errorMessage += error.message
      }
      onError(new Error(errorMessage))
    },
    defaultOptions
  )
}

// 清除位置监听
export function clearLocationWatch(watchId) {
  if (watchId && navigator.geolocation) {
    navigator.geolocation.clearWatch(watchId)
  }
}

export async function getNearbyPOIs(location) {
  try {
    const response = await axios.get(`${API_BASE_URL}/nearby_pois`, {
      params: {
        location: `${location.longitude},${location.latitude}`,
      },
    })

    // 转换后端数据格式以匹配前端需求
    return response.data.pois.map((poi) => ({
      id: String(Math.random()),
      name: poi.name,
      distance: `${poi.distance}m`,
      walkTime: Math.round(poi.distance / 80).toString(), // 假设步行速度约为4.8km/h
      takenCount: String(Math.floor(Math.random() * 200 + 100)),
      viewedCount: String(Math.floor(Math.random() * 400 + 200)),
      tagline: '南大地标建筑',
      avatarImage: poi.photo_url,
      images: [poi.photo_url],
      mapUrl: response.data.map_url,
    }))
  } catch (error) {
    console.error('获取附近POI失败:', error)
    throw error
  }
}
