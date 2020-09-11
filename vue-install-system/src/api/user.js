import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'http://system-django.int.jumei.com/api/login/',
    // url: 'http://127.0.0.1:8100/api/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: 'http://system-django.int.jumei.com/api/userinfo/',
    // url: 'http://127.0.0.1:8100/api/userinfo/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: 'http://system-django.int.jumei.com/api/logout/',
    // url: 'http://127.0.0.1:8100/api/logout/',
    method: 'post'
  })
}
