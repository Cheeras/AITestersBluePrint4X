package com.salesforce.qa.utils;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.FileInputStream;
import java.io.IOException;
import java.time.Duration;
import java.util.Properties;

public class TestUtils {

    private static Properties config;

    static {
        try {
            config = new Properties();
            FileInputStream fis = new FileInputStream("src/test/resources/config.properties");
            config.load(fis);
            fis.close();
        } catch (IOException e) {
            System.err.println("Failed to load config in TestUtils: " + e.getMessage());
            config = new Properties();
        }
    }

    private TestUtils() {
    }

    public static String getProperty(String key) {
        try {
            return config.getProperty(key);
        } catch (Exception e) {
            System.err.println("Failed to read property: " + key + " - " + e.getMessage());
            return null;
        }
    }

    public static void waitForElementVisible(WebDriver driver, WebElement element, int timeoutSeconds) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds));
            wait.until(ExpectedConditions.visibilityOf(element));
        } catch (Exception e) {
            System.err.println("Wait for element visibility failed: " + e.getMessage());
        }
    }

    public static void waitForElementClickable(WebDriver driver, WebElement element, int timeoutSeconds) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds));
            wait.until(ExpectedConditions.elementToBeClickable(element));
        } catch (Exception e) {
            System.err.println("Wait for element clickable failed: " + e.getMessage());
        }
    }

    public static void waitForPageLoad(WebDriver driver, int timeoutSeconds) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds));
            wait.until(webDriver -> {
                JavascriptExecutor js = (JavascriptExecutor) webDriver;
                String readyState = js.executeScript("return document.readyState").toString();
                return "complete".equals(readyState);
            });
        } catch (Exception e) {
            System.err.println("Wait for page load failed: " + e.getMessage());
        }
    }
}