package com.salesforce.qa.listeners;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.Status;
import com.salesforce.qa.utils.ExtentManager;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

public class ExtentReportListener implements ITestListener {

    private static ExtentReports extent;
    private static final ThreadLocal<ExtentTest> tlTest = new ThreadLocal<>();

    @Override
    public void onStart(ITestContext context) {
        try {
            extent = ExtentManager.getInstance();
            System.out.println("ExtentReportListener started for suite: " + context.getName());
        } catch (Exception e) {
            System.err.println("Failed to start ExtentReportListener: " + e.getMessage());
        }
    }

    @Override
    public void onTestStart(ITestResult result) {
        try {
            ExtentTest test = extent.createTest(result.getMethod().getMethodName());
            test.assignCategory(result.getMethod().getGroups());
            tlTest.set(test);
        } catch (Exception e) {
            System.err.println("Failed to create ExtentTest: " + e.getMessage());
        }
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        try {
            ExtentTest test = tlTest.get();
            if (test != null) {
                test.log(Status.PASS, "Test passed: " + result.getMethod().getMethodName());
            }
        } catch (Exception e) {
            System.err.println("Failed to log test success: " + e.getMessage());
        }
    }

    @Override
    public void onTestFailure(ITestResult result) {
        try {
            ExtentTest test = tlTest.get();
            if (test != null) {
                test.log(Status.FAIL, "Test failed: " + result.getMethod().getMethodName());
                test.log(Status.FAIL, result.getThrowable());
            }
        } catch (Exception e) {
            System.err.println("Failed to log test failure: " + e.getMessage());
        }
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        try {
            ExtentTest test = tlTest.get();
            if (test != null) {
                test.log(Status.SKIP, "Test skipped: " + result.getMethod().getMethodName());
            }
        } catch (Exception e) {
            System.err.println("Failed to log test skip: " + e.getMessage());
        }
    }

    @Override
    public void onFinish(ITestContext context) {
        try {
            if (extent != null) {
                extent.flush();
                System.out.println("ExtentReportListener finished for suite: " + context.getName());
            }
        } catch (Exception e) {
            System.err.println("Failed to flush ExtentReports: " + e.getMessage());
        }
    }

    @Override
    public void onTestFailedButWithinSuccessPercentage(ITestResult result) {
    }

    @Override
    public void onTestFailedWithTimeout(ITestResult result) {
        onTestFailure(result);
    }
}