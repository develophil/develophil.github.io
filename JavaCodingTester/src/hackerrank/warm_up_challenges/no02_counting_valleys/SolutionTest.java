package hackerrank.warm_up_challenges.no02_counting_valleys;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

import static hackerrank.warm_up_challenges.no02_counting_valleys.Solution.countingValleys;

public class SolutionTest {

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
