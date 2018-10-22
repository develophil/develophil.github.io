package net.develophil.java9.exam;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.IntStream;
import java.util.stream.Stream;

/**
 * 과제3) 자바 람다식과 스트림
 *
 * 1.	객체지향 언어에서 인터페이스는 그 시그너처와 선언이 변하지 않는다는 전제로 하여 다형성을 정의하는 객체간의 규약입니다. 자바8의 인터페이스는 인터페이스를 업그레이드하는 개념을 도입하였습니다.  새롭게 변경된 인터페이스에 대한 내용을 각각 기술하세요. (30점)
 * A.	인터페이스에서 구현 메서드를 작성할 수 있는 방법을 기술하세요.
 *      : default method 구현
 *      : static method 구현
 * B.	자바9 에서 새롭게 추가된 구현 메서드를 작성할 수 있는 방법을 기술하세요.
 *      : private method / static method 구현
 * C.	함수형 인터페이스에 대해서 설명하세요.
 *      : 추상 메서드가 한 개만 포함된 인터페이스
 *      : @FunctionalInterface 어노테이션을 붙여 함수형 인터페이스임을 명시한다.
 *      : 자주사용되는 함수형 인터페이스는 Runnable, Supplier, Consumer, Function, Predicate 등이 있다.
 *
 *
 * 2.	문제로 제공되는 stream-data.txt 파일에 대해서 다음을 각각 수행하세요. (예외는 별도로 처리하지 않습니다.) (50점)
 * A.	stream-data.txt 파일은 하나의 숫자를 행으로 가지고 있는 텍스트 파일입니다. 각 행을 읽어서 Stream<String> 타입으로 작성하세요.
 * B.	A를 IntStream 타입으로 변환하는 코드를 작성하세요.
 * C.	B 에서 작성된 코드에서 map 중간연산을 사용해서 각 요소를 2배로 해서 새롭게 스트림을 생성합니다.
 * D.	C에서 생성된 스트림에서 50미만의 숫자는 제외하고 새롭게 스트림을 생성합니다.
 * E.	최종적으로 모든 요소의 합을 구해서 출력합니다. (System.out.println)
 *
 *
 * 3.	2번 문제를 스트림을 사용하지 않고 for 문을 사용해서 결과를 도출하는 방식을 Imperative Programming(명령형 프로그래밍, 스트림을 사용하여 처리하는 방식을 선언형이라고 함) 이라고 한다. 다음을 각각 수행할 수 있도록 코드를 작성합니다. (예외는 별도로 처리하지 않습니다.) (20점)
 * A.	stream-data.txt 파일을 읽어 List<Integer> 혹은 ArrayList<Integer> 타입으로 데이터를 읽어옵니다.
 * B.	for 문을 사용하여 요소 중 50을 초과하는 요소의 총 합을 구해서 출력합니다. (각 요소를 2배로 곱하지 않습니다.)
 */
public class Solution {

	final String examFileName = "stream-data.txt";
	final String examFilePath = "/Users/hkpking/study/hkp/develophil.github.io/study/tmon/elearning/java9/exam/";

	public Stream<String> twoA() throws IOException {
		return Files.lines(Paths.get(examFilePath + examFileName));
	}

	public IntStream twoB() throws IOException {
		return twoA().mapToInt(Integer::parseInt);
	}

	public IntStream twoC() throws IOException {
		return twoB().map(i -> i * 2);
	}

	public IntStream twoD() throws IOException {
		return twoC().filter(i -> i >= 50);
	}

	public int twoE() throws IOException {
		int sum = twoD().sum();
		System.out.println(sum);
		return sum;
	}

	public List<Integer> threeA() {

		List<Integer> list = new ArrayList<>();

		try (Scanner scanner = new Scanner(new File(examFilePath + examFileName))) {
			while (scanner.hasNext()){
				list.add(Integer.parseInt(scanner.nextLine()));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		return list;
	}

	public int threeB() {

		int sum = 0;

		for (int i : threeA()) {
			if (i > 50) {
				sum += i;
			}
		}

		System.out.println(sum);
		return sum;
	}

}
