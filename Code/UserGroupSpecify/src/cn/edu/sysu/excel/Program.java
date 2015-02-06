package cn.edu.sysu.excel;

import java.io.IOException;

public class Program {

	/**
	 * @param args
	 * @throws IOException 
	 * @throws BiffException 
	 */
	public static void main(String[] args){
		ReadExcel re=new ReadExcel("E:\\Graduation\\词汇分析结果\\词汇连接SQLSERVER.xlsx");
		//ReadExcel re=new ReadExcel("E:\\Graduation\\词汇分析结果\\test.xlsx");
		re.read();
	}
}
