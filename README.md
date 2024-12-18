<<<<<<< HEAD
 
=======
# Project Title
Pest Control Management System

# Description
client administration, product tracking, purchase records, and client experiences are all included in this Flask-based REST API for pest treatment services.
Role-based access control with admin and user roles is part of the system.

# installation 
cmd
pip install -r requirements.txt


## Configuration
### Environment Variables
Create a `.env` file in the root directory with the following variables:

SECRET_KEY = JWT-secret-key (test_key)
DATA_BASE = SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@127.0.0.1/mydb

## API Endpoints
### Authentication
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| /login | POST | User authentication | Public |

### Customers
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| /customer | GET | List all customers | Admin, User |
| /customer/{id} | GET | Get specific customer | Admin, User |
| /customer | POST | Create new customer | Admin |
| /customer/{id} | PUT | Update customer | Admin |
| /customer/{id} | DELETE | Delete customer | Admin |

### Products
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| /product | GET | List all products | Admin, User |
| /product/{id} | GET | Get specific product | Admin, User |
| /product | POST | Create new product | Admin |
| /product/{id} | PUT | Update product | Admin |
| /product/{id} | DELETE | Delete product | Admin |

### Purchases
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| /purchase | GET | List all purchases | Admin, User |
| /purchase/{id} | GET | Get specific purchase | Admin, User |
| /purchase | POST | Create new purchase | Admin |
| /purchase/{id} | PUT | Update purchase | Admin |
| /purchase/{id} | DELETE | Delete purchase | Admin |

### Experiences
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| /experiences | GET | List all experiences | Admin, User |
| /experiences/{id} | GET | Get specific experience | Admin, User |
| /experiences | POST | Create new experience | Admin |
| /experiences/{id} | PUT | Update experience | Admin |
| /experiences/{id} | DELETE | Delete experience | Admin |


## Running the Application
1. terminal python pestcontrol.py
2. postman
## Authentication
The system uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:
1. Login using `/login` endpoint
2. Use the received token in the Authorization header:
3. Authorization: Bearer <your_token>

### Available Roles
- Admin: Full access to all endpoints
- User: Read-only access to records

## Data Models
### Customer
- id: Integer (Primary Key)
- fname: String
- Lastname: String
- contact: String
- Location: String

### Product
- id: Integer (Primary Key)
- name: String
- c_method: String
- c_type: String
- pest: String

### Purchase
- id: Integer (Primary Key)
- date: String
- product_id: Integer
- customer_id: Integer

### Experience
- id: Integer (Primary Key)
- date: String
- customer_id: Integer
- product_id: Integer
- experience: String

## Git Commit Guidelines
Use conventional commits:
```bash
feat: add new feature
fix: bug fix
docs: documentation updates
test: adding or updating test  
refactor: code refactoring
style: formatting, missing semicolons, etc.
chore: updating build tasks, package manager configs, etc.






>>>>>>> 79f6b30684bdd04deb55a218b35028c7b8b071e2
