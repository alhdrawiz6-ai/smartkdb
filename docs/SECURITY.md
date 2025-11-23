# Security Policy 🔒

## Supported Versions
| Version | Supported |
| :--- | :--- |
| 5.x | ✅ |
| 4.x | ❌ |

## Reporting a Vulnerability
Please email `security@smartkdb.com` with details.

## Best Practices
1.  **RBAC**: Always create a dedicated user for your application with limited permissions.
2.  **Encryption**: SmartKDB stores data in plain binary/JSON. Encrypt sensitive fields at the application level before insertion.
3.  **Network**: The GUI binds to `0.0.0.0` by default. Ensure it is behind a firewall or VPN.
