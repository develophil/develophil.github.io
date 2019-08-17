package codility.lesson1;

import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;
import java.util.function.Predicate;

public class BinaryGap {

    private static final String ONE = "1";

    public int solution(int N) {

        return Arrays.stream(removeRightZeroes(Integer.toBinaryString(N)).split(ONE))
                .filter(s-> !"".equals(s))
                .mapToInt(String::length)
                .max().orElse(0);
    }

    private String removeRightZeroes(String binaryString) {
        int indexLast1 = binaryString.lastIndexOf(ONE);

        if (indexLast1 < binaryString.length()) {
            return binaryString.substring(0, indexLast1);
        } else {
            return binaryString;
        }
    }


    @Test
    public void test() {
//        Assert.assertEquals(0, solution(32));
        Assert.assertEquals(4, solution(529));
    }
}
