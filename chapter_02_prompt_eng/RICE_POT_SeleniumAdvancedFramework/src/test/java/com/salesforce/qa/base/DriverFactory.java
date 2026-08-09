package com.salesforce.qa.base;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class DriverFactory {

    private static final ThreadLocal<WebDriver> tlDriver = new ThreadLocal<>();
    private static final Logger logger = LogManager.getLogger(DriverFactory.class);

    private DriverFactory() {
    }

    public static WebDriver getDriver(String browser) {
        try {
            String browserName = (browser != null && !browser.isEmpty()) ? browser.toLowerCase() : "chrome";
            logger.info("Initializing WebDriver for browser: {}", browserName);
            WebDriver driver;
            switch (browserName) {
                case "firefox":
                    WebDriverManager.firefoxdriver().setup();
                    driver = new FirefoxDriver();
                    break;
                case "edge":
                    WebDriverManager.edgedriver().setup();
                    driver = new EdgeDriver();
                    break;
                case "chrome":
                default:
                    WebDriverManager.chromedriver().setup();
                    driver = new ChromeDriver();
                    break;
            }
            tlDriver.set(driver);
            logger.info("WebDriver initialized successfully for: {}", browserName);
            return driver;
        } catch (Exception e) {
            logger.error("Failed to initialize WebDriver for browser: {}", browser, e);
            throw new RuntimeException("WebDriver initialization failed for: " + browser, e);
        }
    }

    public static WebDriver getTLDriver() {
        return tlDriver.get();
    }

    public static void quitDriver() {
        try {
            WebDriver driver = tlDriver.get();
            if (driver != null) {
                driver.quit();
                logger.info("WebDriver quit successfully");
            }
        } catch (Exception e) {
            logger.error("Failed to quit WebDriver: {}", e.getMessage());
        } finally {
            tlDriver.remove();
        }
    }
}