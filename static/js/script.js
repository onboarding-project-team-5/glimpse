const KEY_JWT = 'JWT'
const KEY_USER_ID = 'LOGIN_USER_ID'


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

// 로그인을 무조건 해야 하는 URL 기입.
const URL_MUST_LOGIN = ['/', '/profile/me', '/card/registration']

// 로그인 유저 정보를 담아내기
let LOGIN_USER_INFO = {}
    function is_user_logined(func_when_success) {
        let login_id = localStorage.getItem(KEY_USER_ID)

        fetch(`/api/users/${login_id}`)
        .then(a => a.json())
        .then(data => {
            let pathname = window.location.pathname

            // login 실패 시, 로그인 페이지로 리다이렉트.
            if(data.error_code && URL_MUST_LOGIN.includes(pathname)) {
                alert("비로그인 유저는 확인할 수 없습니다. 로그인 후 이용해주세요.")
                window.location.href = '/login'
                return ;
            }

            // login 성공 시, 로그인 유저 내용을 적재.
            LOGIN_USER_INFO = data.result
            func_when_success()
        })
    }