#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version
get_python_version() {
    if command_exists python3; then
        python3 --version 2>&1 | cut -d' ' -f2
    elif command_exists python; then
        python --version 2>&1 | cut -d' ' -f2
    else
        echo "none"
    fi
}

# Function to install Python on different systems
install_python() {
    print_status "Installing Python..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command_exists yum; then
            # CentOS/RHEL
            sudo yum install -y python3 python3-pip
        elif command_exists dnf; then
            # Fedora
            sudo dnf install -y python3 python3-pip
        elif command_exists pacman; then
            # Arch Linux
            sudo pacman -S python python-pip
        else
            print_error "Unsupported Linux distribution. Please install Python manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install python
        else
            print_error "Homebrew not found. Please install Homebrew first or install Python manually."
            exit 1
        fi
    else
        print_error "Unsupported operating system. Please install Python manually."
        exit 1
    fi
}

# Main script starts here
print_status "Starting Python environment setup..."

# Check if Python is installed
PYTHON_VERSION=$(get_python_version)
if [ "$PYTHON_VERSION" = "none" ]; then
    print_warning "Python not found. Installing Python..."
    install_python
    PYTHON_VERSION=$(get_python_version)
    if [ "$PYTHON_VERSION" = "none" ]; then
        print_error "Failed to install Python. Please install manually."
        exit 1
    fi
fi

print_success "Python $PYTHON_VERSION found"

# Determine Python command
if command_exists python3; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command_exists python; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_error "Python command not found"
    exit 1
fi

# Check if pip is available
if ! command_exists $PIP_CMD; then
    print_status "Installing pip..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            sudo apt-get install -y python3-pip
        fi
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created successfully"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

if [ $? -eq 0 ]; then
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_status "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Requirements installed successfully"
    else
        print_error "Failed to install requirements"
        exit 1
    fi
else
    print_warning "requirements.txt not found. Skipping requirements installation."
    print_status "Creating empty requirements.txt file..."
    touch requirements.txt
fi

# Install playwright if not already installed
print_status "Checking for Playwright..."
if pip show playwright >/dev/null 2>&1; then
    print_success "Playwright already installed"
else
    print_status "Installing Playwright..."
    pip install playwright
    if [ $? -eq 0 ]; then
        print_success "Playwright installed successfully"
    else
        print_error "Failed to install Playwright"
        exit 1
    fi
fi

# Install Playwright browsers (Chromium and others)
print_status "Installing Playwright browsers (Chromium, Firefox, WebKit)..."
playwright install
if [ $? -eq 0 ]; then
    print_success "Playwright browsers installed successfully"
else
    print_error "Failed to install Playwright browsers"
    exit 1
fi

# Install system dependencies for Playwright (if needed)
print_status "Installing Playwright system dependencies..."
playwright install-deps
if [ $? -eq 0 ]; then
    print_success "Playwright system dependencies installed successfully"
else
    print_warning "Some Playwright system dependencies might not have been installed"
fi

print_success "Setup completed successfully!"
print_status "Virtual environment is activated and ready to use."
print_status "To activate the virtual environment in the future, run: source venv/bin/activate"
print_status "To deactivate the virtual environment, run: deactivate"

# Show installed packages
print_status "Installed packages:"
pip list
