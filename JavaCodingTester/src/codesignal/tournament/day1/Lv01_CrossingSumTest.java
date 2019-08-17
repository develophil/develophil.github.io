package codesignal.tournament.day1;

import org.junit.Assert;
import org.junit.Test;

public class Lv01_CrossingSumTest {

    @Test
    public void crossingSum() {

        Assert.assertEquals(12, new Lv01_CrossingSum().crossingSum(new int[][]{{1,1,1,1},{2,2,2,2},{3,3,3,3}},1, 3));
        Assert.assertEquals(3, new Lv01_CrossingSum().crossingSum(new int[][]{{1,1},{1,1}},0, 0));
    }
}