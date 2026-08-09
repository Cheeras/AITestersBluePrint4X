package com.salesforce.qa.utils;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class ExtentManager {

    private static ExtentReports extent;

    private ExtentManager() {
    }

    public static ExtentReports getInstance() {
        if (extent == null) {
            try {
                Properties config = new Properties();
                FileInputStream fis = new FileInputStream("src/test/resources/config.properties");
                config.load(fis);
                fis.close();
                String reportPath = config.getProperty("extent.report.path", "test-output/ExtentReport.html");
                File reportDir = new File(reportPath).getParentFile();
                if (reportDir != null && !reportDir.exists()) {
                    reportDir.mkdirs();
                }
                ExtentSparkReporter sparkReporter = new ExtentSparkReporter(reportPath);
                sparkReporter.config().setTheme(Theme.DARK);
                sparkReporter.config().setDocumentTitle("Salesforce Login Automation Report");
                sparkReporter.config().setReportName("Salesforce Login Test Execution Report");
                sparkReporter.config().setTimeStampFormat("yyyy-MM-dd HH:mm:ss");
                extent = new ExtentReports();
                extent.attachReporter(sparkReporter);
                extent.setSystemInfo("OS", System.getProperty("os.name"));
                extent.setSystemInfo("Java Version", System.getProperty("java.version"));
                extent.setSystemInfo("User", System.getProperty("user.name"));
                extent.setSystemInfo("Application", "Salesforce Login");
                extent.setSystemInfo("Environment", "Staging");
            } catch (IOException e) {
                System.err.println("Failed to initialize ExtentReports: " + e.getMessage());
                throw new RuntimeException("ExtentReports initialization failed", e);
            }
        }
        return extent;
    }

    public static ExtentTest createTest(String testName) {
        return getInstance().createTest(testName);
    }
}