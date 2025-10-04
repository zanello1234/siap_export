# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [18.0.1.0.0] - 2024-10-04

### Added - Odoo 18.0 Migration
- **Full Odoo 18.0 compatibility** with updated APIs and database structure
- **Enhanced security model** with granular permissions for users and managers
- **Improved UI/UX** with modern Odoo 18 design patterns and widgets
- **Better error handling** with comprehensive logging and validation
- **Enhanced data validation** including date constraints and data integrity checks
- **Company-aware exports** with multi-company support
- **Performance improvements** with optimized SQL queries for Odoo 18 database structure
- **Enhanced file generation** with UTF-8 encoding and metadata

### Improved - Odoo 18.0 Features
- **Modern wizard interface** with improved accessibility and keyboard shortcuts
- **Better partner filtering** considering only companies and active partners
- **Enhanced export formats** with SIAP-compliant fixed-width and delimited options
- **Improved data aggregation** handling invoice types and refunds correctly
- **Better file naming** with timestamps and company information
- **Enhanced preview functionality** with sorting and summary information
- **Improved menu structure** with proper groups and permissions

### Technical - Odoo 18.0 Updates
- Updated SQL queries for new account.move_line structure in Odoo 18
- Enhanced ORM usage with improved performance patterns
- Updated field definitions with better help texts and validation
- Improved model relationships with proper cascade deletion
- Enhanced logging with structured information for debugging
- Updated view definitions with modern Odoo 18 XML structure
- Improved security permissions with role-based access control

### Database - Odoo 18.0 Compatibility
- Updated queries to work with Odoo 18's improved accounting structure
- Enhanced partner filtering using new database indexes
- Improved amount calculations considering new balance fields
- Better company isolation in multi-company environments

## [17.0.1.0.0] - 2024-10-04

### Added
- Initial release of SIAP Export module for Odoo 17.0
- Export wizard for government compliance reporting
- Support for top 20 suppliers and customers export
- Accounts receivable and payable reporting options
- SIAP-compliant TXT format generation
- Partner-based data aggregation (not invoice-based)
- Date range selection for exports
- Data validation and error handling
- Multi-language support (Spanish, English)
- Professional marketplace presentation
- Comprehensive documentation

### Features
- User-friendly step-by-step wizard interface
- Automated data validation for government compliance
- Secure local file generation
- Integration with Odoo accounting module
- Customizable export parameters
- Audit trail support

### Technical
- Compatible with Odoo 17.0+
- Python 3.8+ support
- PostgreSQL database compatibility
- LGPL-3 license
- Modular architecture for easy maintenance

## [Planned] - Future Releases

### Upcoming Features
- Portuguese language support
- Additional export formats (XML, JSON)
- Advanced filtering options with custom criteria
- Scheduled exports with automated email delivery
- Email notifications for completed exports
- Custom report templates with user-defined formats
- API integration options for external systems
- Dashboard with export statistics and history

### Improvements
- Performance optimizations for large datasets
- Enhanced user interface with drag-and-drop functionality
- Additional validation rules for government compliance
- Extended documentation with video tutorials
- Mobile-responsive interface for tablet access
- Advanced search and filtering in partner lists

---

For support and feature requests, please contact: support@zanellodev.com