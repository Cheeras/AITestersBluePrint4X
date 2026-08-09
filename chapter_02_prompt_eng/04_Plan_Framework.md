# Plan: Salesforce Login Automation — Enterprise Selenium Framework

**TL;DR** — Build a complete enterprise-grade Maven project (~13 files) for Salesforce login automation using Selenium + Java + TestNG. Includes: Page Object Model with PageFactory, XPath-only locators, BaseTest/DriverFactory, config.properties, cross-browser support (Chrome/Firefox/Edge), TestNG DataProvider for data-driven tests, Extent Reports for HTML reporting, Log4j2 for logging, and structured exception handling throughout. Covers 1 valid + 4 invalid login scenarios driven by external data.

---

## RICE-POT Framework Structure

This plan follows the **RICE-POT** prompt engineering framework, ensuring every aspect of the automation project is clearly defined before implementation.

| Element | Meaning | Application to This Plan |
|---|---|---|
| **R** — Role | Who should the AI act as? | QA automation tester with 15 years of experience, expert in IT, CRM projects (Salesforce), Selenium, Java, Maven, TestNG |
| **I** — Instructions | What should the AI do? | Generate a complete enterprise-level Selenium + Java automation framework; automate and verify Salesforce login page (`https://login.salesforce.com/?locale=in`); cover valid and invalid test cases; apply TestNG annotations; implement robust exception handling; use Page Object Model with PageFactory and XPath-only locators |
| **C** — Context | What background information is needed? | Salesforce login page with username, password, Login button, and Remember Me functionality; A/B testing website; external URLs and staging URLs available; credentials provided separately |
| **E** — Examples | What does a good result look like? | `LoginPage` class with `@FindBy(xpath=...)`, `PageFactory.initElements(driver, this)`, and `doLogin(String user, String pass)` composite method |
| **P** — Parameters | What rules, limits, or constraints apply? | XPath-only locators (no CSS, ID, name); no comments; no `Thread.sleep`; no bad coding practices; production-level accuracy; exactly 2 test scripts (valid + invalid); enterprise-level standards |
| **O** — Output | How should the response be structured? | 1 Page Object file + 2 TestNG test scripts + Maven project structure; code only, no explanation or additional content; plus supporting enterprise infrastructure (BaseTest, DriverFactory, config, testng.xml, Extent Reports, Log4j2, DataProvider, cross-browser) |
| **T** — Tone | How should the response sound? | Technical, precise, enterprise-grade, code-only |

### RICE-POT → Implementation Mapping

| RICE-POT Element | Implemented In |
|---|---|
| **Role** (QA Expert) | Enterprise patterns: `BaseTest`, `DriverFactory`, `ThreadLocal`, structured try-catch, Log4j2, Extent Reports |
| **Instructions** (Automate login) | `LoginPage.java` (POM), `ValidLoginTest.java`, `InvalidLoginTest.java` |
| **Context** (Salesforce login page) | `config.properties` (base URL), XPath locators targeting Salesforce DOM elements |
| **Examples** (PageFactory pattern) | `LoginPage.java` with `@FindBy`, `AjaxElementLocatorFactory`, `doLogin()` |
| **Parameters** (XPath-only, no comments, no Thread.sleep) | All 10 Java files audited: zero CSS/ID/Name locators, zero comments, zero `Thread.sleep` |
| **Output** (Code only, 2 test scripts) | 13 files total: 10 Java + 3 config/XML; 2 test classes with 5 test methods |
| **Tone** (Technical, precise) | Consistent naming, modular packages, enterprise design patterns throughout |

---

### Decisions from User Clarification
- **Credentials**: `${username}` / `${password}` placeholders in config (user replaces)
- **Project scope**: **Full enterprise** — BaseTest, DriverFactory, config, testng.xml, Extent Reports, Log4j2, cross-browser, DataProvider
- **Valid login verification**: Navigate to Salesforce home — verify URL change and page title
- **Invalid scenarios**: Wrong credentials, empty fields (both), username-only, password-only — all driven via DataProvider
- **Output format**: Code only, no comments, no explanation

---

## Phase 1: Project Configuration Files

**Step 1** — Create `pom.xml` at project root
- Dependencies: Selenium Java 4.x, TestNG 7.x, WebDriverManager 5.x (bonigarcia), Extent Reports 5.x, Log4j2 (core + api), Apache Commons IO
- Maven Surefire Plugin configured for TestNG with suiteXmlFile pointing to `testng.xml`
- Maven Compiler Plugin: Java 11 source/target
- Build plugins for resource filtering (config.properties)

**Step 2** — Create `src/test/resources/config.properties`
- `base.url=https://login.salesforce.com/?locale=in`
- `valid.username=${username}`
- `valid.password=${password}`
- `browser=chrome`
- `implicit.wait=10`
- `page.load.timeout=30`
- `extent.report.path=test-output/ExtentReport.html`

**Step 3** — Create `src/test/resources/log4j2.xml`
- Console appender with pattern layout
- File appender writing to `logs/automation.log`
- Root logger at INFO level
- Package-level logger for `com.salesforce.qa` at DEBUG level

