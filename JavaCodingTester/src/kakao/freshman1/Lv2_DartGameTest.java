package kakao.freshman1;

import org.junit.Assert;
import org.junit.Test;

import static org.junit.Assert.*;

public class Lv2_DartGameTest {

    @Test
    public void solution() {

        Assert.assertEquals(37, new Lv2_DartGame().solution("1S2D*3T"));
        Assert.assertEquals(9, new Lv2_DartGame().solution("1D2S#10S"));
        Assert.assertEquals(3, new Lv2_DartGame().solution("1D2S0T"));
        Assert.assertEquals(23, new Lv2_DartGame().solution("1S*2T*3S"));
        Assert.assertEquals(5, new Lv2_DartGame().solution("1D#2S*3S"));
        Assert.assertEquals(-4, new Lv2_DartGame().solution("1T2D3D#"));
        Assert.assertEquals(59, new Lv2_DartGame().solution("1D2S3T*"));

    }
}