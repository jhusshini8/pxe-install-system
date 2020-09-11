import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: 'http://system-django.int.jumei.com/api/userlist/',
    // url: 'http://127.0.0.1:8100/api/userlist/',
    method: 'get',
    params: { name }
  })
}

export function transactionList(query) {
  return request({
    url: 'http://system-django.int.jumei.com/api/userlistall/',
    // url: 'http://127.0.0.1:8100/api/userlistall/',
    method: 'get',
    params: query
  })
}

export function fetchdate(query) {
  return request({
    url: 'http://system-django.int.jumei.com/api/linechart/',
    // url: 'http://127.0.0.1:8100/api/linechart/',
    method: 'get',
    params: query
  })
}

export function fetchbread(query) {
  return request({
    url: 'http://system-django.int.jumei.com/api/breadchart/',
    // url: 'http://127.0.0.1:8100/api/breadchart/',
    method: 'get',
    params: query
  })
}
