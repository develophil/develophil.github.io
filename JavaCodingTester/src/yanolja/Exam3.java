package yanolja;

import org.junit.Assert;
import org.junit.Test;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static java.util.stream.Collectors.counting;

/**
 * S, T 는 HH:MM:SS 규칙을 따른다.
 * S 는 같은날 T 이전의 시간
 */
public class Exam3 {
    public int solution(String S, String T) {

        int startSeconds = convertSeconds(S);
        int endSeconds = convertSeconds(S);

/*
        IntStream.rangeClosed(startSeconds, endSeconds)
                .mapToObj(t->new HashSet(convertTimeString(t)))


*/

        return 0;
    }



    private static int convertSeconds(String s) {
        int[] convertRate = new int[]{60 * 60, 60, 1};
        String[] timeTokens = s.split(":");

        if (timeTokens.length != 3) {
            throw new IllegalArgumentException();
        }

        int result = 0;
        for (int i = 0; i < timeTokens.length; i++) {
            result += Integer.parseInt(timeTokens[i]) * convertRate[i];
        }

        return result;
    }

    private static String convertTimeString(int seconds) {
        LocalTime lt = LocalTime.ofSecondOfDay(seconds);
        return lt.format(DateTimeFormatter.ofPattern("HHmmSS"));
    }

    @Test
    public void convertTest() {
//        Assert.assertEquals(1, convertSeconds("00:00:01"));
//        Assert.assertEquals(3661, convertSeconds("01:01:01"));

        LocalTime lt = LocalTime.ofSecondOfDay(101);
        System.out.println(lt.format(DateTimeFormatter.ofPattern("HHmmSS")));


    }

    @Test
    public void test() {
        Assert.assertTrue(solution("00:00:00", "23:59:59") > 0);
    }
}
