package yanolja;

import org.junit.Assert;
import org.junit.Test;

/**
 * 2진법의 숫자가 홀수면 - 1, 짝수면 / 2. 총 몇번의 스텝까지 진행할 수 있는지 구하라
 */
public class Exam4 {
    public int solution(String s) {

        try {
            assertArgument(s);

            int num = Integer.parseInt(s, 2);

            int count = 0;
            while(num > 0) {
                if(isOdd(num)) {
                    num -= 1;
                } else {
                    num >>= 1;
                }
                count++;
            }

            return count;

        } catch (IllegalArgumentException e) {
            return 0;
        }
    }

    private void assertArgument(String s) {
        if (s == null || s.length() < 1 || s.length() > 1000000) {
            throw new IllegalArgumentException();
        }
    }

    private boolean isOdd(int num) {
        return num % 2 != 0;
    }

    @Test
    public void test() {
        Assert.assertEquals(7, solution("011100"));
        Assert.assertEquals(0, solution("0"));
        Assert.assertEquals(0, solution("0121100"));
    }
}
