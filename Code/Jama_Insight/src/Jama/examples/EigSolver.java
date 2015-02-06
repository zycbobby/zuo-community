package Jama.examples;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import Jama.EigenvalueDecomposition;
import Jama.Matrix;

public class EigSolver {

	public static Matrix getMatrix() throws IOException {
		return Matrix.read(new BufferedReader(new InputStreamReader(
				new FileInputStream(new File("test.matrix")))));

	}

	public static void AdditionalMethod(Matrix m) {

		double[][] d = m.getArray();

		// 列向量归一化
		for (int j = 0; j < d[0].length; j++) {
			double total = 0.0;
			for (int i = 0; i < d.length; i++) {
				total += d[i][j];
			}

			for (int i = 0; i < d.length; i++) {
				d[i][j] /= total;
			}
		}

		// 按行求和
		double[] linesum = new double[d.length];
		for (int i = 0; i < linesum.length; i++) {
			linesum[i] = 0.0;
		}

		for (int i = 0; i < d.length; i++) {
			double total = 0.0;
			for (int j = 0; j < d[0].length; j++) {
				total += d[i][j];
			}
			linesum[i] = total;
		}

		double total=0.0;
		//按列归一化
		for(int i=0;i<linesum.length;i++){
			total+=linesum[i];	
		}
		for(int i=0;i<linesum.length;i++){
			linesum[i]/=total;
			System.out.println(linesum[i]);
		}
		
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		Matrix m = getMatrix();

		AdditionalMethod(m);
		//EigenvalueDecomposition ed = m.eig();

		// 答案是对的，剩下的就是知道他怎么做到的
		//Matrix m1 = ed.getV();

		//m1.print(10, 6);

	}

}
