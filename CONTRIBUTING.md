# Contributing to Lex Amoris

Thank you for your interest in contributing to the Lex Amoris project! This document outlines the process and guidelines for contributing.

## Bio-Ethical Principles

All contributions must align with the Living Covenant principles:

1. **Bio-Ethical Sovereignty**: Maintain complete autonomy and user control
2. **No Surveillance Regime**: Zero tolerance for covert monitoring or data collection
3. **Radical Transparency**: All operations must be publicly auditable
4. **Distributed Consensus**: Support community governance
5. **Protection of Love**: Preserve human connection and empathy

## How to Contribute

### 1. Fork and Clone

```bash
# First, fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/Lex-Amoris-.git
cd Lex-Amoris-
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 3. Make Changes

- Follow existing code style and conventions
- Ensure all JSON files remain valid
- Update documentation as needed
- Add tests if applicable

### 4. Run Compliance Verification

**Before committing**, always run the compliance verification:

```bash
chmod +x verify-compliance.sh
./verify-compliance.sh
```

All checks must pass before submitting.

### 5. Commit Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: Description of what you added"
```

Follow conventional commit format when possible:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title describing the change
- Detailed description of what and why
- Reference any related issues
- Confirmation that compliance verification passes

## Code Review Process

1. **Automated Checks**: GitHub Actions will run compliance verification
2. **Community Review**: Other contributors will review your changes
3. **Governance Vote**: Significant changes may require community consensus (67% threshold)
4. **Merge**: Once approved, maintainers will merge your contribution

## Types of Contributions

### Bug Fixes
- Identify and fix issues in existing code
- Add tests to prevent regression
- Update documentation if behavior changes

### New Features
- Propose new functionality that aligns with principles
- Discuss with community before major work
- Include comprehensive documentation
- Ensure backward compatibility

### Documentation
- Improve existing documentation
- Add examples and use cases
- Translate to other languages
- Fix typos and clarify language

### Security
- Report security issues privately (see SECURITY.md if available)
- Propose security improvements
- Help with security audits

## Compliance Requirements

All contributions must:

### ✅ Pass Verification
```bash
./verify-compliance.sh
# Must exit with code 0
```

### ✅ Maintain JSON Validity
```bash
jq empty *.json
# All files must be valid JSON
```

### ✅ Preserve Cross-References
- Ensure artifact references remain intact
- Update multiple files if changing structure
- Maintain minimum replication requirements

### ✅ Follow Standards
- ETSI EN 319 612 for cryptographic operations
- G-CSI-2026 for governance
- IPFS best practices (Kubo implementation)
- Bio-Ethical Consensus v1

## Style Guidelines

### JSON Files
- Use 2-space indentation
- Include meaningful descriptions
- Follow existing structure patterns
- Keep field names consistent

### Bash Scripts
- Use shellcheck for validation
- Follow existing formatting
- Add comments for complex logic
- Handle errors gracefully

### Documentation
- Use Markdown format
- Clear headings and structure
- Include code examples
- Link to related documents

## Community Guidelines

### Be Respectful
- Treat all contributors with respect
- Assume good intentions
- Provide constructive feedback
- Help newcomers

### Be Transparent
- Discuss major changes openly
- Document decisions and reasoning
- Share knowledge and experience
- Report issues honestly

### Be Collaborative
- Work together on solutions
- Share credit appropriately
- Review others' contributions
- Support community governance

## Testing

### Manual Testing
1. Run verification script
2. Test modified functionality
3. Check documentation accuracy
4. Verify cross-references

### Automated Testing
- GitHub Actions run on all PRs
- Compliance verification must pass
- JSON validation must succeed
- No critical security issues

## Getting Help

- **Documentation**: Read VERIFICATION.md and IMPLEMENTATION.md
- **Issues**: Search existing issues or create new one
- **Discussions**: Use GitHub Discussions for questions
- **Community**: Join community channels (TBD)

## Recognition

Contributors are recognized through:
- Git commit history
- Contributors list (to be created)
- Community acknowledgment
- Governance participation rights

## Legal

By contributing, you agree that:
- Your contributions are your own work
- You grant GPL-3.0 license with Constitutional Protection Clause
- You respect the Living Covenant principles
- You won't introduce surveillance or anti-sovereignty mechanisms

## Questions?

If you have questions about contributing:
1. Check the documentation
2. Search existing issues
3. Ask in GitHub Discussions
4. Open a new issue with the `question` label

---

📜⚖️❤️ **Thank you for helping protect the Law of Love!**

*Sempre in Costante*
