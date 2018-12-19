### MainServlet.java
```
// TODO Auto-generated constructor stub
```
> 필요없는 주석은 제거해주는게 좋습니다.
> 해당내용처럼 자동생성 되는 경우 추가적으로 할 작업이 없다면 아예 삭제를 하여 혼란을 방지하는 것이죠


### TodoFormServlet.java
```
RequestDispatcher rdp=request.getRequestDispatcher("/todoForm.jsp");
```
> 코딩규칙은 프로젝트마다 정의하는 내용이 조금씩 차이가 있을수는 있으나
> 가급적 한 프로젝트 내에서는 통일시켜주는 것이 좋습니다.
> 대부분 '='에 대한 코딩 스타일은 a = b 이런식으로 빈칸을 두어 가독성을 높이는 방향으로 많이 쓰이고 있습니다.

### TodoDao.java
```
private static String dburl = "jdbc:mysql://localhost:3306/connectdb?useUnicode=true&characterEncoding=utf8";
```
> 보통 정해져있는 값을 상수로 사용하려는 경우에는 값을 수정할 수 없도록 final 이라는 제어자와 함께 쓰는 것이 일반적입니다.
> 또한 자바에서 변수의 네이밍은 가독성을 위하여 연결되는 각 단어의 첫글자를 대문자로 표시하는 카멜케이스 표기법을 사용합니다.
private static final String dbUrl 이렇게 사용하면 좋겠네요
한 가지 더 부가적인 설명을 드린다면 현업에서는 대개 local/dev/qa/real 의 환경이 나눠지고 이 환경들에 맞춰 세팅값들도 변하게 됩니다.
> 그래서 보통 이런 값들은 환경별 세팅 파일에 따로 저장하고 그 값을 로드하여 사용하는 형태로 개발됩니다. 참고해주세요.

### TodoDao.java
```
public List<TodoDto> getTodos() {
  List<TodoDto> list = new ArrayList<>();

try {
    Class.forName("com.mysql.jdbc.Driver");
} catch (ClassNotFoundException e) {
    e.printStackTrace();
}

String sql = "SELECT * FROM todo order by regdate asc";
try (Connection conn = DriverManager.getConnection(dburl, dbUser, dbpasswd);
PreparedStatement ps = conn.prepareStatement(sql)) {

try (ResultSet rs = ps.executeQuery()) {

while (rs.next()) {
    long id = rs.getLong("id");
    String title = rs.getString("title");
    String name = rs.getString("name");
    int sequence = rs.getInt("sequence");
    String type = rs.getString("type");
    String regdate = rs.getString("regdate");
    TodoDto todo = new TodoDto(id, name, regdate, sequence, title, type);
    list.add(todo);
}
} catch (Exception e) {
e.printStackTrace();
}
} catch (Exception ex) {
ex.printStackTrace();
}
return list;
}
```
> getTodos, addTodo, updateTodo 메서드의 내용을 보면 공통적으로 수행되는 로직들이 보이네요.
> 드라이버를 로드하고 connection을 가져오는 부분은 따로 메서드를 정의하여 사용하는 것이 유지보수 차원에서 훨씬 유리합니다.
또한, 객체지향개발 원리 중 단일책임의 원칙에 입각하여 '하나의 객체는 하나의 책임만을 가진다'라는 의미를 되새길 필요가 있는데
TodoDao에서는 데이터베이스 연결에 대한 부분은 책임지지 않고 할일에 대해 조회/등록/수정 이라는 각각의 기능에 대한 책임만 지도록 설계하는 것이 좋습니다.
> 따라서 데이터베이스를 연동하고 커넥션을 맺는 기능 등은 독립적인 객체를 통해 수행하는 것이 좋습니다.

### TodoDao.java
```
 try (Connection conn = DriverManager.getConnection(dburl, dbUser, dbpasswd);
```
> 향상된 예외처리문을 사용하여 connection 객체의 종료를 관리하는 것은 좋은 시도입니다.
> 다른 소스를 보니 일반적인 예외처리문 인 경우 어떻게 close 하는지도 알고 계신 것 같네요!

### TodoDao.java
```
String title=new String(dto.getTitle().getBytes("8859_1"),"UTF-8");
```
> 보통 문자열은 상수로 등록하여 사용하는 것이 일반적입니다.
> 반복되는 8859_1, UTF-8 등 의 문자열은
> private static final String BYTE_ENCODING_CHARACTERSET_NAME = "8859_1";
> private static final String STRING_DECODING_CHARACTERSET_NAME = "UTF-8";
> 이런식으로 사용하면 문자열값에 대한 의미를 변수명을 통해 명확히 전달할 수 있고 유지보수가 용이해 집니다.

### main.jsp
```
List<TodoDto> dto = new ArrayList<>();
if (request.getAttribute("dto") != null)
       dto = (List<TodoDto>) request.getAttribute("dto");
```
> 49행에서 ${requestScope.dto} requestScope에 등록된 dto를 그대로 사용하였으므로
자원의 낭비를 막기 위해 사용되지 않는 변수는 삭제하는 것이 좋습니다.
> 14-15행에서의 할당 또한 필요없습니다.

### main.jsp
```
if('${row.type}'=='TODO'){
p.appendChild(a);
todo.appendChild(p);
}
else if('${row.type}'=='DOING'){
p.appendChild(a);
doing.appendChild(p);
}
else{
  done.appendChild(p);
}
```
> 'DONE'의 경우에만 해당되는 로직이므로 위의 조건 분기와 마찬가지로 else if를 통해 'DONE'을 명시해주는 것이 가독성을 높이고 유지보수 측면에서 많이 도움이 됩니다.
> switch로 조건들을 분기하여 가독성을 더욱 높일 수도 있습니다.

### main.jsp
```
var a = document.createElement("span");
```
> 어떤 프로그래밍 언어에서건 변수명은 의미가 있는 이름으로 선언하는 것이 중요합니다.
> 이와 같은 경우 'span' 이라고 명시해주는 것이 훨씬 더 이해하기 쉽겠죠?

### TodoFormServlet.java
```
if (ret == 1)
  response.sendRedirect("main.jsp");
```
> 해당 조건에 수행하는 명령어가 한 줄이면 이렇게 중괄호를 생략하여 표시할 수는 있지만 보통 서비스가 커지면서 두 줄 이상의 로직이 들어가는 경우가 대부분입니다.
> 유지보수를 용이하게 하고 명확한 범위 가독성을 위해 한 줄 이라도 현업에서는 보통 중괄호를 사용하는 것을 장려하는 곳이 더 많으니 참고하시기 바랍니다.

### TodoTypeServlet.java
```
List<TodoDto> dto = dao.getTodos();
for (int i = 0; i < dto.size(); i++)
    if (dto.get(i).getId() == id)
        dao.updateTodo(dto.get(i));
```
> 데이터베이스에 접근하여 Todo 데이터를 조회하는 것이 TodoDao의 역할 이므로 id 값을 통해 하나의 Todo 객체를 가져오는 서비스 로직도 dao 내부에서 처리하면 좋습니다.
> public TodoDto getTodo(long id) { ... }
> 이런식으로 말이죠.
> 그러면 서블릿에서는 TodoDto todoDtoById = dao.getTodo(id) 이런 식으로 책임을 분리시키고 좀 더 가독성 높은 코드를 작성할 수 있습니다.  

###
```
```
>

###
```
```
>
