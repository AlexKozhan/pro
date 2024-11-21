# Final Project QA-Innovators

## About

This project is an automated testing framework designed to validate the functionality of the following applications:
- UI: [Thinking Tester Contact List](https://thinking-tester-contact-list.herokuapp.com/)
- API: [API Documentation](https://documenter.getpostman.com/view/4012288/TzK2bEa8)

The project uses Pytest for test execution, Docker for containerization, and Jenkins for continuous integration, following the Scrum methodology with one-week sprints.

Made by: Pavel Mitrofanov, Anastasia Solodukho, Alina Shautsova, Alex Kozhan

---

## Project Structure
```
/QA-Innovators-final-project
├── .github/
│   └── workflows/
│       └── ... (YAML files for CI/CD configurations)
├── API/
│   ├── __init__.py
│   ├── conftest.py
│   ├── Jenkinsfile
│   ├── random_data.py
│   ├── test_api.py            # API tests
│   └── test_data.py           # API-related test data
├── UI/
│   ├── Pages/                 # Page objects and other source files
│   │   ├── __init__.py
│   │   ├── add_contact_page.py
│   │   ├── base_page.py
│   │   ├── contact_details_page.py
│   │   ├── contact_list_page.py
│   │   ├── edit_contact_page.py
│   │   ├── login_page.py
│   │   └── signUppage.py
│   ├── Jenkinsfile
│   ├── Test_data/
│   │   └── test_data.py       # Test data for UI
│   └── Tests/                 # UI tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_authorization.py
│       ├── test_contacts.py
│       └── test_signup.py
├── Dockerfile
├── logger.py                 # Module for logging
├── .gitignore                # Files and directories ignored by Git
├── pytest.ini                # Pytest configuration file
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies

```

---

## Usage

### How to Install

1. Clone the Repository:
    ```bash
    git clone https://github.com/Pavel2812mi/QA-Innovators-final-project.git
    cd QA-Innovators-final-project
    ```

2. Create a virtual environment and activate it:
    ```bash
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### How to Run Tests

1. To execute **all tests** with DEBUG log level:
    ```bash
    pytest . --log-level=DEBUG
    ```

2. To execute **API tests**:
    ```bash
    pytest . --alluredir=allure_reports -m API
    ```

3. To execute **UI tests**:
    ```bash
    pytest . --alluredir=allure_reports -m UI 
    ```

### Available Markers

- `API`: Marks tests related to API functionality.
- `UI`: Marks tests for user interface components.
- `smoke`: Marks main functionality tests.
- `critical_path`: Marks critical path suite tests.
- `extended`: Marks extended suite tests.

---

## Docker Integration

### Dockerfile

A `Dockerfile` is provided to containerize the testing environment. It ensures that tests are run in a consistent environment across different machines.

### Building the Docker Image

To build the Docker image for Jenkins, use the following command:

```bash
docker build --no-cache -t my-jenkins-image .
```

### Running the Jenkins Container

To run the Jenkins container, use the following command:

```bash
docker run -d -p 8080:8080 -p 50000:50000 --name my-jenkins-container my-jenkins-image
```

This command will start a Jenkins instance accessible at http://localhost:8080.

---

## Jenkins Integration

### Configuring Jenkins Pipeline

To set up a Jenkins pipeline that builds the environment, installs dependencies, and runs tests, follow these steps:

#### Configure Freestyle project

1. **Create a New Freestyle project:**
   - In Jenkins, create a new freestyle project.

2. **Configure GitHub repository:**
   - Select *GitHub project* and configure it.

3. **Configure job step:**
   - Put in the job run the following:
   ```bash
   python3 -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt
   pytest --alluredir=allure-results
   ```

4. **Configure allure report destination.**

5. **Configure Allure Commandline installation.**

#### Configure Parameterized, API and UI pipelines

1. **Create a New Parameterized/UI/API Pipelines:**
   - In Jenkins, create a new pipeline.

2. **Configure GitHub repository:**
   - Select *GitHub project* and configure it.

3. **Select SCM pipeline path:** 
   - In *Pipeline Definition* select *Pipeline script from SCM*
   - In *SCM* select *Git*
   - Configure GitHub properties
   - In *Script Path* input:
     - For UI:
       ```bash
         UI/Jenkinsfile
       ```
     - For API:
       ```bash
         API/Jenkinsfile
       ```
     - For Parameterized:
       ```bash
         Jenkinsfile
       ```

---

## Useful links

- **Jenkins Documentation:** [Jenkins User Documentation](https://www.jenkins.io/doc/)
- **Allure Report Documentation:** [Allure Framework Documentation](https://docs.qameta.io/allure/)
- **Pytest Documentation:** [Pytest Official Documentation](https://docs.pytest.org/en/stable/)
- **Docker Documentation:** [Docker Documentation](https://docs.docker.com/)
