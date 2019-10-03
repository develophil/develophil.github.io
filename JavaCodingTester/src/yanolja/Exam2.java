package yanolja;

import org.junit.Assert;
import org.junit.Test;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

import static java.util.stream.Collectors.*;

public class Exam2 {
    public int solution(int[] ranks) {

        AtomicInteger result = new AtomicInteger(0);

        Arrays.stream(ranks)
                .sorted()
                .boxed()
                .collect(Collectors.groupingBy(v -> v, TreeMap::new, counting()))
                .entrySet().stream()
                .reduce( (e1, e2) -> {
                    if (canReport(e1, e2)) {
                        result.addAndGet(e1.getValue().intValue());
                    }
                    return e2;
                });

        return result.get();
    }

    private static boolean canReport(Map.Entry<Integer, Long> e1, Map.Entry<Integer, Long> e2) {
        return e2.getKey() - e1.getKey() == 1;
    }

    @Test
    public void test() {
        Assert.assertEquals(0, solution(new int[]{4,2,0}));
        Assert.assertEquals(3, solution(new int[]{0,3,1,4,3,4}));
        Assert.assertEquals(5, solution(new int[]{3,4,3,0,2,2,3,0,0}));
        Assert.assertEquals(0, solution(new int[]{1000000000,1000000000}));
    }
}
