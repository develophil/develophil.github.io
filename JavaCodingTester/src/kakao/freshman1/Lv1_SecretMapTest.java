package kakao.freshman1;

import org.junit.Assert;
import org.junit.Test;

import static org.junit.Assert.*;

public class Lv1_SecretMapTest {

    @Test
    public void solution() {
        Assert.assertArrayEquals(
                new String[]{"#####","# # #", "### #", "#  ##", "#####"},
                new Lv1_SecretMap().solution(5, new int[]{9, 20, 28, 18, 11}, new int[]{30, 1, 21, 17, 28}));
        Assert.assertArrayEquals(
                new String[]{"######","###  #","##  ##"," #### "," #####","### # "},
                new Lv1_SecretMap().solution(6, new int[]{46, 33, 33 ,22, 31, 50}, new int[]{27 ,56, 19, 14, 14, 10}));

    }

    @Test
    public void bit() {
        Assert.assertEquals(31, 22 | 27);
        Assert.assertEquals(18, 22 & 27);

        System.out.println(Integer.toBinaryString(18));
    }
}