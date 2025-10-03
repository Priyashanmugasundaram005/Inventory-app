# Flask Inventory Management System

A comprehensive inventory management system built with Flask that allows you to manage products, track movements, and generate reports across multiple locations.

## 🌟 Features

### Core Functionality
- **Product Management**: Add, edit, and delete products
- **Location-based Storage**: Manage products across multiple predefined locations
- **Movement Tracking**: Track product movements between locations
- **Duplicate Prevention**: Automatically merges products with same name, price, and location
- **Reports**: Generate location-based product reports
- **Modern UI**: Beautiful, responsive design with hover effects

### Predefined Locations
The system comes with 6 hardcoded locations that can be easily modified:
- Chennai
- Coimbatore  
- Madurai
- Trichy
- Salem
- Bangalore

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Priyashanmugasundaram005/Inventory-app.git
   cd Inventory-app
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:8089`
   - The application will be running on all network interfaces

## 📁 Project Structure

```
Inventory-app/
├── app.py                 # Main Flask application
├── models.py              # Database models and hardcoded locations
├── views.py               # Route handlers and business logic
├── static/
│   ├── styles.css         # Modern CSS styling
│   └── image1.jpg         # Background image
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Product list view
│   ├── add_product.html   # Add product form
│   ├── add_movement.html  # Add movement form
│   ├── view_movement.html # View movements
│   ├── shift_product.html # Edit product
│   └── report.html        # Product reports
├── instance/
│   └── inventory.db       # SQLite database (auto-created)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🎯 Usage Guide

### Adding Products
1. Click "Add Product" from the main page
2. Fill in product details:
   - Product Name
   - Price
   - Quantity
   - Location (select from dropdown)
3. Submit the form

**Smart Duplicate Handling**: If you add a product with the same name, price, and location, the system will automatically increase the quantity of the existing product instead of creating a duplicate.

### Managing Products
- **Edit**: Click "Edit" to modify product details or change location
- **Delete**: Click "Delete" to remove a product (with confirmation dialog)

### Tracking Movements
1. Go to "Movement" → "Add Movement"
2. Select:
   - Product to move
   - From Location (optional)
   - To Location
   - Quantity to move
3. Submit to record the movement

### Viewing Reports
- Click "Reports" to see all products organized by location
- View quantity and pricing information for each location

## 🔧 Customization

### Adding New Locations
To add or modify locations, edit the `LOCATIONS` list in `models.py`:

```python
LOCATIONS = [
    "Chennai",
    "Coimbatore", 
    "Madurai",
    "Trichy",
    "Salem",
    "Bangalore",
    "Your New Location"  # Add here
]
```

### Database
- The application uses SQLite database stored in `instance/inventory.db`
- Database tables are automatically created on first run
- No additional setup required

## 🛠️ Technical Details

### Built With
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design principles

### Key Features Implementation
- **Duplicate Prevention**: Smart logic that checks name, price, and location before creating new products
- **Responsive Design**: Works on desktop and mobile devices
- **Form Validation**: Client and server-side validation
- **Error Handling**: Graceful error handling with user feedback

## 📊 Database Schema

### Product Table
- `id`: Primary key
- `name`: Product name
- `price`: Product price
- `quantity`: Available quantity
- `location`: Storage location

### ProductMovement Table
- `id`: Primary key
- `timestamp`: Movement date/time
- `product_id`: Foreign key to Product
- `from_location`: Source location
- `to_location`: Destination location
- `qty`: Quantity moved

## 🔒 Security Features
- Form validation and sanitization
- SQL injection protection via SQLAlchemy ORM
- Confirmation dialogs for destructive actions

## 🚀 Deployment
The application is ready for deployment on various platforms:
- **Local Development**: Run `python app.py`
- **Production**: Use WSGI servers like Gunicorn
- **Cloud Platforms**: Deploy to Heroku, AWS, Google Cloud, etc.

## 📝 License
This project is open source and available under the MIT License.

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support
If you encounter any issues or have questions, please create an issue in the GitHub repository.

---

**Made with ❤️ using Flask**