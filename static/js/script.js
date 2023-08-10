KEY_JWT = 'JWT'

function add_prefix(token) {
    return `Bearer ${token}`
}

// fetch 대용으로 사용 가능한 jwt 동봉 호출
function auth(url, options={}) {
    let token = localStorage.getItem(KEY_JWT)

    let new_options = {
        ...options,
        headers: {}
    }
    new_options.headers = {
        ...options.headers,
        Authorization: add_prefix(token),
    }
    return fetch(url, new_options)
}