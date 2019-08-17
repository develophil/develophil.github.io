package codility.lesson6sorting;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

import static org.junit.Assert.*;

public class MaxProductOfThreeTest {

    MaxProductOfThree maxProductOfThree = new MaxProductOfThree();

    @Test
    public void test() {

        int[] arr = new int[]{-3, 1, 2, -2, 5, 6};

        int result = maxProductOfThree.solution(arr);
        Assert.assertEquals(60, result);

    }

    @Test
    public void test2() {

        int[] arr = new int[]{1, -4, 3, -2, 2, 5};

        int result = maxProductOfThree.solution(arr);
        Assert.assertEquals(40, result);

    }

    @Test
    public void test3() {

        int[] arr = new int[]{-3, -2, 6};

        int result = maxProductOfThree.solution(arr);
        Assert.assertEquals(36, result);

    }

    @Test()
    public void test4() {

        int[] arr = new int[]{-100000, -2, 6};

        int result = maxProductOfThree.solution(arr);
        Assert.assertEquals(0, result);

    }
}
