package com.salesforce.qa.pages;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.pagefactory.AjaxElementLocatorFactory;

public class LoginPage {

    private static final Logger logger = LogManager.getLogger(LoginPage.class);
    private static final int TIMEOUT_SECONDS = 20;
    private WebDriver driver;

    @FindBy(xpath = "//input[@id='username']")
    private WebElement usernameField;

    @FindBy(xpath = "//input[@id='password']")
    private WebElement passwordField;

    @FindBy(xpath = "//input[@id='Login']")
    private WebElement loginButton;

    @FindBy(xpath = "//input[@id='rememberUn']")
    private WebElement rememberMeCheckbox;

    @FindBy(xpath = "//div[@id='error']")
    private WebElement errorMessageContainer;

    @FindBy(xpath = "//div[@id='logo_wrapper']")
    private WebElement logoWrapper;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        AjaxElementLocatorFactory factory = new AjaxElementLocatorFactory(driver, TIMEOUT_SECONDS);
        PageFactory.initElements(factory, this);
        logger.debug("LoginPage initialized with AjaxElementLocatorFactory");
    }

    public void enterUsername(String username) {
        try {
            usernameField.clear();
            usernameField.sendKeys(username);
            logger.debug("Username entered: {}", username);
        } catch (Exception e) {
            logger.error("Failed to enter username: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to enter username", e);
        }
    }

    public void enterPassword(String password) {
        try {
            passwordField.clear();
            passwordField.sendKeys(password);
            logger.debug("Password entered");
        } catch (Exception e) {
            logger.error("Failed to enter password: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to enter password", e);
        }
    }

    public void clickLoginButton() {
        try {
            loginButton.click();
            logger.debug("Login button clicked");
        } catch (Exception e) {
            logger.error("Failed to click login button: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to click login button", e);
        }
    }

    public void doLogin(String username, String password) {
        try {
            enterUsername(username);
            enterPassword(password);
            clickLoginButton();
            logger.info("Login action completed for user: {}", username);
        } catch (Exception e) {
            logger.error("Login action failed: {}", e.getMessage(), e);
            throw new RuntimeException("Login action failed", e);
        }
    }

    public String getErrorMessage() {
        try {
            String errorText = errorMessageContainer.getText();
            logger.debug("Error message retrieved: {}", errorText);
            return errorText;
        } catch (Exception e) {
            logger.warn("Failed to retrieve error message: {}", e.getMessage());
            return "";
        }
    }

    public boolean isErrorMessageDisplayed() {
        try {
            boolean displayed = errorMessageContainer.isDisplayed();
            logger.debug("Error message displayed: {}", displayed);
            return displayed;
        } catch (Exception e) {
            logger.warn("Error message element not found: {}", e.getMessage());
            return false;
        }
    }

    public void clearAllFields() {
        try {
            usernameField.clear();
            passwordField.clear();
            logger.debug("All fields cleared");
        } catch (Exception e) {
            logger.error("Failed to clear fields: {}", e.getMessage(), e);
        }
    }

    public boolean isLoginPageDisplayed() {
        try {
            boolean displayed = loginButton.isDisplayed();
            logger.debug("Login page displayed: {}", displayed);
            return displayed;
        } catch (Exception e) {
            logger.warn("Login page check failed: {}", e.getMessage());
            return false;
        }
    }

    public String getPageTitle() {
        try {
            String title = driver.getTitle();
            logger.debug("Page title: {}", title);
            return title;
        } catch (Exception e) {
            logger.error("Failed to get page title: {}", e.getMessage(), e);
            return "";
        }
    }

    public String getCurrentUrl() {
        try {
            String url = driver.getCurrentUrl();
            logger.debug("Current URL: {}", url);
            return url;
        } catch (Exception e) {
            logger.error("Failed to get current URL: {}", e.getMessage(), e);
            return "";
        }
    }

    public void toggleRememberMe() {
        try {
            rememberMeCheckbox.click();
            logger.debug("Remember Me toggled");
        } catch (Exception e) {
            logger.error("Failed to toggle Remember Me: {}", e.getMessage(), e);
        }
    }
}