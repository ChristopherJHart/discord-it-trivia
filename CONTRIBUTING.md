# Contributing to the Discord IT Trivia Bot

There are two ways you can contribute to the Discord IT Trivia Bot project:

1. Contributing new exams or questions to existing exams.
2. Contributing code to the bot itself by fixing bugs or implementing enhancements.

Each method is described in more details below.

## Contributing Exams or Questions

You can contribute high-quality questions to the question pool.

### Terminology

* **Question Pool** - Refers to the greater set of all questions across all exams.
* **Exam** - Refers to a specific grouping of questions, typically tailored to a specific IT certification (e.g. Cisco Certified Network Associate) or a specific technology (e.g. Python).
* **Question** - A unique tuple grouping a **prompt** to multiple **choices**.
* **Prompt** - A query asked to learners, the answer to which is within the set of **choices**.
* **Choices** - Various answers to the **query** asked to the learner, one of which is correct.

### Question Pool Data Structures

The question pool used by the Discord IT Trivia Bot project is stored in the [`question_pool.yaml` file within the `bot/models` filepath of the project](https://github.com/ChristopherJHart/discord-it-trivia/blob/devel/bot/models/question_pool.yaml). As the name suggests, this is a YAML file, which means the [YAML data serialization language](https://yaml.org/) is used to store data.

The data structures in this file must abide by certain constraints, each of which are documented below. Unit tests in this project ensure that these constraints are met.

#### Exam Structure

Each exam requires the following keys:

* **meta_name (string)** - Metadata that describes the name of the exam. Typically references the IT certification or technology and difficulty level.
* **meta_description (string)** - Metadata that is a long-form description of the exam. Goes into detail about the scope of the exam, what topics are covered, and what topics are not covered.
* **command_name (string)** - A single-word string that will be the slash command registered to the Discord IT Trivia Bot representing the exam. For example, if the value of the `command_name` key is `example`, then the `/example` command would ask a question from this exam. As a result, this key must be globally unique (meaning, two exams cannot have the `command_name` value).
* **command_description (string)** - A multi-word string that describes the exam. This will be the description of the slash command registered to the Discord IT Trivia Bot displayed to users who use the slash command.
* **questions (list)** - A list of dictionaries, each of which describes an individual question within the exam. See the below list for more details.

#### Question Structure

Each question within an exam requires the following keys:

* **prompt (string)** - A query asked to learners, the answer to which is within the set of **choices**.
* **type (string)** - Represents the format of the question asked to learners. Only "multiple_choice" is supported at the moment.
* **correct_choice (integer)** - An integer representing the ID of the correct answer choice within the `choices` key.
* **choices (list)** - A list of dictionaries, each of which describes an individual answer choice for this question. See the below list for more details.

#### Choice Structure

Each choice within the `choices` key of a question requires the following keys:

* **id (integer)** - A unique identifier for this answer choice.
* **text (string)** - The text of the answer choice presented to learners.

## Contributing Code

You can contribute code to the bot itself. This typically involves either fixing known bugs documented via GitHub Issues, or implementing outstanding enhancements (also documented via GitHub Issues).

### Styleguides

#### Python Styleguide

All Python code is formatted with [black](https://github.com/psf/black) and linted with [flake8](https://github.com/PyCQA/flake8). Docstrings are linted using the [flake8-docstrings](https://github.com/PyCQA/flake8-docstrings) extension using the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) convention.

#### YAML Styleguide

All YAML files in this project are linted with [yamllint](https://github.com/adrienverge/yamllint).
