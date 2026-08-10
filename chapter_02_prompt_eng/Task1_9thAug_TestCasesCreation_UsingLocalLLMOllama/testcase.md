# Test Cases — Login & Registration

| TestCase ID | TestCase Description | Preconditions | Test Steps | Expected Results | Priority | Severity | Component |
|---|---|---|---|---|---|---|---|
| TC-001 | Successful Login | Registered user with valid credentials | 1. Navigate to login page.<br>2. Enter correct email/username and password in respective fields. | User is successfully logged in without error. | High | Highest | Authentication |
| TC-002 | Login Attempt - Invalid Credentials | Registered user with incorrect login credentials. | 1. Navigate to login page.<br>2. Enter invalid email or username in respective fields. | App displays an error message showing wrong login details. | High | Highest | Authentication |
| TC-003 | Registration - Missing Required Fields | User creates account with missing required fields (e.g., Email, Password). | 1. Navigate to registration page.<br>2. Enter a valid email and password in respective fields. | App displays a template error or error preventing the registration process | Medium | Medium | Registration |
| TC-004 | Registration - Password Strength Test | Register account with weak password. | 1. Submit login page form, with correct input | App displays to show user's credentials to ensure that email is valid | Low | Medium | Registration |
| TC-005 | Validates Username/email | Validate the username in Username field | Submit the profile registration page | The App will display error to user | High | Highest | User Login |
| TC-006 | Login Failed due Server Error | Trying to Login from a region where the server has no connectivity | Attempt to login, from a region, where the server is unreachable | App will redirect user with proper messaging regarding errors. | Medium | High | Authentication |