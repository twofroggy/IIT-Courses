package com.tiffanywong.com;

import java.util.ArrayList;
import java.util.Scanner;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Application_entrypoint {
  public static void main(String[] args) {

    Connection conn = ConnectDB.connect();

    Scanner scan = new Scanner(System.in);
    System.out.println("\nPlease enter your username (STRING with no spaces):");
    String username = scan.nextLine();
    System.out.println("\nPlease enter your password (STRING with no spaces)");
    String password = scan.nextLine();
    int selection = 0;
    try {
      Statement stmt = conn.createStatement();

      try {

        ResultSet rs = stmt.executeQuery("Select * " + "From Employee " + "Where username= '" + username + "'");

        while (rs.next()) {
          String actualPassword = rs.getString("user_password");

          if (actualPassword.equals(password)) {
            String jobtitle = rs.getString("jobTitle");
            String SSN = rs.getString("SSN");

            switch (jobtitle) {

            case "employee": // employee role
              int employee_selection = 0;
              ArrayList<String> depArray = new ArrayList<String>();
              // start of do
              while (employee_selection != 6) {
                System.out.println("\nEmployee Menu: \nSelect what you want to do (INT):");
                System.out.println(
                    "1. Update your address \n2. Update your dependent's information \n3. Add a dependent \n4. View your biweekly paycheck \n5. Update your 401k match percent\n6. Leave the program");
                employee_selection = scan.nextInt();
                scan.nextLine();

                // sanity check for employee_selection
                while (employee_selection < 1 || employee_selection > 6) {
                  System.out.println("\nERROR: Please enter a valid number.");
                  employee_selection = scan.nextInt();
                  scan.nextLine();
                }
                switch (employee_selection) {
                case 1: // update your address
                  System.out.println("\nEnter your updated address (STRING): ");
                  String up_address = scan.nextLine();

                  // System.out.println("scanned address");
                  try {
                    stmt.executeUpdate(
                        "update employee " + "set address = '" + up_address + "' where SSN = '" + SSN + "'");
                  } catch (SQLException sqle) {
                    System.out.println("\nCould not update your address." + sqle);
                  }
                  break; // for case 1 in employee selection

                case 2: // update dependent's name and relationship
                  System.out.println("\nEnter the SSN of the dependent you want to update (STRING): ");
                  String input_depSSN = scan.nextLine();
                  depArray = new ArrayList<String>();
                  rs = stmt.executeQuery("Select dependent_SSN from dependents where SSN = '" + SSN + "'");
                  while (rs.next()) {
                    depArray.add(rs.getString(1));
                  }
                  boolean inDep = depArray.contains(input_depSSN);
                  while (inDep != true) {
                    System.out.println("\nEnter a valid SSN");
                    input_depSSN = scan.nextLine();
                    inDep = depArray.contains(input_depSSN);
                  }

                  System.out.println(
                      "\nUpdating dependent info Menu: \nSelect what information you want to update for your dependent (INT): ");
                  System.out.println("1. Dependent's full name \n2. Dependent's relationship to you");
                  int dep_selection = scan.nextInt();
                  scan.nextLine();

                  // sanity check for updating dependent selection
                  while (dep_selection < 1 || dep_selection > 2) {
                    System.out.println("\nERROR: Please enter a valid number.");
                    dep_selection = scan.nextInt();
                    scan.nextLine();
                  }
                  switch (dep_selection) {
                  case 1: // dependent's name
                    System.out.println("\nEnter your dependent's updated name (STRING): ");
                    String up_depname = scan.nextLine();
                    try {
                      stmt.executeUpdate("update dependents " + "set full_name = '" + up_depname + "' where SSN = '"
                          + SSN + "' and dependent_SSN = '" + input_depSSN + "'");
                    } catch (SQLException sqle) {
                      System.out.println("\nCould not update dependent's name." + sqle);
                    }
                    break; // for case 1 in dependent selection

                  case 2: // dependent's relationship
                    System.out.println("\nEnter your dependent's updated relationship to you (STRING): ");
                    String up_deprel = scan.nextLine();
                    try {
                      stmt.executeUpdate("update dependents " + "set relationship = '" + up_deprel + "' where SSN = '"
                          + SSN + "' and dependent_SSN = '" + input_depSSN + "'");
                    } catch (SQLException sqle) {
                      System.out.println("\nCould not update dependent's relationship." + sqle);
                    }
                    break; // for case 2 in dependent selection
                  }
                  break; // for case 2 in emeployee selection

                case 3: // add a dependent
                  System.out.println("\nEnter your dependent's full name (STRING): ");
                  String new_dependentname = scan.nextLine();
                  System.out.println("\nEnter your dependent's SSN (STRING): ");
                  String new_dependentSSN = scan.nextLine();

                  depArray = new ArrayList<String>();
                  rs = stmt.executeQuery("Select dependent_SSN from dependents where SSN = '" + SSN + "'");
                  while (rs.next()) {
                    depArray.add(rs.getString(1));
                  }
                  inDep = depArray.contains(new_dependentSSN);
                  while (inDep == true) {
                    System.out.println("\nEnter a valid SSN (STRING)");
                    new_dependentSSN = scan.nextLine();
                    inDep = depArray.contains(new_dependentSSN);
                  }

                  System.out.println("\nEnter your dependent's relationship to you (STRING): ");
                  String new_dependentrel = scan.nextLine();

                  try {
                    stmt.executeUpdate("insert into dependents (full_name, dependent_SSN, relationship, SSN) values ('"
                        + new_dependentname + "', '" + new_dependentSSN + "', '" + new_dependentrel + "', '" + SSN
                        + "')");
                  } catch (SQLException sqle) {
                    System.out.println("\nCould not insert dependent." + sqle);
                  }
                  break; // for case 3 in employee selection

                case 4: // view your paycheck

                  try {
                    rs = stmt.executeQuery("Select * from biweekly_paycheck where SSN = '" + SSN + "'");
                    System.out.println(
                        "\nUsername | SSN | BiWeekly Salary | Bonus | Medicare Amount | State Tax Amount | Federal Tax Amount | Social Security Amount | 401k Amount | Insurance Amount");
                    while (rs.next()) {
                      System.out.println(
                          rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | " + rs.getString(4)
                              + " | " + rs.getString(5) + " | " + rs.getString(6) + " | " + rs.getString(7) + " | "
                              + rs.getString(8) + " | " + rs.getString(9) + " | " + rs.getString(10));
                    }
                  } catch (SQLException sqle) {
                    System.out.println("\nCould not view biweekly paycheck." + sqle);
                  }

                  break; // for case 4 in employee selection

                case 5: // Update your 401k match percent
                  System.out.println("\nEnter your updated 401k match percent (FLOAT): ");
                  Double updated_401kper = scan.nextDouble();
                  try {
                    stmt.executeUpdate("update Benefit_401k " + "set employeeContribution_ben = '" + updated_401kper
                        + "' where SSN = '" + SSN + "'");
                  } catch (SQLException sqle) {
                    System.out.println("\nCould not update your 401k match percent." + sqle);
                  }
                  break; // for case 5 in employee selection
                case 6:
                  System.out.println("\nExited");
                  return;
                } // end of switch case for employee selection

              }

            case "manager":
              int selection2 =0;
              int selection3 = 0;
              selection = 0;

              String inputUser;
              while (selection != 4) {
                System.out.println("\nManager Menu: \nSelect what you want to do (INT):");
                System.out.println( // Update employee benefits, contribution, tax and bonus
                    "1. Update employee information \n2. View employee information \n3. View reports \n4. Exit the program");
                selection = scan.nextInt();

                while (selection < 1 || selection > 4) {
                  System.out.println("\nERROR: Please enter a valid number.");
                  selection = scan.nextInt();
                }

                switch (selection) {
                case 1:
                  // do {
                  System.out.println("\nManager Updating employee info Menu: \nSelect what you want to do (INT):");
                  System.out.println(
                      "1. Update address \n2. Update dependent's information \n3. Add a dependent \n4. View biweekly paycheck \n5. Update 401k match percent \n6. Update employee performance percent \n7. Update employee benefits \n8. Update employee contribution \n9. Update federal and state tax\n10. Exit the update employee info menu");
                  employee_selection = scan.nextInt();
                  scan.nextLine();

                  if (employee_selection == 10) {
                    // return;
                    break;
                  }

                  // sanity check for employee_selection
                  while (employee_selection < 1 || employee_selection > 9) {
                    System.out.println("\nERROR: Please enter a valid number.");
                    employee_selection = scan.nextInt();
                    scan.nextLine();
                  }

                  System.out.println(
                      "\nPlease enter the SSN of the employee you would like to update information for (STRING): ");
                  String inputSSN = scan.nextLine();
                  ArrayList<String> employeeSSN = new ArrayList<String>();
                  rs = stmt.executeQuery("Select SSN from employee");
                  while (rs.next()) {
                    employeeSSN.add(rs.getString(1));
                  }
                  Boolean inEmp = employeeSSN.contains(inputSSN);
                  while (inEmp != true) {
                    System.out.println("\nEnter a valid SSN (STRING): ");
                    inputSSN = scan.nextLine();
                    inEmp = employeeSSN.contains(inputSSN);
                  }

                  while (employee_selection != 10)// start employee_section while loop
                  {
                    switch (employee_selection) {
                    case 1: // update your address
                      System.out.println("\nEnter updated address (STRING): ");
                      String up_address = scan.nextLine();

                      try {
                        stmt.executeUpdate(
                            "update employee " + "set address = '" + up_address + "' where SSN = '" + inputSSN + "'");
                      } catch (SQLException sqle) {
                        System.out.println("\nCould not update address." + sqle);
                      }
                      break; // for case 1 in employee selection

                    case 2: // update dependent's name and relationship
                      System.out.println(
                          "\nEnter the SSN of the dependent of the employee you want to update for (STRING): ");
                      String input_depSSN = scan.nextLine();
                      depArray = new ArrayList<String>();
                      rs = stmt.executeQuery("Select dependent_SSN from dependents where SSN = '" + inputSSN + "'");
                      while (rs.next()) {
                        depArray.add(rs.getString(1));
                      }
                      boolean inDep = depArray.contains(input_depSSN);
                      while (inDep != true) {
                        System.out.println("\nEnter a valid SSN");
                        input_depSSN = scan.nextLine();
                        inDep = depArray.contains(input_depSSN);
                      }

                      System.out
                          .println("\nSelect the information you want to update for the employee's dependent (INT): ");
                      System.out.println("1. Dependent's full name \n2. Dependent's relationship to you");
                      int dep_selection = scan.nextInt();
                      scan.nextLine();

                      // sanity check for updating dependent selection
                      while (dep_selection < 1 || dep_selection > 2) {
                        System.out.println("\nERROR: Please enter a valid number.");
                        dep_selection = scan.nextInt();
                        scan.nextLine();
                      }
                      switch (dep_selection) {
                      case 1: // dependent's name
                        System.out.println("\nEnter the dependent's updated name (STRING): ");
                        String up_depname = scan.nextLine();
                        try {
                          stmt.executeUpdate("update dependents " + "set full_name = '" + up_depname + "' where SSN = '"
                              + inputSSN + "' and dependent_SSN = '" + input_depSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update dependent's name." + sqle);
                        }
                        break; // for case 1 in dependent selection

                      case 2: // dependent's relationship
                        System.out.println("\nEnter the dependent's updated relationship to the employee (STRING): ");
                        String up_deprel = scan.nextLine();
                        try {
                          stmt.executeUpdate("update dependents " + "set relationship = '" + up_deprel
                              + "' where SSN = '" + inputSSN + "' and dependent_SSN = '" + input_depSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update dependent's relationship." + sqle);
                        }
                        break; // for case 2 in dependent selection
                      }
                      break; // for case 2 in emeployee selection

                    case 3: // add a dependent
                      System.out.println("\nEnter the dependent's full name (STRING): ");
                      String new_dependentname = scan.nextLine();
                      System.out.println("\nEnter the dependent's SSN (STRING): ");
                      String new_dependentSSN = scan.nextLine();

                      depArray = new ArrayList<String>();
                      rs = stmt.executeQuery("Select dependent_SSN from dependents where SSN = '" + SSN + "'");
                      while (rs.next()) {
                        depArray.add(rs.getString(1));
                      }
                      inDep = depArray.contains(new_dependentSSN);
                      while (inDep == true) {
                        System.out.println("Enter a valid SSN (STRING)");
                        new_dependentSSN = scan.nextLine();
                        inDep = depArray.contains(new_dependentSSN);
                      }

                      System.out.println("\nEnter the dependent's relationship to you (STRING): ");
                      String new_dependentrel = scan.nextLine();

                      try {
                        stmt.executeUpdate(
                            "insert into dependents (full_name, dependent_SSN, relationship, SSN) values ('"
                                + new_dependentname + "', '" + new_dependentSSN + "', '" + new_dependentrel + "', '"
                                + SSN + "')");
                      } catch (SQLException sqle) {
                        System.out.println("\nCould not insert dependent." + sqle);
                      }
                      break; // for case 3 in employee selection

                    case 4: // view your paycheck

                      try {
                        rs = stmt.executeQuery("Select * from biweekly_paycheck where SSN = '" + inputSSN + "'");
                        System.out.println(
                            "\nUsername | SSN | BiWeekly Salary | Bonus | Medicare Amount | State Tax Amount | Federal Tax Amount | Social Security Amount | 401k Amount | Insurance Amount");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                              + rs.getString(7) + " | " + rs.getString(8) + " | " + rs.getString(9) + " | "
                              + rs.getString(10));
                        }
                      } catch (SQLException sqle) {
                        System.out.println("\nCould not view biweekly paycheck." + sqle);
                      }

                      break; // for case 4 in employee selection

                    case 5: // Update your 401k match percent
                      System.out.println("\nEnter your updated 401k match percent (FLOAT): ");
                      Double updated_401kper = scan.nextDouble();
                      scan.nextLine();
                      try {
                        stmt.executeUpdate("update Benefit_401k " + "set employeeContribution_ben = " + updated_401kper
                            + " where SSN = '" + inputSSN + "'");
                      } catch (SQLException sqle) {
                        System.out.println("\nCould not update 401k match percent." + sqle);
                      }
                      break; // for case 5 in employee selection

                    case 6: // update employee's performance percent
                      System.out.println(
                          "\nEmployee performance is graded from the following list: 0, 0.5, 1, 1.5, where 1.5 is very satisfactory and 0 is completely unsatisfactory. \nEnter the updated employee performance (FLOAT): ");
                      Double updated_perfper = scan.nextDouble();
                      scan.nextLine();
                      try {
                        stmt.executeUpdate("update Bonus " + "set employeePerformance = " + updated_perfper
                            + " where SSN = '" + inputSSN + "'");
                      } catch (SQLException sqle) {
                        System.out.println("\nCould not update performance percent." + sqle);
                      }
                      break; // for case 6 in employee selection

                    case 7:// Update employee benefits
                      int userSel = 0;

                      System.out.println(
                          "\nPlease select what you would like to change (INT):\n1. Health Plan\n2. Attorney Plan \n3. Dental insurance\n4. Vision insurance\n5. Life insurance");
                      userSel = scan.nextInt();
                      scan.nextLine();
                      // while (userSel != 6) {

                      while (userSel < 1 || userSel > 5) {
                        System.out.println("\nPlease enter a valid menu choice number (INT): ");
                        userSel = scan.nextInt();
                        scan.nextLine();
                      }
                      String plan = "";

                      switch (userSel) {
                      case 1:
                        System.out.println("\nPlease enter the employee's new health plan (STRING):");
                        plan = scan.nextLine();
                        try {
                          stmt.executeUpdate(
                              "update Benefits " + "set healthPlan = '" + plan + "' where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update health plan" + sqle);
                        }
                        break;
                      case 2:
                        System.out.println("\nPlease enter the employee's new attorney plan (STRING):");
                        plan = scan.nextLine();
                        try {
                          stmt.executeUpdate(
                              "update Benefits " + "set attorneyPlan = '" + plan + "' where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update attorney plan" + sqle);
                        }
                        break;
                      case 3:
                        System.out.println("\nPlease enter the employee's new dental insurance (STRING): ");
                        plan = scan.nextLine();
                        try {
                          stmt.executeUpdate("update Health_Benefits " + "set dentalInsurance = '" + plan
                              + "' where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update dental insurance" + sqle);
                        }
                        break;

                      case 4:
                        System.out.println("\nPlease enter the employee's new vision insurance (STRING): ");
                        plan = scan.nextLine();
                        try {
                          stmt.executeUpdate("update Health_Benefits " + "set visionInsurance = '" + plan
                              + "' where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update vision insurance" + sqle);
                        }
                        break;

                      case 5:
                        System.out.println("\n Please enter the employee's new life insurance (STRING): ");
                        plan = scan.nextLine();
                        try {
                          stmt.executeUpdate("update Health_Benefits " + "set lifeInsurance = '" + plan
                              + "' where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update life insurance" + sqle);
                        }
                        break;

                      }
                      // }

                      break; // break case 7 of manger

                    case 8:// Update employee contribution

                      int userSelection = 0;
                      // while (userSelection != 4) {

                      System.out.println(
                          "\nPlease select which contribution would like to update (INT):\n1. SSN contribution\n2. Insurance contribution\n3. 401k contribution");
                      userSelection = scan.nextInt();
                      scan.nextLine();

                      while (userSelection < 1 || userSelection > 3) {
                        System.out.println("\nPlease enter a valid menu choice number (INT): ");
                        userSelection = scan.nextInt();
                        scan.nextLine();
                      }

                      String con;

                      switch (userSelection) {
                      case 1:
                        System.out.println("\nPlease enter the employee's new SSN contribution (FLOAT): ");
                        con = scan.nextLine();
                        try {
                          stmt.executeUpdate("update Social_Security " + "set employeePercent = " + con
                              + " where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update SSN contribution" + sqle);
                        }
                        break;
                      case 2:
                        System.out.println("\nPlease enter the employee's new insurance contribution (FLOAT): ");
                        con = scan.nextLine();
                        try {
                          stmt.executeUpdate("update Insurance " + "set employeeContribution_ins = " + con
                              + " where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update insurance contribution" + sqle);
                        }
                        break;
                      case 3:
                        System.out.println("\nPlease enter the employee's new 401k contribution (FLOAT): ");
                        con = scan.nextLine();
                        try {
                          stmt.executeUpdate("update Benefit_401k " + " set employeeContribution_ben = " + con
                              + " where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update 401k contribution" + sqle);
                        }
                        break;

                      }

                      break; // end of case 8

                    case 9:
                      int uses = 0;

                      System.out
                          .println("\nPlease select which tax you would like to change (INT):\n1. State\n2. Federal");
                      uses = scan.nextInt();
                      scan.nextLine();

                      while (uses < 1 || uses > 2) {
                        System.out.println("\nERROR: Please enter a valid number.");
                        uses = scan.nextInt();
                        scan.nextLine();
                      }

                      String taxes;

                      switch (uses) {
                      case 1:
                        System.out.println("\nPlease enter which state the employee lives in (STRING): ");
                        String state = scan.nextLine();
                        System.out.println("\nPlease enter new state tax rate (FLOAT): ");
                        taxes = scan.nextLine();
                        try {
                          stmt.executeUpdate(
                              "Update State " + "set stateName = '" + state + "' where SSN = '" + inputSSN + "'");
                          stmt.executeUpdate(
                              "Update State " + "set stateTaxRate = " + taxes + " where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update state taxes" + sqle);
                        }
                        break;

                      case 2:
                        System.out.println("\nPlease enter new federal tax rate (FLOAT): ");
                        taxes = scan.nextLine();
                        try {
                          stmt.executeUpdate(
                              "Update Federal " + " set taxRate = " + taxes + " where SSN = '" + inputSSN + "'");
                        } catch (SQLException sqle) {
                          System.out.println("\nCould not update federal taxes" + sqle);
                        }

                      }
                      // }
                      break;// break for case 10
                    case 10:
                      // hv to log in again

                      break;// return for case 11

                    } // end of switch case for employee selection

                    if (employee_selection == 10) {
                      // return;
                      System.out.println("\nexited manager update menu");
                      break;
                    }
                    employee_selection = 0;
                    System.out.println(
                        "\nManager Updating employee info Menu (INT): \n1. Update address \n2. Update dependent's information \n3. Add a dependent \n4. View biweekly paycheck \n5. Update 401k match percent \n6. Update employee performance percent \n7. Update employee benefits \n8. Update employee contribution \n9. Update federal and state tax\n10. Exit the update employee info menu");
                    employee_selection = scan.nextInt();
                    scan.nextLine();

                    while (employee_selection < 1 || employee_selection > 10) {
                      System.out.println("\nERROR: Please enter a valid number.");
                      employee_selection = scan.nextInt();
                      scan.nextLine();
                    }

                  } // end employee selection while loop

                  break;// leaving case1 of manager
                case 2:
                  System.out.println("\nSelect which option you would like (INT):");
                  System.out.println("1. All employees\n2. Specific Employee");
                  selection2 = scan.nextInt();
                  scan.nextLine();
                  while (selection2 < 1 || selection2 > 2) {
                    System.out.println("\nERROR: Please enter a valid number.");
                    selection2 = scan.nextInt();
                    scan.nextLine();
                  }

                  if (selection2 == 2) {
                    System.out.println("\nEnter the SSN of the employee you would like to see (STRING)");
                    inputUser = scan.nextLine();
                    try {
                      rs = stmt.executeQuery("Select * from employee where SSN = '" + inputUser + "'");
                      System.out.println(
                          "\nUsername | First Name | Last Name | Address | Job Title | Salary Type | Salary | SSN");
                      while (rs.next()) {
                        System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                            + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                            + rs.getString(7) + " | " + rs.getString(8));
                      }
                    } catch (SQLException e) {
                      System.out.println("ERROR in Manager Select * from employee where SSN =");
                    }
                  } else {
                    try {
                      rs = stmt.executeQuery("Select * from employee");
                      System.out.println(
                          "\nUsername | First Name | Last Name | Address | Job Title | Salary Type | Salary | SSN");
                      while (rs.next()) {
                        System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                            + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                            + rs.getString(7) + " | " + rs.getString(8));
                      }
                    } catch (SQLException e) {
                      System.out.println("\nERROR in Manager Select * from employee");
                    }
                  }

                  break;
                case 3:
                  System.out.println("\nSelect which report you want to view (INT):");
                  System.out.println("1. W2\n2. Biweekly Paycheck\n3. Expense Report");
                  selection2 = scan.nextInt();
                  scan.nextLine();
                  while (selection2 < 1 || selection2 > 3) {
                    System.out.println("\nERROR: Please enter a valid number.");
                    selection2 = scan.nextInt();
                    scan.nextLine();
                  }


                  if (selection2!=3){
                    System.out.println("\nSelect which option you would like (INT):");
                    System.out.println("1. Specific employee\n2. All users");
                    selection3 = scan.nextInt();
                    scan.nextLine();
                
                    while (selection3 < 1 || selection3 > 2) {
                        System.out.println("\nERROR: Please enter a valid number.");
                        selection3 = scan.nextInt();
                        scan.nextLine();
                    }
                  }




                  /* System.out.println("\nSelect which option you would like (INT):");
                  System.out.println("1. Specific employee\n2. All users");
                  selection3 = scan.nextInt();
                  scan.nextLine();
                  while (selection3 < 1 || selection3 > 2) {
                    System.out.println("\nERROR: Please enter a valid number.");
                    selection3 = scan.nextInt();
                    scan.nextLine(); */
                  }

                  switch (selection2) {
                  case 1:
                    if (selection3 == 1) {
                      // select on employee
                      System.out
                          .println("\nEnter the SSN of the employee you would like to view the W2 Report for (STRING)");
                      inputUser = scan.nextLine();
                      try {
                        // System.out.println("\nSelect * from W2 where SSN = '" + inputUser +
                        // "'");
                        rs = stmt.executeQuery("Select * from W2 where SSN = '" + inputUser + "'");
                        System.out.println("\nUsername | SSN | Salary | Bonus | Deduction");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5));
                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from W2 where username =");
                      }
                    } else {
                      // create whole table
                      try {
                        rs = stmt.executeQuery("Select * from W2");
                        System.out.println("\nUsername | SSN | Salary | Bonus | Deduction");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5));

                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from W2");
                      }
                    }
                    break;
                  case 2:
                    if (selection3 == 1) {
                      // select on employee
                      System.out.println(
                          "\nEnter the SSN of the employee you would like to view biweekly paycheck for (STRING)");
                      inputUser = scan.nextLine();
                      try {
                        rs = stmt.executeQuery("Select * from biweekly_paycheck where SSN = '" + inputUser + "'");
                        System.out.println(
                            "\nUsername | SSN | BiWeekly Salary | Bonus | Medicare Amount | State Tax Amount | Federal Tax Amount | Social Security Amount | 401k Amount | Insurance Amount");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                              + rs.getString(7) + " | " + rs.getString(8) + " | " + rs.getString(9) + " | "
                              + rs.getString(10));
                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from biweekly_paycheck where username =");
                      }
                    } else {
                      // create whole table
                      try {
                        rs = stmt.executeQuery("Select * from biweekly_paycheck");
                        System.out.println(
                            "\nUsername | SSN | BiWeekly Salary | Bonus | Medicare Amount | State Tax Amount | Federal Tax Amount | Social Security Amount | 401k Amount | Insurance Amount");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                              + rs.getString(7) + " | " + rs.getString(8) + " | " + rs.getString(9) + " | "
                              + rs.getString(10));
                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from biweekly_paycheck");
                      }
                    }
                    break;
                  case 3:
                    //if (selection3 == 1) {
                      // select on employee
                      System.out.println("\nExpense Report Menu (INT)");
                      System.out.println("\n1. Total Company\n2. Split by Employee\n3. Specific Employee");

                      int num = scan.nextInt();
                      scan.nextLine();
                      if (num == 3) {
                        System.out.println(
                            "\nEnter the SSN of the employee you would like to view Expense Report for (STRING)");
                        inputUser = scan.nextLine();
                        try {
                          rs = stmt.executeQuery("Select * from expenseReport where SSN = '" + inputUser + "'");
                          System.out.println(
                              "\nUsername | SSN | Salary | Bonus | Benefits Cost | Social Security Cost | Insurance Cost");
                          while (rs.next()) {
                            System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3)
                                + " | " + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                                + rs.getString(7));
                          }
                        } catch (SQLException e) {
                          System.out.println("\nERROR in Manager Select * from expenseReport where username =");
                        }
                      } else if (num == 2) {
                        try {
                          rs = stmt.executeQuery("Select * from expenseReport");
                          System.out.println(
                              "\nUsername | SSN | Salary | Bonus | Benefits Cost | Social Security Cost | Insurance Cost");
                          while (rs.next()) {
                            System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3)
                                + " | " + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                                + rs.getString(7));
                          }
                        } catch (SQLException e) {
                          System.out.println("\nERROR in Manager Select * from expenseReport");
                        }
                      } else if (num == 1) {
                        rs = stmt.executeQuery("Select * from expenseReportTotal");
                        System.out.println(
                            "\nSalary | Bonus | 401k Contribution Cost | Social Security Cost | Insurance Cost");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5));
                        }
                      } else {
                        System.out.println("INVALID NUMBER");
                      }

                    //}//end of if
                    break;
                  case 4:
                    System.out.println("\nExited");
                    return;

                  }
                  // PUT INSIDE WHILE
                }
            
              

            case "admin":
              selection3 =0;
              selection = 0;
              while (selection != 4) {
                System.out.println("\nADMIN MENU: \nSelect what you want to do (INT):");
                System.out.println("1. Add employee \n2. View report \n3. Delete an employee \n4. Leave the program");
                selection = scan.nextInt();
                scan.nextLine();
                while (selection < 1 || selection > 4) {
                  System.out.println("\nERROR: Please enter a valid number.");
                  selection = scan.nextInt();
                  scan.nextLine();
                }
                switch (selection) {
                case 1: // case 1 for admin case: add employee
                  String newem_ssn;
                  String newem_salaryTy;
                  try {

                    System.out.println("\nEnter first name (STRING): ");
                    String newem_firstN = scan.nextLine();
                    System.out.println("\nEnter last name (STRING): ");
                    String newem_lastN = scan.nextLine();
                    System.out.println("\nEnter address (STRING): ");
                    String newem_add = scan.nextLine();
                    System.out.println(
                        "\nEnter job title (choose one of the following: employee, manager, admin) (STRING): ");
                    String newem_job = scan.nextLine().toLowerCase();
                    System.out
                        .println("\nEnter salary type (choose one of the following: hourly or annual) (STRING): ");

                    newem_salaryTy = scan.nextLine().toLowerCase();

                    System.out.println("\nEnter the hours worked (INT). 0 if they haven't worked any");
                    int hoursWorked = scan.nextInt();
                    scan.nextLine();

                    System.out.println("\nEnter salary (INT): ");
                    int newem_salary = scan.nextInt();
                    scan.nextLine();
                    System.out.println("\nEnter SSN (STRING) ");
                    newem_ssn = scan.nextLine();
                    System.out.println("\nEnter username (STRING): ");
                    String newem_userN = scan.nextLine();
                    System.out.println("\nEnter password (STRING): ");
                    String newem_passw = scan.nextLine();

                    stmt.executeUpdate(
                        "insert into employee (firstName, lastName, address, jobTitle, salaryType , hoursWorked, salary, SSN, username, user_password) values ('"
                            + newem_firstN + "', '" + newem_lastN + "', '" + newem_add + "', '" + newem_job + "', '"
                            + newem_salaryTy + "'," + hoursWorked + ",'" +
                            // "', '"
                            +newem_salary + "', '" + newem_ssn + "', '" + newem_userN + "', '" + newem_passw + "')");

                    // double check: checked once
                  } catch (SQLException sqle) {

                    System.out.println("\nCould not insert new employee" + sqle);
                    break;
                  }

                  // start alisha's code
                  // FEDERAL
                  System.out.println("\nEnter tax rate (FLOAT)");
                  double taxRate = scan.nextDouble();
                  scan.nextLine();
                  // COME BACK HERE
                  System.out.println("\nEnter bracket (STRING)");
                  String federalBracket = scan.nextLine();

                  stmt.executeUpdate("insert into federal (taxRate, bracket, SSN) values (" + taxRate + " ,'"
                      + federalBracket + "' ,'" + newem_ssn + "')");

                  // MEDICARE
                  System.out.println("\nEnter medicare rate (FLOAT)");
                  double medicareRate = scan.nextDouble();
                  scan.nextLine();

                  stmt.executeUpdate(
                      "insert into medicare (rate, SSN) values (" + medicareRate + " ,'" + newem_ssn + "')");

                  // STATE GOT
                  System.out.println("\nEnter state name (STRING)");
                  String state = scan.nextLine();
                  System.out.println("\nEnter state tax rate (FLOAT)");
                  double stateTaxRate = scan.nextDouble();
                  scan.nextLine();
                  // printing out state insert table
                  /*
                   * System.out.
                   * println("insert into State (stateName, stateTaxRate, SSN) values ('" + state
                   * + "'," + stateTaxRate + ",'" + newem_ssn + "')");
                   */

                  stmt.executeUpdate("insert into State (stateName, stateTaxRate, SSN) values ('" + state + "',"
                      + stateTaxRate + ",'" + newem_ssn + "')");

                  // Social Security
                  double employerSocialRate;
                  double employeeSocialRate;
                  if (newem_salaryTy.toLowerCase().equals("hourly")) {
                    employeeSocialRate = 0.15;
                    employerSocialRate = 0;
                  } else {
                    employeeSocialRate = 0.075;
                    employerSocialRate = 0.075;
                  }

                  stmt.executeUpdate(
                      "insert into Social_Security(totalPercent, employeePercent, employerPercent, SSN) values (" + 0.15
                          + " ," + employeeSocialRate + "," + employerSocialRate + ",'" + newem_ssn + "')");

                  // benefits
                  System.out.println("\nEnter health plan (STRING)");
                  String healthPlan = scan.nextLine();
                  System.out.println("\nEnter attorney plan (STRING)");
                  String attorneyPlan = scan.nextLine();

                  stmt.executeUpdate("insert into Benefits(healthPlan, attorneyPlan, SSN) values (" + "'" + healthPlan
                      + "','" + attorneyPlan + "','" + newem_ssn + "')");

                  // DEPENDENTS
                  System.out.println("\nEnter 1 if you would like to enter dependents for this employee, else enter 2");
                  int num = scan.nextInt();
                  scan.nextLine();
                  while (num == 1) {
                    num = 0;
                    System.out.println("\nEnter the full name of the dependent (STRING)");
                    String depName = scan.nextLine();
                    System.out.println("\nEnter the SSN of the dependent (STRING)");
                    String depSSN = scan.nextLine();

                    depArray = new ArrayList<String>();
                    rs = stmt.executeQuery("Select dependent_SSN from dependents");
                    while (rs.next()) {
                      depArray.add(rs.getString(1));
                    }
                    boolean inDep = depArray.contains(depSSN);
                    while (inDep == true) {
                      System.out.println("\nEnter a valid SSN");
                      depSSN = scan.nextLine();
                      inDep = depArray.contains(depSSN);
                    }

                    // PRINT DEPENDETS
                    System.out.println("\nEnter the relationship to the dependent (STRING)");
                    String depRel = scan.nextLine();

                    stmt.executeUpdate("insert into Dependents(full_name, dependent_SSN, relationship, SSN) values ("
                        + "'" + depName + "','" + depSSN + "','" + depRel + "','" + newem_ssn + "')");

                    System.out.println(
                        "\nEnter 1 if you would like to continue to enter dependents for this employee , else enter 2");
                    num = scan.nextInt();
                    scan.nextLine();
                  }

                  // INSURANCE
                  System.out.println("\nEnter the insurance plan (STRING)");
                  String insurancePlan = scan.nextLine();
                  System.out.println("\nEnter the individual cost (INT)");
                  double individualCost = scan.nextDouble();
                  scan.nextLine();
                  System.out.println("\nEnter the family cost (INT)");
                  double familyCost = scan.nextDouble();
                  scan.nextLine();
                  System.out.println("\nEnter the employee contribution (FLOAT)");
                  double employeeC = scan.nextDouble();
                  scan.nextLine();
                  System.out.println("\nEnter the employer contribution (FLOAT)");
                  double employerC = scan.nextDouble();
                  scan.nextLine();

                  stmt.executeUpdate(
                      "insert into Insurance (insurancePlan, individualCost, familyCost, employeeContribution_ins,employerContribution_ins,SSN) values ("
                          + "'" + insurancePlan + "'," + individualCost + "," + familyCost + "," + employeeC + ","
                          + employerC + ",'" + newem_ssn + "')");

                  // HEALTH_BENEFITS
                  System.out.println("\nEnter 1 if you would like to add health benefits , else enter 2");
                  num = 0;
                  num = scan.nextInt();
                  scan.nextLine();
                  if (num == 1) {
                    System.out.println("\nEnter the dental insurance plan (STRING)");
                    String dental = scan.nextLine();

                    System.out.println("\nEnter the vision insurance plan (STRING)");
                    String vision = scan.nextLine();

                    System.out.println("\nEnter the life insurance plan (STRING)");
                    String life = scan.nextLine();

                    stmt.executeUpdate(
                        "insert into Health_Benefits(dentalInsurance,visionInsurance,lifeInsurance,SSN) values (" + "'"
                            + dental + "','" + vision + "','" + life + "','" + newem_ssn + "')");
                  }

                  // BENEFIT_401K
                  System.out.println("\nEnter the employee contribution rate for 401k (FLOAT)");
                  employeeC = 0;
                  employerC = 0;
                  employeeC = scan.nextDouble();
                  scan.nextLine();

                  System.out.println("\nEnter the employer contribution rate for 401k (FLOAT)");
                  employerC = scan.nextDouble();
                  scan.nextLine();

                  stmt.executeUpdate(
                      "insert into Benefit_401k(employeeContribution_ben, employerContribution_ben, SSN) values("
                          + employeeC + "," + employerC + ",'" + newem_ssn + "')");

                  // BONUS
                  System.out.println("\nEnter the employee performance rate [0, 0.5, 1, or 1.5] (FLOAT) ");
                  double performance = scan.nextDouble();
                  scan.nextLine();

                  stmt.executeUpdate("insert into Bonus(employeePerformance,companyPercent,SSN) values(" + performance
                      + "," + 1.5 + ",'" + newem_ssn + "')");

                  // end alisha's code

                  break;

                case 2: // case 2 for admin case: view reports
                  System.out.println("\nADMIN REPORT MENU:\nSelect which report you want to view (INT):");
                  System.out.println("1. W2\n2. Biweekly Paycheck\n3. Expense Report");
                  selection2 = scan.nextInt();
                  scan.nextLine();
                  while (selection2 < 1 || selection2 > 3) {
                    System.out.println("\nERROR: Please enter a valid number.");
                    selection2 = scan.nextInt();
                    scan.nextLine();
                  }
                  
                  if (selection2!=3){
                    System.out.println("\nSelect which option you would like (INT):");
                    System.out.println("1. Specific employee\n2. All users");
                    selection3 = scan.nextInt();
                    scan.nextLine();
                
                    while (selection3 < 1 || selection3 > 2) {
                        System.out.println("\nERROR: Please enter a valid number.");
                        selection3 = scan.nextInt();
                        scan.nextLine();
                    }
                  }

                  switch (selection2) {
                  case 1: // case 1 for case admin: W2
                    if (selection3 == 1) {
                      // select on employee
                      System.out.println("\nEnter the SSN of the employee you would like to see (STRING)");
                      inputUser = scan.nextLine();
                      try {
                        rs = stmt.executeQuery("Select * from W2 where SSN = '" + inputUser + "'");
                        System.out.println("\nUsername | SSN | Salary | Bonus | Deduction");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5));
                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from W2 where username =");
                      }
                    } else {
                      // create whole table
                      try {
                        rs = stmt.executeQuery("Select * from W2");
                        System.out.println("\nUsername | SSN | Salary | Bonus | Deduction");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5));

                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from W2");
                      }
                    }
                    break;
                  case 2: // case 2 of case 1 for admin case: paycheck
                    if (selection3 == 1) {
                      // select on employee
                      System.out.println("\nEnter the SSN of the employee you would like to see (STRING)");
                      inputUser = scan.nextLine();
                      try {
                        rs = stmt.executeQuery("Select * from biweekly_paycheck where SSN = '" + inputUser + "'");
                        System.out.println(
                            "\nUsername | SSN | BiWeekly Salary | Bonus | Medicare Amount | State Tax Amount | Federal Tax Amount | Social Security Amount | 401k Amount | Insurance Amount");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                              + rs.getString(7) + " | " + rs.getString(8) + " | " + rs.getString(9) + " | "
                              + rs.getString(10));
                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from biweekly_paycheck where username =");
                      }
                    } else {
                      // create whole table
                      try {
                        rs = stmt.executeQuery("Select * from biweekly_paycheck");
                        System.out.println(
                            "\nUsername | SSN | BiWeekly Salary | Bonus | Medicare Amount | State Tax Amount | Federal Tax Amount | Social Security Amount | 401k Amount | Insurance Amount");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                              + rs.getString(7) + " | " + rs.getString(8) + " | " + rs.getString(9) + " | "
                              + rs.getString(10));
                        }
                      } catch (SQLException e) {
                        System.out.println("\nERROR in Manager Select * from biweekly_paycheck");
                      }
                    }
                    break;
                  case 3: // case 3 of case 1 for admin case: expensereport
                    //if (selection3 == 1) {
                      // select on employee
                      System.out.println("\nExpense Report Menu (INT)");
                      System.out.println("\n1. Total Company\n2. Split by Employee\n3. Specific Employee");
                      num=0;
                      num = scan.nextInt();
                      scan.nextLine();
                      if (num == 3) {
                        System.out.println(
                            "\nEnter the SSN of the employee you would like to view Expense Report for (STRING)");
                        inputUser = scan.nextLine();
                        try {
                          rs = stmt.executeQuery("Select * from expenseReport where SSN = '" + inputUser + "'");
                          System.out.println(
                              "\nUsername | SSN | Salary | Bonus | Benefits Cost | Social Security Cost | Insurance Cost");
                          while (rs.next()) {
                            System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3)
                                + " | " + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                                + rs.getString(7));
                          }
                        } catch (SQLException e) {
                          System.out.println("\nERROR in Manager Select * from expenseReport where username =");
                        }
                      } else if (num == 2) {
                        try {
                          rs = stmt.executeQuery("Select * from expenseReport");
                          System.out.println(
                              "\nUsername | SSN | Salary | Bonus | Benefits Cost | Social Security Cost | Insurance Cost");
                          while (rs.next()) {
                            System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3)
                                + " | " + rs.getString(4) + " | " + rs.getString(5) + " | " + rs.getString(6) + " | "
                                + rs.getString(7));
                          }
                        } catch (SQLException e) {
                          System.out.println("\nERROR in Manager Select * from expenseReport");
                        }
                      } else if (num == 1) {
                        rs = stmt.executeQuery("Select * from expenseReportTotal");
                        System.out.println(
                            "\nSalary | Bonus | 401k Contribution Cost | Social Security Cost | Insurance Cost");
                        while (rs.next()) {
                          System.out.println(rs.getString(1) + " | " + rs.getString(2) + " | " + rs.getString(3) + " | "
                              + rs.getString(4) + " | " + rs.getString(5));
                        }
                      } else {
                        System.out.println("INVALID NUMBER");
                      }

                    //}//end of if
                    break;
                  }
                  break; // break for swtch case in case 2 in admin

                case 3: // remove employee
                  System.out.println("\nPlease enter the SSN of the employee you want to remove (STRING)");
                  String ne_ssn = scan.nextLine();
                  // System.out.println("DELETE FROM employee" + " WHERE SSN = '" + ne_ssn + "'");
                  stmt.executeUpdate("DELETE FROM employee" + " WHERE SSN = '" + ne_ssn + "'");
                  System.out.println("worked");
                  break;

                case 4: // leave
                  System.out.println("Exited");
                  return;

                }

              }

            }
          }

        }

      } catch (SQLException sqle) {
        System.out.println("This username doesn't exist");
      }

    } catch (SQLException sqle) {
      System.out.println(sqle);
    }

  }
}
