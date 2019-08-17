package naver.exam;

import org.junit.Test;

import java.util.Collections;
import java.util.stream.Collectors;

public class No1 {

    public String solution(String T) {

        int size = T.length();

        if (size < 1 || size > 200000) {
            throw new IllegalArgumentException("out of range.");
        }

        return T.chars().boxed().sorted(Collections.reverseOrder()).map(integer -> (char) integer.intValue()).map(Object::toString).collect(Collectors.joining());
    }


    @Test
    public void test() {

        System.out.println(solution("MSSLS"));
        System.out.println(solution("LLMS"));
        System.out.println(solution("SMS"));
    }

}
