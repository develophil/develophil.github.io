package yanolja;

import org.junit.Assert;
import org.junit.AssumptionViolatedException;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.Stopwatch;
import org.junit.runner.Description;

import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static java.util.stream.Collectors.*;

/**
 * 수의 차이가 1인 상사가 존재하는 경우에만 보고 가능. 보고 가능한 모든 병사의 숫자를 구하라.
 *   - 순서대로 정렬
 *     k : 기준 숫자
 *     v : 숫자의 갯수
 */
public class Exam2 {

    @Rule
    public MyJUnitStopWatch stopwatch = new MyJUnitStopWatch();

    public int solution(int[] ranks) {

        final AtomicInteger result = new AtomicInteger(0);
        int test = 0;

        Arrays.stream(ranks)
//                .parallel()
                .sorted()
                .boxed()
                .collect(Collectors.groupingBy(v -> v, TreeMap::new, counting()))
                .entrySet().stream()
//                .parallel()
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
    @Test
    public void test_max_performance() {

        int[] a = IntStream.rangeClosed(1, 10000).toArray();

        Assert.assertEquals(9999, solution(a));
    }
}

class MyJUnitStopWatch extends Stopwatch {

    private static void logInfo(Description description, String status, long nanos) {
        String testName = description.getMethodName();
        System.out.println(String.format("Test %s %s, spent %d microseconds",
                testName, status, TimeUnit.NANOSECONDS.toMicros(nanos)));
    }

    @Override
    protected void succeeded(long nanos, Description description) {
        logInfo(description, "succeeded", nanos);
    }

    @Override
    protected void failed(long nanos, Throwable e, Description description) {
        logInfo(description, "failed", nanos);
    }

    @Override
    protected void skipped(long nanos, AssumptionViolatedException e, Description description) {
        logInfo(description, "skipped", nanos);
    }

    @Override
    protected void finished(long nanos, Description description) {
        logInfo(description, "finished", nanos);
    }
}
