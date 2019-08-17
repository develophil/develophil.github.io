package codesignal.tournament.day2;

import org.junit.Test;

public class GrowingPlant {

    int growingPlant(int upSpeed, int downSpeed, int desiredHeight) {

        if (upSpeed >= desiredHeight) {
            return 1;
        }

        return (int)Math.ceil((desiredHeight - downSpeed) / (double)(upSpeed - downSpeed));
    }


    @Test
    public void a() {
        System.out.println(growingPlant(100, 10, 910));
        System.out.println(growingPlant(10, 9, 4));
        System.out.println(growingPlant(5, 2, 7));
    }

}
