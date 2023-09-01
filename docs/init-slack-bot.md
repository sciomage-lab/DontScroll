# Create slack bot api

[slack apps](https://api.slack.com/apps)

1. url에서 앱을 만들고
2. 좌측 OAuth & Permission에 들어가서
3. Scopes 추가
 - `app_mentions:read`
 - `channels:history`
 - `channels:read`
 - `groups:read`
 - `mpim:read`
 - `im:read`
 - `files:read`

# API Test

[slack app test](https://api.slack.com/methods/conversations.list/test)

1. url들아가면 tester 페이지가 나옴
2. 위의 `auth_token`을 집어 넣고 "Test method" 녹색 버튼