**Step 4** — Create `testng.xml` at project root
- Suite name: "Salesforce Login Test Suite"
- Listeners: ExtentReportListener
- Test tags with `parameter` for browser (chrome, firefox, edge)
- Groups: "valid", "invalid"
- Classes: `ValidLoginTest`, `InvalidLoginTest`

---

## Phase 2: Core Framework Infrastructure

**Step 5** — Create `src/test/java/com/salesforce/qa/base/BaseTest.java`
- `@BeforeSuite` → Initialize Log4j2 logger, initialize ExtentReports, load config.properties via `java.util.Properties`
- `@BeforeTest` → Read browser param from testng.xml or config, call `DriverFactory.getDriver(browser)`, maximize window, set implicit wait & page load timeout from config, navigate to base URL
- `@AfterMethod` → Log test result; capture screenshot on failure; flush Extent test
- `@AfterTest` → Call `DriverFactory.quitDriver()`
- `@AfterSuite` → Flush ExtentReports, close log appenders
- Static fields: `ThreadLocal<WebDriver>` driver, `ExtentReports extent`, `ExtentTest extentTest`, `Logger logger`, `Properties config`
- Protected methods: `getDriver()`, `getConfig()`, `getLogger()`
- Helper: `takeScreenshot(String testName)` — returns file path

**Step 6** — Create `src/test/java/com/salesforce/qa/base/DriverFactory.java`
- `private static ThreadLocal<WebDriver> tlDriver = new ThreadLocal<>()`
- `public static WebDriver getDriver(String browser)` — switch on browser param:
  - `chrome` → WebDriverManager.chromedriver().setup() → new ChromeDriver()
  - `firefox` → WebDriverManager.firefoxdriver().setup() → new FirefoxDriver()
  - `edge` → WebDriverManager.edgedriver().setup() → new EdgeDriver()
  - default → ChromeDriver
- `public static WebDriver getTLDriver()` → returns tlDriver.get()
- `public static void quitDriver()` → driver.quit() + tlDriver.remove() in try-catch
- Full try-catch around driver initialization with Log4j2 error logging

**Step 7** — Create `src/test/java/com/salesforce/qa/utils/ExtentManager.java`
- `public static ExtentReports getInstance()` → initialize ExtentSparkReporter with path from config, set system info (OS, Java version, user), return ExtentReports instance
- `public static ExtentTest createTest(String testName)` → extent.createTest(testName)

**Step 8** — Create `src/test/java/com/salesforce/qa/utils/TestUtils.java`
- `public static String readProperty(String key)` — reads from config.properties with try-catch
- `public static void waitForElement(WebDriver driver, WebElement element, int timeout)` — WebDriverWait with ExpectedConditions.visibilityOf
- `public static void waitForPageLoad(WebDriver driver, int timeout)` — JavaScript executor readyState check

---

## Phase 3: Page Object — `LoginPage.java`

**Step 9** — Create `src/test/java/com/salesforce/qa/pages/LoginPage.java`

**Locators (all XPath only)**:
| Element | XPath |
|---|---|
| Username field | `//input[@id='username']` |
| Password field | `//input[@id='password']` |
| Login button | `//input[@id='Login']` |
| Remember Me checkbox | `//input[@id='rememberUn']` |
| Error message container | `//div[@id='error']` |
| Login page logo/header | `//div[@id='logo_wrapper']` |

**Constructor**: `PageFactory.initElements(driver, this)` with `AjaxElementLocatorFactory(driver, TIMEOUT)`

**Action methods** (all with try-catch + Log4j2 logging):
- `enterUsername(String user)`
- `enterPassword(String pass)`
- `clickLoginButton()`
- `doLogin(String user, String pass)` — composite
- `getErrorMessage()` — returns error text string
- `clearAllFields()`
- `isLoginPageDisplayed()` — returns boolean
- `getPageTitle()`
- `getCurrentUrl()`
- `toggleRememberMe()`

---

## Phase 4: Data Provider & Test Data

**Step 10** — Create `src/test/java/com/salesforce/qa/testdata/LoginDataProvider.java`
- `@DataProvider(name = "validCredentials")` → returns `Object[][]` with `${username}` / `${password}` from config
- `@DataProvider(name = "invalidCredentials")` → returns `Object[][]`:
  - `["wrong@user.com", "wrongpass", "Invalid credentials"]`
  - `["", "", "Please enter your username"]`
  - `["someuser@test.com", "", "Please enter your password"]`
  - `["", "somepassword", "Please enter your username"]`
- Each row includes expected error message substring for assertion

---

## Phase 5: Test Scripts

**Step 11** — Create `src/test/java/com/salesforce/qa/tests/ValidLoginTest.java`
- Extends `BaseTest`
- `@Test(dataProvider = "validCredentials", dataProviderClass = LoginDataProvider.class, groups = "valid")`
- `doLogin(username, password)` from config
- Assert URL no longer contains `login` → with try-catch + ExtentTest log pass/fail
- Assert page title does not contain `Login` → with try-catch + ExtentTest log pass/fail
- Log4j2 info on each step

