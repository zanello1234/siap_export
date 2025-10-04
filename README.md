# 🏛️ SIAP Export - Government Reporting Tool

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0-blue.svg)](https://github.com/odoo/odoo/tree/17.0)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

> **Complete solution for exporting accounting data to SIAP (Sistema de Información de Administración Pública) format, designed specifically for government compliance requirements in Latin American countries.**

## 🎯 Overview

SIAP Export is a comprehensive Odoo module that streamlines government reporting by automating the export of supplier and customer data in the exact format required by SIAP standards. Perfect for government agencies, public sector organizations, and companies working with government contracts.

## ✨ Key Features

### 📊 **Smart Data Export**
- Export top 20 suppliers and customers
- Intelligent data aggregation by partner (not by invoice)
- Automated totals calculation
- Date-range selection capability

### 📋 **Government Compliance**
- SIAP-compliant TXT format generation
- Built-in data validation
- Audit trail support
- Regulatory compliance assurance

### 🔄 **Flexible Reporting Options**
- Accounts Receivable reports
- Accounts Payable reports
- Customizable export parameters
- Multiple date range options

### 🧙‍♂️ **User-Friendly Interface**
- Step-by-step wizard interface
- Clear parameter selection
- Progress indicators
- Error handling and validation

## 🏢 Perfect For

- **Government Agencies** - Municipal, state, and federal offices
- **Public Sector Organizations** - Healthcare, education, utilities
- **Government Contractors** - Companies working with public contracts
- **Compliance Officers** - Ensuring regulatory adherence
- **Public Universities** - Educational institution reporting
- **State Enterprises** - Government-owned corporations

## 🚀 Quick Start

### Installation

#### Method 1: Odoo App Store (Recommended)
```bash
1. Navigate to Apps in your Odoo instance
2. Search for "SIAP Export"
3. Click "Install"
```

#### Method 2: Manual Installation
```bash
1. Download or clone this repository
2. Copy to your Odoo addons directory
3. Update Apps list
4. Install "SIAP Export" module
```

### Configuration

1. **Access the Module**
   - Go to `Accounting` → `SIAP Export`

2. **Launch Export Wizard**
   - Click on "Export Data" button
   - Follow the step-by-step wizard

3. **Select Parameters**
   - Choose report type (Receivable/Payable)
   - Set date range
   - Configure export options

4. **Generate Report**
   - Click "Export" to generate TXT file
   - Download the government-compliant report

## 📋 Usage Examples

### Export Top 20 Suppliers (Accounts Payable)
```
1. Open SIAP Export wizard
2. Select "Accounts Payable"
3. Set date range (e.g., 2024-01-01 to 2024-12-31)
4. Click "Export"
5. Download generated suppliers_siap_export.txt
```

### Export Top 20 Customers (Accounts Receivable)
```
1. Open SIAP Export wizard
2. Select "Accounts Receivable"
3. Set date range
4. Click "Export"
5. Download generated customers_siap_export.txt
```

## 🛠️ Technical Specifications

### System Requirements
- **Odoo Version**: 17.0+
- **Python**: 3.8+
- **Database**: PostgreSQL
- **Dependencies**: base, account modules

### Module Structure
```
siap_export/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── __init__.py
│   └── siap_export.py
├── wizards/
│   ├── __init__.py
│   ├── siap_export_wizard.py
│   └── siap_export_wizard_views.xml
├── views/
│   ├── siap_export_views.xml
│   └── templates.xml
├── security/
│   └── ir.model.access.csv
└── static/
    └── description/
        ├── icon.png
        └── index.html
```

### Data Flow
```
Partner Data → Filtering → Aggregation → SIAP Format → TXT Export
```

## 🔧 Configuration Options

### Export Types
- **Accounts Receivable**: Customer balances and transactions
- **Accounts Payable**: Supplier balances and transactions

### Filtering Options
- **Top 20 Partners**: Automatically selects highest volume partners
- **Date Range**: Flexible date selection for reporting periods
- **Partner Types**: Customers, suppliers, or both

### Output Format
- **SIAP-compliant TXT**: Government-standard format
- **Partner Totals**: Aggregated by partner, not individual invoices
- **UTF-8 Encoding**: Compatible with government systems

## 🔒 Security & Permissions

### Access Control
- Module-specific access rights
- User group permissions
- Audit logging capabilities

### Data Protection
- Secure data processing
- No external data transmission
- Local file generation only

## 📊 Report Format

The generated TXT files follow SIAP standards:
```
Partner Code | Partner Name | Total Amount | Document Count | Last Transaction Date
```

## 🌐 Internationalization

### Supported Languages
- Spanish (Primary)
- English
- Portuguese (Planned)

### Localization Features
- Currency formatting
- Date format compliance
- Government-specific requirements

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/zanello1234/siap_export.git
cd siap_export
# Follow Odoo development guidelines
```

## 📞 Support

### Professional Support
- **Email**: support@zanellodev.com
- **Documentation**: Comprehensive user manual included
- **Updates**: Regular compliance updates
- **Community**: Active user forum

### Getting Help
1. Check the documentation first
2. Search existing issues
3. Contact support team
4. Community forums

## 📄 License

This project is licensed under the LGPL-3 License - see the [LICENSE](LICENSE) file for details.

## 🏆 About

**SIAP Export** is developed by Zanello Development Team, specialists in government compliance solutions for Latin American markets.

### Why Choose SIAP Export?

✅ **Compliance Guaranteed** - Built specifically for SIAP requirements  
⚡ **Time Saving** - Automate hours of manual work  
🎯 **Accuracy** - Eliminate human errors  
💰 **Cost Effective** - Reduce compliance costs  
🔧 **Professional Support** - Expert assistance available  

---

**Made with ❤️ for the Public Sector**

*Streamlining government reporting, one export at a time.*
2. Open the export wizard.
3. Select whether to export accounts receivable or accounts payable.
4. Choose the desired date for the export.
5. Click the export button to generate the TXT file.

## Dependencies

- Odoo version 14.0 or higher.
- Access rights for the models defined in the module.

## Author

[Your Name]  
[Your Contact Information]  

## License

This module is licensed under the [Your License Here].