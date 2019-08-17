package playground;

import org.junit.Test;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;


public class Playground implements A, B{

    int fibonacciIndex(int n) {

        return String.valueOf(fiboNum(n)).length();
    }

    int fiboNum(int n) {

        if (n == 1) {
            return 0;
        }

        if (n == 2) {
            return 1;
        }

        return fiboNum(n - 1) + fiboNum(n - 2);
    }



    int largestNumber(int n) {
        return Integer.parseInt(IntStream.range(0, n).mapToObj(i -> "9").collect(Collectors.joining()));
    }

    int arrayMinimumIndex(int[] inputArray) {

        int min = 100;
        int minIndex = 0;

        for (int i = 0; i < inputArray.length; i++) {
            if (inputArray[i] < min) {
                min = inputArray[i];
                minIndex = i;
            }
        }

        return minIndex;

    }

    int extraNumber(int a, int b, int c) {

        return (double)a/b == 1.0 ? c : ((double)a/c == 1.0 ? b : a);
    }

//    int[] maxSumSegments(int[] inputArray) {
//
//    }

    @Test
    public void ttt() {
        System.out.println(fiboNum(10));
    }


    public int factorial(int n) {

        if (n <= 1) {
            return n;
        }

        return n * factorial(n - 1);
    }

    @Test
    public void t() {
        System.out.println(factorial(0));

    }







    public void quickSortSample(int[] arr, int left, int right) {
        int i, j, pivot, tmp;
        if (left < right) {
            i = left;   j = right;
            pivot = arr[(left+right)/2];
            //분할 과정
            while (i < j) {
                while (arr[j] > pivot) j--;
                // 이 부분에서 arr[j-1]에 접근해서 익셉션 발생가능함.
                while (i < j && arr[i] <= pivot) i++;

                tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }
            //정렬 과정
            quickSort(arr, left, i - 1);
            quickSort(arr, i + 1, right);
        }
    }

    public void quickSort(int[] arr, int left, int right) {
        int i, j, pivot, tmp;
        if (left < right) {
            i = left;
            j = right;
            pivot = arr[(left + right) / 2];

            while (i < j) {
                while(arr[j] > pivot) j--;
                while (i < j && arr[i] < pivot) i++;

                tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
                printArr(arr);
            }

            quickSort(arr, left, j - 1);
            quickSort(arr, i + 1, right);
        }


    }

    public void sort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }


    public void printArr(int[] arr) {
        System.out.println(Arrays.stream(arr).mapToObj(String::valueOf).collect(Collectors.joining(", ")));
    }

    @Test
    public void test() {
        List<Integer> test = Arrays.asList(4, 2, 6, 5, 34, 3, 26, 1);

        int[] arr = new int[]{5,-2,7,6,3,9,-11,35,38,1};
//        int[] arr = new int[]{3,2,7,6,5,4,9,8,1};
        sort(arr);

        System.out.println("--------------");
        printArr(arr);
    }

    @Override
    public void print() {
        B.super.print();
    }
}


interface A {
    default void print() {
        System.out.println("A!!!");
    }
}
interface B {
    default void print() {
        System.out.println("B!!!");
    }
}