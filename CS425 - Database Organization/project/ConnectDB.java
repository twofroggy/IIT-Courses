package com.tiffanywong.com;
import java.sql.Connection; 
import java.sql.DriverManager; 

public class ConnectDB {
	public static Connection connect() { 
		
		Connection connection=null;
		
		try { 
			
			Class.forName("org.postgresql.Driver");
			connection = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres","tiffwong","password"); 
			
			if(connection != null) {
				System.out.println("Connection OK"); 
			} else { 
				System.out.println("Connection Failed"); 
			} 
			
			
		} catch (Exception e) { 
			System.out.println(e); 
		}
		
		return connection; 
	}
} 


	

