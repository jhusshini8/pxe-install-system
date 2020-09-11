import request from '@/utils/request'

export function fetchList(query) {
  return request({
    // url: '/vue-element-admin/article/list',
    // url: 'http://system-django.int.jumei.com/api/getdetail/',
    url: 'http://127.0.0.1:8100/api/getdetail/',
    method: 'get',
    params: query
  })
}

export function statustag(data) {
  return request({
    // url: 'http://system-django.int.jumei.com/api/statustag/',
    url: 'http://127.0.0.1:8100/api/statustag/',
    method: 'post',
    data
  })
}

export function fetchArticle(id) {
  return request({
    // url: 'http://system-django.int.jumei.com/vue-element-admin/article/detail',
    url: 'http://127.0.0.1:8100/vue-element-admin/article/detail',
    method: 'get',
    params: { id }
  })
}

export function fetchPv(pv) {
  return request({
    url: 'http://system-django.int.jumei.com/vue-element-admin/article/pv',
    method: 'get',
    params: { pv }
  })
}

export function createArticle(data) {
  return request({
    // url: 'http://system-django.int.jumei.com/api/beganinstall/',
    url: 'http://127.0.0.1:8100/api/beganinstall/',
    method: 'post',
    data
  })
}

export function repassArticle(data) {
  return request({
    // url: 'http://system-django.int.jumei.com/api/usereditpass/',
    url: 'http://127.0.0.1:8100/api/usereditpass/',
    method: 'post',
    data
  })
}

export function updateArticle(data) {
  return request({
    // url: 'http://system-django.int.jumei.com/api/beganinstall/',
    url: 'http://127.0.0.1:8100/api/beganinstall/',
    method: 'post',
    data
  })
}
