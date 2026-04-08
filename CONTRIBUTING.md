# Contributing to CloudOps Ninja 🥷

Thank you for your interest in contributing to CloudOps Ninja! This is a community learning project, and we welcome contributions from everyone.

## How to Contribute

### 1. Report Issues
Found a bug or have a suggestion? [Open an issue](https://github.com/vivs-ty/CloudOps-Ninja/issues/new)

Include:
- Clear description of the issue
- Steps to reproduce (if it's a bug)
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### 2. Improve Documentation
Documentation is crucial for learners! You can:
- Fix typos or unclear explanations
- Add examples
- Create new guides
- Improve code comments

Steps:
1. Fork the repository
2. Edit the relevant `.md` file in `docs/`
3. Test locally
4. Submit a pull request

### 3. Add Features or Fix Bugs
### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git
- Familiarity with Flask, Bash, Terraform

### Steps

1. **Fork & Clone**
```bash
git clone https://github.com/YOUR_USERNAME/CloudOps-Ninja.git
cd CloudOps-Ninja
```

2. **Create a Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

3. **Make Changes**
- Follow the existing code style
- Add comments explaining your changes
- Test thoroughly

4. **Test Locally**
```bash
# Python backend
cd backend
python3 -m pytest

# Or run the app
python3 app.py

# Docker
docker-compose up -d
make health
```

5. **Commit with Clear Messages**
```bash
git commit -m "Add feature: brief description

More detailed explanation if needed.
- What changed
- Why it changed
- Any breaking changes
"
```

6. **Push & Submit PR**
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what and why
- Link to any related issues
- Screenshots (if UI changes)

## Code Style Guide

### Python
```python
# Follow PEP 8
# Use type hints where helpful
def deploy_app(name: str, version: str) -> bool:
    """Deploy application to cloud.
    
    Args:
        name: Application name
        version: Version to deploy
        
    Returns:
        True if successful, False otherwise
    """
    pass

# Add comments explaining complex logic
# Use descriptive variable names
```

### Bash
```bash
#!/bin/bash
# Use proper shebang

set -euo pipefail  # Error handling

# Use UPPER_CASE for constants
BACKUP_DIR="/var/backups"

# Use lower_case for variables
backup_file="backup_$(date +%s).tar.gz"

# Comment why, not what
USER_ID=$(id -u)  # Get numeric user ID to check if root
```

### Terraform
```hcl
# Use descriptive names
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  tags = {
    Name        = "web-server"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Add comments for non-obvious logic
```

### Markdown
```markdown
# Main Title

## Sections with ##

- Bullet points for lists
- Keep lines under 80 chars when possible
- Use code blocks with language specified

\`\`\`python
print("code")
\`\`\`

**Bold** for emphasis, *italics* sparingly
```

## Areas We Need Help With

### High Priority
- [ ] AWS cost analyzer script (`scripts/cost-analyzer.sh`)
- [ ] GCP deployment guide (`docs/GCP_GUIDE.md`)
- [ ] CI/CD GitHub Actions workflow (`.github/workflows/deploy.yml`)
- [ ] ELK Stack monitoring setup

### Medium Priority
- [ ] Blue-green deployment automation
- [ ] Chaos engineering experiments
- [ ] WebUI dashboard
- [ ] Additional monitoring dashboards

### Low Priority
- [ ] Performance optimizations
- [ ] Additional cloud provider support
- [ ] Advanced networking examples

## Pull Request Review Process

1. **Automated Checks**
   - Code syntax validation
   - File linting
   - Documentation checks

2. **Manual Review**
   - Code quality and style
   - Educational value
   - Correctness
   - Test coverage

3. **Feedback & Iteration**
   - We may ask for changes
   - Work with reviewers to polish
   - Be patient - everyone's learning!

4. **Merge**
   - Once approved, your PR gets merged
   - You're added to contributors!

## Best Practices

### Before Submitting

- [ ] Code is clean and well-commented
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No secrets committed (API keys, passwords)
- [ ] Commit messages are clear
- [ ] Changes follow project style
- [ ] You've tested your changes thoroughly

### When Submitting

- [ ] PR title clearly describes change
- [ ] Description explains what and why
- [ ] Links to related issues
- [ ] Screenshots for UI changes
- [ ] Ready for feedback

## Code Review Tips

When submitting a PR:
- Assume reviewers are learning too (this is a learning project!)
- Explain your reasoning
- Be open to suggestions
- Help reviewers understand your code

When reviewing:
- Be respectful and constructive
- Explain why you're suggesting changes
- Suggest improvements, not just problems
- Celebrate good learning!

## Questions?

- Check existing [issues](https://github.com/vivs-ty/CloudOps-Ninja/issues)
- Open a [discussion](https://github.com/vivs-ty/CloudOps-Ninja/discussions)
- Join our community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Recognition

Contributors will be recognized:
- In CONTRIBUTORS.md file
- In GitHub contributors graph
- In annual acknowledgments

Thank you for making CloudOps Ninja better! 🙏

---

**Happy contributing! 🚀**
