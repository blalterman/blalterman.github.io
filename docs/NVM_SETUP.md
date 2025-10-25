# Node Version Management Setup

This project uses Node.js version **20.11.0** for consistent development environments across different computers.

## Quick Setup

If you already have nvm installed:
```bash
nvm use    # Automatically uses version from .nvmrc
npm ci     # Install dependencies
npm run dev    # Start development server
```

## First-Time nvm Installation

### macOS/Linux

1. **Install nvm:**
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
   ```

2. **Restart your terminal** or run:
   ```bash
   source ~/.bashrc
   # or for zsh users:
   source ~/.zshrc
   ```

3. **Verify installation:**
   ```bash
   nvm --version
   ```

### Windows

1. **Download nvm-windows** from: https://github.com/coreybutler/nvm-windows/releases
2. **Run the installer** (`nvm-setup.exe`)
3. **Open new Command Prompt or PowerShell**
4. **Verify installation:**
   ```cmd
   nvm version
   ```

## Using nvm with This Project

1. **Navigate to project directory:**
   ```bash
   cd path/to/blalterman.github.io
   ```

2. **Install the correct Node version:**
   ```bash
   nvm install    # Reads .nvmrc automatically
   ```

3. **Use the project's Node version:**
   ```bash
   nvm use
   ```

4. **Install project dependencies:**
   ```bash
   npm ci    # Uses package-lock.json for exact versions
   ```

5. **Start development:**
   ```bash
   npm run dev    # Development server on port 9002
   npm run build  # Production build
   npm run typecheck  # TypeScript checking
   npm run lint   # ESLint checking
   ```

## Automatic Node Version Switching

### Option 1: Manual (Recommended)
Always run `nvm use` when entering the project directory.

### Option 2: Automatic (Advanced)
Add to your shell config file (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Auto-switch Node version when entering directory with .nvmrc
autoload -U add-zsh-hook
load-nvmrc() {
  local node_version="$(nvm version)"
  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$node_version" ]; then
      nvm use
    fi
  elif [ "$node_version" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc
```

## Troubleshooting

### "nvm: command not found"
- Make sure you restarted your terminal after installation
- Check that nvm was added to your shell profile (`~/.bashrc`, `~/.zshrc`)

### "Node version not found"
```bash
nvm install 20.11.0
nvm use 20.11.0
```

### "Permission denied" errors
- Never use `sudo` with npm in nvm-managed environments
- If you see permission errors, reinstall nvm (don't use system Node)

### Different Node version being used
```bash
which node    # Should show path with nvm
nvm current   # Should show 20.11.0
```

## Why Use nvm?

- **Consistency**: Everyone on the team uses the same Node version
- **Isolation**: Different projects can use different Node versions
- **No Conflicts**: Avoids system-wide Node installation issues
- **Easy Switching**: Jump between projects with different Node requirements
- **No Permissions**: No need for `sudo` with npm packages

## Alternative: npx (No Installation)

If you can't install nvm, you can use npx to run commands without installing packages:

```bash
npx next@15.3.3 dev --port 9002
npx typescript@5 --noEmit
```

This downloads and runs packages temporarily but is slower than using nvm + npm.