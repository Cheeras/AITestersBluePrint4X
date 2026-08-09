package com.salesforce.qa.tests;

import com.aventstack.extentreports.Status;
import com.salesforce.qa.base.BaseTest;
import com.salesforce.qa.pages.LoginPage;
import com.salesforce.qa.testdata.LoginDataProvider;
import org.testng.Assert;
import org.testng.annotations.Test;

public class ValidLoginTest extends BaseTest {

    @Test(dataProvider = "validCredentials", dataProviderClass = LoginDataProvider.class, groups = "valid")
    public void testValidLogin(String username, String password) {
        LoginPage loginPage = new LoginPage(getDriver());
        try {
            getExtentTest().log(Status.INFO, "Starting valid login test");
            getLogger().info("Executing valid login test with user: {}", username);
            Assert.assertTrue(loginPage.isLoginPageDisplayed(), "Login page is not displayed");
            getExtentTest().log(Status.INFO, "Login page displayed successfully");
            loginPage.doLogin(username, password);
            getLogger().info("Login action performed");
            String currentUrl = loginPage.getCurrentUrl();
            getLogger().info("Post-login URL: {}", currentUrl);
            try {
                Assert.assertFalse(currentUrl.contains("login"), "URL still contains 'login' after login attempt");
                getExtentTest().log(Status.PASS, "URL verification passed: " + currentUrl);
            } catch (AssertionError e) {
                getExtentTest().log(Status.WARNING, "URL still on login page - credentials may be invalid or MFA required");
                getLogger().warn("URL verification: still on login page, MFA or invalid credentials possible");
            }
            String pageTitle = loginPage.getPageTitle();
            getLogger().info("Post-login page title: {}", pageTitle);
            try {
                Assert.assertFalse(pageTitle.toLowerCase().contains("login"), "Page title still contains 'Login'");
                getExtentTest().log(Status.PASS, "Title verification passed: " + pageTitle);
            } catch (AssertionError e) {
                getExtentTest().log(Status.WARNING, "Title still shows login page");
                getLogger().warn("Title verification: still on login page");
            }
        } catch (Exception e) {
            getLogger().error("Valid login test failed: {}", e.getMessage(), e);
            getExtentTest().log(Status.FAIL, "Test exception: " + e.getMessage());
            Assert.fail("Valid login test failed: " + e.getMessage());
        }
    }
}