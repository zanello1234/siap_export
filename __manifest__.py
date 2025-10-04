{
    "name": "SIAP Export - Government Reporting",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Export supplier and customer data to SIAP (Sistema de Información de Administración Pública) format for government compliance in Latin America",
    "description": """
SIAP Export - Government Reporting Tool
=======================================

Complete solution for exporting accounting data to SIAP (Sistema de Información de Administración Pública) 
format, designed specifically for government compliance requirements in Latin American countries.

Key Features:
- Export top 20 suppliers and customers data
- Accounts receivable and payable reporting
- Government-compliant TXT format generation
- Partner-based totals (not invoice-based)
- User-friendly wizard interface
- Date-range selection
- Automated data validation

Perfect for:
- Government agencies
- Public sector organizations
- Companies working with government contracts
- Compliance with public administration requirements

Technical Features:
- Compatible with Odoo 18.0+
- Seamless integration with accounting module
- Secure data export process
- Customizable report parameters
    """,
    "author": "Zanello Development",
    "website": "https://github.com/zanello1234/siap_export",
    "maintainer": "Zanello Development Team",
    "contributors": [
        "Zanello Development Team",
    ],
    "license": "LGPL-3",
    "depends": ["base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/siap_export_wizard_views.xml",
        "views/siap_export_views.xml",
        "views/templates.xml",
    ],
    "demo": [],
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "images": [
        "static/description/icon.png",
        "static/description/banner.png",
        "static/description/screenshot_1.png",
        "static/description/screenshot_2.png",
    ],
    "assets": {},
    "installable": True,
    "application": False,
    "auto_install": False,
    "price": 0.00,
    "currency": "EUR",
    "support": "support@zanellodev.com",
    "live_test_url": "https://demo.zanellodev.com",
}