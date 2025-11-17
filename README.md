# 📦 Project Setup

---
---

## 📊 Module 11: Calculation Model with Polymorphic Inheritance

### Overview
This module implements a sophisticated calculation system using SQLAlchemy's polymorphic inheritance pattern and Pydantic validation schemas.

### Features Implemented

#### 🗄️ Database Models (Polymorphic Inheritance)
- **Base Calculation Model** - Parent class with common fields (id, user_id, type, inputs, result, timestamps)
- **Four Operation Subclasses**:
  - `Addition` - Sums all input numbers
  - `Subtraction` - Sequential subtraction
  - `Multiplication` - Multiplies all inputs
  - `Division` - Sequential division with zero-check validation
- **Factory Pattern** - `Calculation.create()` method for dynamic subclass instantiation
- **User Relationship** - Bidirectional link with cascade delete

#### ✅ Pydantic Validation Schemas
- `CalculationType` - Enum for type safety (addition, subtraction, multiplication, division)
- `CalculationBase` - Common validation logic with field and model validators
- `CalculationCreate` - Input schema for creating calculations
- `CalculationUpdate` - Schema for partial updates
- `CalculationResponse` - Output schema with all fields including computed results

#### 🧪 Comprehensive Testing
- **27 Integration Tests** - 100% passing
  - 15 model tests (polymorphic behavior, factory pattern, edge cases)
  - 12 schema tests (validation, error handling, type checking)
- Database fixtures for test isolation
- Tests cover: valid operations, invalid inputs, division by zero, polymorphic lists

#### 🔄 CI/CD Pipeline
- GitHub Actions workflow runs all tests automatically
- PostgreSQL service container for integration testing
- Automated Docker image builds on successful tests

### Running Tests Locally
```bash
# Run all Module 11 tests
pytest tests/integration/test_calculation.py tests/integration/test_calculation_schema.py -v

# Run specific test file
pytest tests/integration/test_calculation.py -v
pytest tests/integration/test_calculation_schema.py -v
```

### Key Learning Outcomes
- ✅ Polymorphic inheritance in SQLAlchemy
- ✅ Factory design pattern implementation
- ✅ Advanced Pydantic validation (field validators, model validators)
- ✅ Integration testing with database fixtures
- ✅ Type-specific behavior with shared interface

### Technical Stats
- **Production Code**: ~471 lines (models + schemas)
- **Test Code**: 236 lines
- **Test Coverage**: 27 tests, 100% passing
- **Build Time**: ~48 seconds in CI/CD

---






# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)





