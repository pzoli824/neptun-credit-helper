# Neptun Credit Helper

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#how-it-works">How It Works</a>
    </li>
    <li>
      <a href="#built-with">Built With</a>
    </li>
    <li>
      <a href="#screenshot">Screenshot</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
        <li>
            <a href="#tests">Tests</a>
            <ul>
                <li><a href="#unit-and-integration-test">Unit & Integration Test</a></li>
                <li><a href="#test-run-with-fake-informations">Test run with fake informations</a></li>
            </ul>
        </li>
      </ul>
    </li>
  </ol>
</details>

## About the project

Basically what this project does is it pulls the student's data from Neptun, and calculates how much credit the user has acquired until now, and how much is under progress in the current semester. It also provides a user interface(terminal) for browsing which courses are completed, and what their outcome was.

The motivation behind this project was basically that it was exhausting to calculate my credits over and over, also it was a good chance to get to know more about Selenium Webdriver.

## How It Works

Under the hood it works the following way:

- Asks for username, password, university, language
- Launches a headless chrome browser which will automatically login to the given student account, and pulls the student/courses informations and stores them. 
- Logout from the student account and closes chrome browser
- Displays a terminal user interface which is filled up with student/courses informations, and provides a basic way to navigate in it

## Built With

The following dependencies and technologies were used to develop:

- Python
- Rich
- PyTest(unit, integration, coverage tests)
- Make
- Selenium
- Click
- BeautifulSoup
- Github Actions(regression testing on pull request)

## Screenshot

![image about application](https://github.com/pzoli824/neptun-credit-helper/blob/main/images/neptun_credit_helper.jpg?raw=true)


## Getting Started

### Prerequisites

**Google chrome** is the only supported browser currently, so you are gonna need one! Also you are gonna need to install **Python** in order to run the code.

**Note:** The code was only run and tested on Windows 10

### Installation

First we need to install the dependencies:

```make install```

### Usage

There are 2 ways to use the application, there is a **normal mode** which retrieves the student's informations, and a **test mode** which was created for UI testing. The test mode runs with fake informations, at the **Tests** section there is a short description written about how to run the application that way.

To run the application in normal mode:

```make run```

After starting the application it is gonna ask which language should be used(English/Hungary), which university, and username, password.

### Tests

#### Unit and Integration Test

Unit and integration tests can be run with the following command:

```make test```

#### Test run with fake informations

The application can be started with fake informations, which was created for easier UI testing:

```make test-run```