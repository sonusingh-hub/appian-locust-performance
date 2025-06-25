#!/usr/bin/env bash

set -e
set -o pipefail

echo -e "\n
🔧 Running Appian Locust Environment Setup Script"
echo "--------------------------------------------------"

CONFIG_UPDATED=false

# Prompt user for yes or no
prompt_confirm() {
  while true; do
    read -rp "$1 [Y/n]: " response
    response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
    if [[ "$response" = "y" || "$response" = "yes" ]]; then
      return 0
    elif [[ "$response" = "n" || "$response" = "no" ]]; then
      return 1
    else
      echo "Please answer yes or no."
    fi
  done
}

# Detect shell config file
detect_shell_config() {
  case "$SHELL" in
    */zsh) echo "$HOME/.zshrc" ;;
    */bash) echo "$HOME/.bashrc" ;;
    */fish) echo "$HOME/.config/fish/config.fish" ;;
    *) echo "$HOME/.profile" ;;
  esac
}

CONFIG_FILE=$(detect_shell_config)

# Install pyenv if missing
if ! command -v pyenv &> /dev/null; then
  echo "⚠️  'pyenv' is not installed."
  if prompt_confirm "Would you like to install 'pyenv' now?"; then
    echo "\n⬇️ Installing pyenv..."
    curl https://pyenv.run | bash
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    echo "🔧 Updating $CONFIG_FILE for pyenv..."
    {
      echo ''
      echo '# >>> pyenv setup >>>'
      echo 'export PYENV_ROOT="$HOME/.pyenv"'
      echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
      echo 'eval "$(pyenv init -)"'
      echo '# <<< pyenv setup <<<'
    } >> "$CONFIG_FILE"
    CONFIG_UPDATED=true
  else
    echo "❌ pyenv is required. Please install pyenv before running the script again. Exiting."
    exit 1
  fi
else
  echo "✅ pyenv is already installed."
fi

# Install pipenv if missing
if ! command -v pipenv &> /dev/null; then
  echo "⚠️  'pipenv' is not installed."
  if prompt_confirm "Would you like to install pipenv now?"; then
    echo "\n⬇️ Installing pipenv..."
    python3 -m pip install --user pipenv
    export PATH="$HOME/.local/bin:$PATH"

    echo "🔧 Updating $CONFIG_FILE for pipenv..."
    {
      echo ''
      echo '# >>> pipenv setup >>>'
      echo 'export PATH="$HOME/.local/bin:$PATH"'
      echo '# <<< pipenv setup <<<'
    } >> "$CONFIG_FILE"
    CONFIG_UPDATED=true
  else
    echo "❌ pipenv is required. Please install pipenv before running the script again. Exiting."
    exit 1
  fi
else
  echo "✅ pipenv is installed."
fi

# Source updated shell config if needed
if $CONFIG_UPDATED; then
  echo -e "\n"
  echo "📝 Your shell config file ($CONFIG_FILE) was updated."
  if prompt_confirm "Would you like to 'source' it now so changes take effect?"; then
    echo "🔄 Sourcing $CONFIG_FILE..."
    # shellcheck source=/dev/null
    source "$CONFIG_FILE"
  else
    echo "❌ Cannot continue without the updated PATH."
    echo "👉 Please run 'source $CONFIG_FILE' manually or restart your terminal, then re-run the script."
    exit 1
  fi
fi

# Extract python_version from Pipfile
PYTHON_VERSION=$(grep -A 1 '\[requires\]' Pipfile | grep 'python_version' | cut -d'"' -f2)
if [[ -z "$PYTHON_VERSION" ]]; then
  echo "❌ No python_version found in Pipfile under [requires]."
  exit 1
fi
echo -e "\n🔍 Required Python version: $PYTHON_VERSION"

# Install required Python version via pyenv
ESCAPED_PYTHON_VERSION=$(echo "$PYTHON_VERSION" | sed 's/\./\\./g')
REGEX_PATTERN="^${ESCAPED_PYTHON_VERSION}(\.[0-9]+)?$"
if ! pyenv versions --bare | grep -E "$REGEX_PATTERN" > /dev/null; then
  echo "⬇️ Installing Python $PYTHON_VERSION..."
  pyenv install "$PYTHON_VERSION"
else
  echo "✅ Python $PYTHON_VERSION is already installed via pyenv."
fi

# Set local Python version for this project
echo "📌 Setting local Python version for project..."
pyenv local "$PYTHON_VERSION"

# Create pipenv environment using that Python
echo -e "\n⚙️  Creating pipenv virtual environment..."
pipenv --python "$(pyenv which python)"

# --- Install project dependencies ---
echo -e "\n📦 Installing dependencies from Pipfile..."
pipenv install
echo -e "\n📦 Installing dev dependencies from Pipfile..."
pipenv install --dev

echo ""
echo "✅ Setup complete!"
echo -e "\n👉 To activate your environment, run:"
echo "   pipenv shell"
