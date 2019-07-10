package hackerrank.warm_up_challenges.no02_counting_valleys;

import org.junit.Assert;
import org.junit.Test;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.stream.IntStream;

public class Solution {

    static class Hike {

        private int step;
        private char[] paths;
        private int groundLevel = 0;
        private int valleyCount = 0;


        public Hike(int n, String s) {
            this.step = n;
            this.paths = s.toCharArray();
        }

        public void travel() {

            for (int i = 0; i < step; i++) {

                switch (paths[i]) {
                    case 'U':
                        groundLevel++;
                        break;
                    case 'D':
                        checkZeroLevel(() -> valleyCount++);
                        groundLevel--;
                        break;
                    default:
                        throw new IllegalArgumentException("path 문자열은 'U' 나 'D'만 입력 가능합니다.");
                }
            }
        }

        private void checkZeroLevel(Runnable runnable) {
            if (groundLevel == 0) {
                runnable.run();
            }
        }

        public int getValleyCount() {
            return this.valleyCount;
        }

    }

    private static void assertNumberRange(int n) {
        if (n < 2 || n > Math.pow(10, 6)) {
            throw new IllegalArgumentException("n 값은 2 이상 10^6 이하만 가능합니다.");
        }
    }

    // Complete the countingValleys function below.
    static int countingValleys(int n, String s) {
        assertNumberRange(n);

        Hike hike = new Hike(n, s);
        hike.travel();

        return hike.getValleyCount();
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int n = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        String s = scanner.nextLine();

        int result = countingValleys(n, s);

        bufferedWriter.write(String.valueOf(result));
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }


    @Test
    public void test() {
        int result = countingValleys(10, "DUDUDUDUUD");
        Assert.assertEquals(4, result);
    }
    @Test
    public void test1() {
        int result = countingValleys(8, "UDDDUDUU");
        Assert.assertEquals(1, result);
    }
    @Test
    public void test2() {
        int result = countingValleys(2, "UU");
        Assert.assertEquals(0, result);
    }
    @Test
    public void test3() {
        int result = countingValleys(2, "DD");
        Assert.assertEquals(1, result);
    }
    @Test
    public void test4() {

        int n = (int) Math.pow(10, 6);
        StringBuilder sb = new StringBuilder(n);
        IntStream.range(0, n).forEach(i->sb.append("U"));

        int result = countingValleys(n, sb.toString());
        Assert.assertEquals(0, result);
    }
    @Test
    public void test5() {

        int n = (int) Math.pow(10, 6);
        StringBuilder sb = new StringBuilder(n);
        IntStream.range(0, n).forEach(i->sb.append("D"));

        int result = countingValleys(2, sb.toString());
        Assert.assertEquals(1, result);
    }
}
