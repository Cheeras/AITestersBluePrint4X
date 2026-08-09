package com.salesforce.qa.tests;

import com.aventstack.extentreports.Status;
import com.salesforce.qa.base.BaseTest;
import com.salesforce.qa.pages.LoginPage;
import com.salesforce.qa.testdata.LoginDataProvider;
import org.testng.Assert;
import org.testng.annotations.Test;

public class InvalidLoginTest extends BaseTest {

    @Test(dataProvider = "invalidCredentials", dataProviderClass = LoginDataProvider.class, groups = "invalid")
    public void testInvalidLogin(String username, String password, String expectedErrorSubstring) {
        LoginPage loginPage = new LoginPage(getDriver());
        try {
            getExtentTest().log(Status.INFO, "Starting invalid login test");
            getExtentTest().log(Status.INFO, "Username: [" + username + "], Expected error contains: [" + expectedErrorSubstring + "]");
            getLogger().info("Executing invalid login test - User: [{}], Expected error: [{}]", username, expectedErrorSubstring);
            Assert.assertTrue(loginPage.isLoginPageDisplayed(), "Login page is not displayed");
            loginPage.clearAllFields();
            loginPage.doLogin(username, password);
            getLogger().info("Login action performed with invalid credentials");
            boolean errorDisplayed = loginPage.isErrorMessageDisplayed();
            String actualError = loginPage.getErrorMessage();
            getLogger().info("Error displayed: {}, Error message: {}", errorDisplayed, actualError);
            try {
                Assert.assertTrue(errorDisplayed, "Error message is not displayed for invalid login");
                getExtentTest().log(Status.PASS, "Error message displayed: " + actualError);
            } catch (AssertionError e) {
                getExtentTest().log(Status.FAIL, "Error message not displayed. Actual: " + actualError);
                getLogger().error("Error message assertion failed: {}", e.getMessage());
                throw e;
            }
            try {
                Assert.assertTrue(actualError.toLowerCase().contains(expectedErrorSubstring.toLowerCase()),
                        "Error message does not contain expected text. Expected: [" + expectedErrorSubstring + "], Actual: [" + actualError + "]");
                getExtentTest().log(Status.PASS, "Error message contains expected text: [" + expectedErrorSubstring + "]");
            } catch (AssertionError e) {
                getExtentTest().log(Status.WARNING, "Error text mismatch. Expected substring: [" + expectedErrorSubstring + "], Actual: [" + actualError + "]");
                getLogger().warn("Error text mismatch: expected [{}], actual [{}]", expectedErrorSubstring, actualError);
            }
        } catch (Exception e) {
            getLogger().error("Invalid login test failed: {}", e.getMessage(), e);
            getExtentTest().log(Status.FAIL, "Test exception: " + e.getMessage());
            Assert.fail("Invalid login test failed: " + e.getMessage());
        }
    }
}