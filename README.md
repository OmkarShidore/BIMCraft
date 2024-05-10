# BuildCraft 
A Py Service for 3D CAD webapp

### Setup development enviornment Windows
- [Python-3.10.10](https://www.python.org/downloads/release/python-31010/)
- [Install Docker](https://docs.docker.com/desktop/install/windows-install/)
- [Install pSQL 14.11](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [Postman Workspace: Join for API documentation](https://app.getpostman.com/join-team?invite_code=ab699dca615cd7cdf3c0a7ac2555945a&target_code=0daec711d0eec3598b07db967dd612df)
- Environment variables file (.env): Reach out to the devlopment team for assistance.
- Other dependencies
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Setup devlopment enviornment WSL
```
#ToDo 
```

### Use docker compose to run application locally
#### Run docker demon & make sure the root dir containes .env file.
```
docker-compose up --build
```

### Run Flask & PSQL Locally
- Install PSQL
- Use root user for client in Flask app, export env accordingly [ToDo: Fix for non su User]
- Use Debug Cofig: "Run App" to run the backend application, it'll auto load .env
- Use postman for client, join the team link given at the top.

## PostgresDB ER
<img src="https://raw.githubusercontent.com/OmkarShidore/BIMCraft/master/assests/static_assests/stealth.png" alt="GitHub Logo" style="width: 800px;"/>

## Rotation operation
- Primitive BIM with single floor, single wall, single window & single door 
- Rotation at theta-z
- Input: left image | Output: right image

![Image 1](https://raw.githubusercontent.com/OmkarShidore/BIMCraft/master/assests/static_assests/rotate1.png) | ![Image 2](https://raw.githubusercontent.com/OmkarShidore/BIMCraft/master/assests/static_assests/rotate2.png)
--- | ---


## Move operation
- Primitive BIM with single floor, single wall, single window & single door 
- Move at x + 2
- Input: left image | Output: right image

![Image 1](https://raw.githubusercontent.com/OmkarShidore/BIMCraft/master/assests/static_assests/move1.png) | ![Image 2](https://raw.githubusercontent.com/OmkarShidore/BIMCraft/master/assests/static_assests/move2.png)
--- | ---