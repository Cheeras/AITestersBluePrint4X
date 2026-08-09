package com.salesforce.qa.testdata;

import com.salesforce.qa.utils.TestUtils;
import org.testng.annotations.DataProvider;

public class LoginDataProvider {

    @DataProvider(name = "validCredentials")
    public static Object[][] validCredentials() {
        String username = TestUtils.getProperty("valid.username");
        String password = TestUtils.getProperty("valid.password");
        return new Object[][]{
            {username, password}
        };
    }

    @DataProvider(name = "invalidCredentials")
    public static Object[][] invalidCredentials() {
        return new Object[][]{
            {"wronguser@test.com", "WrongPass123", "check your username and password"},
            {"", "", "enter your username"},
            {"validuser@test.com", "", "enter your password"},
            {"", "SomePassword123", "enter your username"}
        };
    }
}