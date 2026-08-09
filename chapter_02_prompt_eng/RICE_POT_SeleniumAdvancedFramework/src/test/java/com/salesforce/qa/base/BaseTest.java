package com.salesforce.qa.base;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.Status;
import com.salesforce.qa.utils.ExtentManager;
import org.apache.commons.io.FileUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

public class BaseTest {

    private static final ThreadLocal<WebDriver> tlDriver = new ThreadLocal<>();
    private static volatile Properties config;
    private static volatile Logger logger;
    private static volatile ExtentReports extent;
    private static final ThreadLocal<ExtentTest> tlExtentTest = new ThreadLocal<>();

    @BeforeSuite
    public void beforeSuite() {
        try {
            getLogger().info("Initializing test suite");
            getConfig();
            getLogger().info("Configuration loaded successfully");
            getExtent();
            getLogger().info("ExtentReports initialized");
        } catch (Exception e) {
            System.err.println("Suite initialization failed: " + e.getMessage());
            throw new RuntimeException("Suite initialization failed", e);
        }
    }

    @BeforeTest
    @Parameters({"browser"})
    public void beforeTest(@Optional("chrome") String browser) {
        try {
            getLogger().info("Setting up browser: {}", browser);
            WebDriver driver = DriverFactory.getDriver(browser);
            tlDriver.set(driver);
            driver.manage().window().maximize();
            driver.manage().deleteAllCookies();
            int implicitWait = Integer.parseInt(getConfig().getProperty("implicit.wait", "10"));
            int pageLoadTimeout = Integer.parseInt(getConfig().getProperty("page.load.timeout", "30"));
            driver.manage().timeouts().implicitlyWait(implicitWait, TimeUnit.SECONDS);
            driver.manage().timeouts().pageLoadTimeout(pageLoadTimeout, TimeUnit.SECONDS);
            String baseUrl = getConfig().getProperty("base.url");
            driver.get(baseUrl);
            getLogger().info("Navigated to: {}", baseUrl);
        } catch (Exception e) {
            getLogger().error("Browser setup failed: {}", e.getMessage(), e);
            throw new RuntimeException("Browser initialization failed", e);
        }
    }

    @BeforeMethod
    public void beforeMethod() {
        ExtentTest extentTest = getExtent().createTest(getClass().getSimpleName());
        tlExtentTest.set(extentTest);
    }

    @AfterMethod
    public void afterMethod(ITestResult result) {
        ExtentTest extentTest = tlExtentTest.get();
        try {
            if (result.getStatus() == ITestResult.SUCCESS) {
                extentTest.log(Status.PASS, "Test passed: " + result.getMethod().getMethodName());
                logger.info("Test passed: {}", result.getMethod().getMethodName());
            } else if (result.getStatus() == ITestResult.FAILURE) {
                extentTest.log(Status.FAIL, "Test failed: " + result.getMethod().getMethodName());
                extentTest.log(Status.FAIL, result.getThrowable());
                logger.error("Test failed: {}", result.getMethod().getMethodName(), result.getThrowable());
                String screenshotPath = takeScreenshot(result.getMethod().getMethodName());
                if (screenshotPath != null) {
                    extentTest.addScreenCaptureFromPath(screenshotPath);
                }
            } else if (result.getStatus() == ITestResult.SKIP) {
                extentTest.log(Status.SKIP, "Test skipped: " + result.getMethod().getMethodName());
                logger.warn("Test skipped: {}", result.getMethod().getMethodName());
            }
        } catch (Exception e) {
            logger.error("AfterMethod logging failed: {}", e.getMessage());
        }
    }

    @AfterTest
    public void afterTest() {
        try {
            logger.info("Tearing down browser session");
            DriverFactory.quitDriver();
            tlDriver.remove();
        } catch (Exception e) {
            logger.error("Browser teardown failed: {}", e.getMessage());
        }
    }

    @AfterSuite
    public void afterSuite() {
        try {
            if (extent != null) {
                extent.flush();
                logger.info("ExtentReports flushed");
            }
        } catch (Exception e) {
            logger.error("Suite teardown failed: {}", e.getMessage());
        }
    }

    protected WebDriver getDriver() {
        return tlDriver.get();
    }

    protected Properties getConfig() {
        if (config == null) {
            synchronized (BaseTest.class) {
                if (config == null) {
                    try {
                        config = new Properties();
                        FileInputStream fis = new FileInputStream("src/test/resources/config.properties");
                        config.load(fis);
                        fis.close();
                    } catch (IOException e) {
                        throw new RuntimeException("Failed to load config", e);
                    }
                }
            }
        }
        return config;
    }

    protected Logger getLogger() {
        if (logger == null) {
            synchronized (BaseTest.class) {
                if (logger == null) {
                    logger = LogManager.getLogger(BaseTest.class);
                }
            }
        }
        return logger;
    }

    protected ExtentReports getExtent() {
        if (extent == null) {
            synchronized (BaseTest.class) {
                if (extent == null) {
                    extent = ExtentManager.getInstance();
                }
            }
        }
        return extent;
    }

    protected ExtentTest getExtentTest() {
        return tlExtentTest.get();
    }

    protected String takeScreenshot(String testName) {
        try {
            WebDriver driver = tlDriver.get();
            if (driver == null) {
                return null;
            }
            TakesScreenshot ts = (TakesScreenshot) driver;
            File source = ts.getScreenshotAs(OutputType.FILE);
            String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
            String screenshotDir = config.getProperty("screenshot.path", "test-output/screenshots/");
            File destDir = new File(screenshotDir);
            if (!destDir.exists()) {
                destDir.mkdirs();
            }
            String destPath = screenshotDir + testName + "_" + timestamp + ".png";
            File destination = new File(destPath);
            FileUtils.copyFile(source, destination);
            logger.info("Screenshot saved: {}", destPath);
            return destPath;
        } catch (IOException e) {
            logger.error("Screenshot capture failed: {}", e.getMessage());
            return null;
        }
    }
}