package hackerrank.warm_up_challenges.no03_jumping_on_the_clouds;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

import static hackerrank.warm_up_challenges.no03_jumping_on_the_clouds.Solution2.jumpingOnClouds;

public class SolutionTest {

    @Test
    public void test() {
        int result = jumpingOnClouds(new int[]{0, 0, 1, 0, 0, 1, 0});
        Assert.assertEquals(4, result);
    }

    @Test
    public void test2() {
        int result = jumpingOnClouds(new int[]{0, 0, 0, 0, 1, 0});
        Assert.assertEquals(3, result);
    }

    @Test
    public void test3() {
        int result = jumpingOnClouds(new int[]{0, 0});
        Assert.assertEquals(1, result);
    }

    @Test
    public void test4() {
        int result = jumpingOnClouds(new int[]{0, 1, 0});
        Assert.assertEquals(1, result);
    }

    @Test
    public void test5() {

        int n = 100;
        int[] ar = IntStream.range(1, 101).map(i -> 0).toArray();

        int result = jumpingOnClouds(ar);
        Assert.assertEquals(50, result);
    }
}