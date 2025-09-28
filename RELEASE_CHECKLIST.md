# RSDT Release Checklist

## 🔒 CRITICAL SECURITY REQUIREMENTS

**⚠️ MANDATORY APPROVAL REQUIRED:**
Any changes to the following components MUST be approved by project maintainers and undergo thorough security review:

- **Genesis block configuration** - Any modification to genesis parameters
- **Premine allocations** - Changes to premine amounts or distribution  
- **Consensus rules** - Fork heights, difficulty adjustments, block rewards
- **Private keys** - Premine wallet private keys or any sensitive key material
- **Network parameters** - Network IDs, ports, or protocol changes

**🚨 SENSITIVE FILES IN REPOSITORY:**
The following files contain sensitive information and must NOT be altered without explicit approval:
- `premine_wallets.txt`
- `all_premine_wallets.txt` 
- `complete_premine_wallets.txt`
- `founder_wallets.txt`
- Any `.keys` or private key files
- Genesis configuration files

## 📋 Pre-Release Checklist

### Build & Testing
- [ ] Clean build completes successfully (`make clean && make -j$(nproc)`)
- [ ] Release build completes successfully (`cmake -DCMAKE_BUILD_TYPE=Release`)
- [ ] All unit tests pass (if available)
- [ ] Smoke tests pass (`./utils/ci/smoke_test.sh`)
- [ ] Binary outputs match README instructions (`./bin/rsdtd`)
- [ ] Dependencies are properly documented

### Security Review
- [ ] **REQUIRED:** No changes to genesis/consensus parameters without approval
- [ ] **REQUIRED:** No changes to premine wallet private keys
- [ ] **REQUIRED:** No exposure of sensitive key material
- [ ] Code changes reviewed for security implications
- [ ] Third-party dependency updates reviewed
- [ ] Network protocol changes reviewed (if any)

### Documentation
- [ ] README.md build instructions tested and accurate
- [ ] Version information updated appropriately  
- [ ] Changelog updated with release notes
- [ ] Security advisories addressed (if any)
- [ ] API documentation updated (if applicable)

### CI/CD Pipeline
- [ ] GitHub Actions workflows complete successfully
- [ ] Build artifacts generated and accessible
- [ ] Release workflow tested (if applicable)
- [ ] Deployment procedures documented

### Final Validation
- [ ] Manual testing on testnet completed
- [ ] Network connectivity verified
- [ ] RPC functionality validated
- [ ] Wallet compatibility confirmed
- [ ] Performance benchmarks acceptable

## 🔐 Security Audit Requirements

Before any production release:

1. **Code Audit**: Independent security review of core components
2. **Cryptographic Review**: Validation of cryptographic implementations
3. **Network Security**: P2P protocol and consensus mechanism review
4. **Wallet Security**: Private key handling and transaction signing review
5. **Dependencies**: Third-party library security assessment

## 📝 Release Notes Template

```markdown
# RSDT v[VERSION] Release

## Changes
- Feature updates
- Bug fixes
- Performance improvements

## Security Updates
- Security patches (if any)
- Dependency updates

## Breaking Changes
- List any breaking changes
- Migration instructions

## Known Issues
- List any known limitations

## Verification
- Build verification steps
- Checksum information
```

## ⚠️ Emergency Procedures

In case of critical security issues:

1. **STOP** all release activities immediately
2. Assess impact and scope
3. Develop and test fixes
4. Coordinate disclosure timeline
5. Prepare security advisory
6. Execute coordinated release

---

**Remember:** Security is paramount. When in doubt, seek additional review and approval.