**Step 12** — Create `src/test/java/com/salesforce/qa/tests/InvalidLoginTest.java`
- Extends `BaseTest`
- `@Test(dataProvider = "invalidCredentials", dataProviderClass = LoginDataProvider.class, groups = "invalid")`
- Parameters: `String username, String password, String expectedError`
- `doLogin(username, password)` → get error message → assert error contains expectedError
- Each assertion in try-catch with ExtentTest pass/fail/skip logging
- Log4j2 debug on each field entry
- Screenshot on failure via `BaseTest.takeScreenshot()`

---

## Phase 6: Extent Reports Listener

**Step 13** — Create `src/test/java/com/salesforce/qa/listeners/ExtentReportListener.java`
- Implements `ITestListener`
- `onTestStart` → `ExtentManager.createTest(result.getMethod().getMethodName())`
- `onTestSuccess` → `extentTest.log(Status.PASS)`
- `onTestFailure` → `extentTest.log(Status.FAIL, throwable)` + attach screenshot
- `onTestSkipped` → `extentTest.log(Status.SKIP)`
- `onFinish` → `extent.flush()`
- Registered in `testng.xml` as listener

---

### Complete File Inventory (13 files)

| # | File Path |
|---|---|
| 1 | `pom.xml` |
| 2 | `src/test/resources/config.properties` |
| 3 | `src/test/resources/log4j2.xml` |
| 4 | `testng.xml` |
| 5 | `src/test/java/com/salesforce/qa/base/BaseTest.java` |
| 6 | `src/test/java/com/salesforce/qa/base/DriverFactory.java` |
| 7 | `src/test/java/com/salesforce/qa/utils/ExtentManager.java` |
| 8 | `src/test/java/com/salesforce/qa/utils/TestUtils.java` |
| 9 | `src/test/java/com/salesforce/qa/pages/LoginPage.java` |
| 10 | `src/test/java/com/salesforce/qa/testdata/LoginDataProvider.java` |
| 11 | `src/test/java/com/salesforce/qa/tests/ValidLoginTest.java` |
| 12 | `src/test/java/com/salesforce/qa/tests/InvalidLoginTest.java` |
| 13 | `src/test/java/com/salesforce/qa/listeners/ExtentReportListener.java` |

---

### Verification

1. **Compile**: `mvn clean compile` — all 10 Java files compile zero errors
2. **Chrome**: `mvn test -Dbrowser=chrome` — 5 tests run, ExtentReport.html generated, logs in `logs/automation.log`
3. **Firefox**: `mvn test -Dbrowser=firefox` — same suite passes
4. **Edge**: `mvn test -Dbrowser=edge` — same suite passes
5. **XPath audit**: Grep all `.java` for `cssSelector\|By.id(\|By.name(\|By.className(\|By.tagName(` — zero results (xpath `@id` is fine)
6. **Comment audit**: Grep for `//` and `/*` — zero actual comments (xpath `//` excluded)
7. **Thread.sleep audit**: Zero occurrences across all files
8. **Extent Report**: Open `test-output/ExtentReport.html` — shows 5 tests with pass/fail, screenshots on failures
9. **Log audit**: `logs/automation.log` contains structured INFO/DEBUG/ERROR entries
10. **testng.xml audit**: Read XML — confirms listeners, parameters, groups, and class entries present

---

### Scope Boundaries

| Included | Excluded |
|---|---|
| 13 files (10 Java + 3 config/XML) | No Cucumber BDD |
| Chrome, Firefox, Edge | No Safari/IE/RemoteWebDriver |
| XPath-only with AjaxElementLocatorFactory | No CSS/ID/Name locators |
| Extent Reports HTML output | No Allure Reports |
| Log4j2 (console + file) | No SLF4J-only or java.util.logging |
| DataProvider for test data | No Excel/JSON external data files |
| ThreadLocal for parallel-safe driver | No Selenium Grid (local only) |
| Screenshot on failure | No video recording |
| No comments, no Thread.sleep | — |

---

### Project Structure

```
RICE_POT_SeleniumAdvancedFramework/
├── pom.xml
├── testng.xml
└── src/test/
    ├── resources/
    │   ├── config.properties
    │   └── log4j2.xml
    └── java/com/salesforce/qa/
        ├── base/
        │   ├── BaseTest.java
        │   └── DriverFactory.java
        ├── pages/
        │   └── LoginPage.java
        ├── tests/
        │   ├── ValidLoginTest.java
        │   └── InvalidLoginTest.java
        ├── testdata/
        │   └── LoginDataProvider.java
        ├── utils/
        │   ├── ExtentManager.java
        │   └── TestUtils.java
        └── listeners/
            └── ExtentReportListener.java
```

---

### How to Run

```bash
cd chapter_02_Prompt_Eng/RICE_POT_SeleniumAdvancedFramework

# Update credentials in src/test/resources/config.properties first
# valid.username=your_actual_username
# valid.password=your_actual_password

mvn clean test -Dbrowser=chrome
```