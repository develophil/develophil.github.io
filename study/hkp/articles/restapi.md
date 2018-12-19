# rest api

애코록

###### 골치 아픈 부분을 해소해보자.

1. 단어
> 1. 단수-복수 같은 형태의 단어
> 1. 콩글리쉬

1. 구조
  1. crud 이외의 action
    1. Store
    > 복수명사
    1. Controller
    > 동사, 동사구













https://en.wikipedia.org/wiki/Uniform_Resource_Identifier

3.1 URI 식별자 설계
URI : Uniform Resourc Identifier(식별)
URL : Uniform Resourc Locator(위치)

#### URI 기본 원칙
1. 마지막 문자로 ‘/’ 를 포함하지 않는다.
1. 가독성을 높이는 데에는 ‘-’를 사용한다.
1. 소문자만 사용
1. URI 에는 확장자를 넣지 않는다.


3.1.2 리소스 형식 (Resource Type)
도큐먼트 ( Document )
컬렉션 ( Collection )
스토어 ( Store )
컨트롤러 ( Controller )
3.1.2.1 도큐먼트 ( Document )
가장 기본이 되는 리소스 형식
데이터 베이스의 레코드와 같은 것
ex) http://api.your-service-books.com/books/1
3.1.2.2 컬렉션 ( Collection )
도큐먼트의 디렉터리 리소스
도큐먼트의 리스트
ex) http://api.your-service-books.com/books
3.1.2.3 스토어 ( Store )
클라이언트가 특별히 관리하는 형태를 갖는 것
favorites, mark, done
ex) http://api.your-service-books.com/users/1/favorites
3.1.2.4 컨트롤러 ( Controller )
CRUD 이외의 것
ex) http://api.your-service-books.com/books/1/buy
3.1.3 명명 규칙 (Conventional Naming Rules)
CRUD 는 URI 에 표시 X
도규먼트 : 단수
컬렉션 : 복수
스토어 : 복수
컨트롤러 : 동사/동사구
Query : 선택 사항
페이지네이션
타입
소팅
3.1.4 HTTP 프로토콜 이용
요청 메서드
응답 상태 코드
3.1.4.1 요청 메서드
GET : 리소스 상태
HEAD : 리소스의 메타 데이터
PUT : ‘스토어 리소스’ 및 ‘리스소’ 갱신
POST : 컬렉션에 리소스 추가 / 스토어에 리소스 추가 / 제한 없는 사용
가지고 오는 것(get) x
저장하는 것(put:store) x
지우는 것 (delete) x
DELETE : 리소스 제거
3.1.4.2 응답 상태 코드
2xx : 정상 처리 (성공)
3xx : 실패하지 않은 요청 중 비정상 처리 (변경 및 이동)
4xx : 비정상 처리 (실패)
5xx : 서버 에러
