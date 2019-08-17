package codesignal.tournament.day1;

import org.junit.Assert;
import org.junit.Test;

public class Lv02_SumOfCubesTest {

    @Test
    public void sumOfCubes() {
        Assert.assertEquals(36, new Lv02_SumOfCubes().sumOfCubes(3));
        Assert.assertEquals(1, new Lv02_SumOfCubes().sumOfCubes(1));
        Assert.assertEquals(1, new Lv02_SumOfCubes().sumOfCubes(10));
    }
}