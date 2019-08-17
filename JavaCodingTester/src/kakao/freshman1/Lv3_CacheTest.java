package kakao.freshman1;

import org.junit.Assert;
import org.junit.Test;

public class Lv3_CacheTest {

    @Test
    public void solution() {
        Assert.assertEquals(50, new Lv3_Cache().solution(3, new String[]{"Jeju", "Pangyo", "Seoul", "NewYork", "LA", "Jeju", "Pangyo", "Seoul", "NewYork", "LA"}));
        Assert.assertEquals(21, new Lv3_Cache().solution(3, new String[]{"Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul", "Jeju", "Pangyo", "Seoul"}));
        Assert.assertEquals(60, new Lv3_Cache().solution(2, new String[]{"Jeju", "Pangyo", "Seoul", "NewYork", "LA", "SanFrancisco", "Seoul", "Rome", "Paris", "Jeju", "NewYork", "Rome"}));
        Assert.assertEquals(52, new Lv3_Cache().solution(5, new String[]{"Jeju", "Pangyo", "Seoul", "NewYork", "LA", "SanFrancisco", "Seoul", "Rome", "Paris", "Jeju", "NewYork", "Rome"}));
        Assert.assertEquals(16, new Lv3_Cache().solution(2, new String[]{"Jeju", "Pangyo", "NewYork", "newyork"}));
        Assert.assertEquals(25, new Lv3_Cache().solution(0, new String[]{"Jeju", "Pangyo", "Seoul", "NewYork", "LA"}));
    }
}


