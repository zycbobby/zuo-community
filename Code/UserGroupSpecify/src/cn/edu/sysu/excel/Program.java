package cn.edu.sysu.excel;

import java.io.IOException;

public class Program {

	/**
	 * @param args
	 * @throws IOException 
	 * @throws BiffException 
	 */
	public static void main(String[] args){
		ReadExcel re=new ReadExcel("E:\\Graduation\\�ʻ�������\\�ʻ�����SQLSERVER.xlsx");
		//ReadExcel re=new ReadExcel("E:\\Graduation\\�ʻ�������\\test.xlsx");
		re.read();
	}
}
