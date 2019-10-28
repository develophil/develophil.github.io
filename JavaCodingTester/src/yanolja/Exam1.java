package yanolja;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

/**
 * N개의 숫자를 더해서 0으로 만드는 숫자 배열 찾기
 *   - 0으로 초기화 된 배열의 중간값을 기준으로 맨앞, 맨뒤의 숫자들부터 반대의 숫자로 채우자.
 */
public class Exam1 {

    private static final int DIV_PAIR_NUM = 2;

    public int[] solution(int N) {

        if (N < 1 || N > 100) {
            return new int[0];
        }

        final int quotient = N / DIV_PAIR_NUM;
        final int remainder = N % DIV_PAIR_NUM;

        int[] result = new int[N];

        if (remainder == 1) {
            result[quotient] = 0;
        }

        for (int i = 1; i <= quotient; i++) {
            result[i - 1] = i * -1;
            result[N - i] = i;
        }

        return result;
    }


    @Test
    public void test() {
        Assert.assertArrayEquals(new int[]{0}, solution(1));
        Assert.assertArrayEquals(new int[]{-1,1}, solution(2));
        Assert.assertArrayEquals(new int[]{-1,0,1}, solution(3));
        Assert.assertArrayEquals(null, solution(0));
    }
}


