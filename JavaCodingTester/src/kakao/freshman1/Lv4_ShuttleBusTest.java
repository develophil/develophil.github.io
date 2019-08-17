package kakao.freshman1;

import org.junit.Assert;
import org.junit.Test;

import static org.junit.Assert.*;

public class Lv4_ShuttleBusTest {

    @Test
    public void solution() {
        Assert.assertEquals("09:00", new Lv4_ShuttleBus().solution(1, 1, 5, new String[]{"08:00", "08:01", "08:02", "08:03"}));
        Assert.assertEquals("09:09",new Lv4_ShuttleBus().solution(2,10,2, new String[]{"09:10", "09:09", "08:00"}));
        Assert.assertEquals("08:59",new Lv4_ShuttleBus().solution(2,1,2, new String[]{"09:00", "09:00", "09:00", "09:00"}));
        Assert.assertEquals("00:00",new Lv4_ShuttleBus().solution(1,1,5, new String[]{"00:01", "00:01", "00:01", "00:01", "00:01"}));
        Assert.assertEquals("09:00",new Lv4_ShuttleBus().solution(1,1,1, new String[]{"23:59"}));
        Assert.assertEquals("18:00",new Lv4_ShuttleBus().solution(10,60,45, new String[]{"23:59","23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59", "23:59"}));
    }
}