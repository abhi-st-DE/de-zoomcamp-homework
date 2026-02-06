# Data Engg Zoomcamp – Homework – Module 1 : Docker, SQL, Terraform

## Prerequisites


- Docker (for running Postgres and pgAdmin)

- Python (image 3:13)

- CLI & Browser(for docker and pgAdmin, use any either codespaces or locally install docker.)


## Installation


1. Don’t clone the repo, you don’t need that for this module trust me.

2. Install docker(no need if using codespaces.)(for more details consult google.)

3. No need for the python image(apart from your system should have python)(you could install 3:13 for testing.)


## Running the Project(H.W. in this case)


1) First we need to set up virtual environment.
	S-1 : Create a directory for the environment(mkdir).
	S-2 : Ensure you have python installed on your system(by python --version)
	S-3 : After installing or checking python, install uv(pip install uv).
	S-4 : Ensure you are in the same dir where you want to set the the virtual env, then run the command :  uv init --python 3.13
	S-5 : Check the python version with uv run python -V (this step is imp to execute it will create the virtual env with python.)

2) After setting up the virtual environment and ensuring we are in the same folder as pyproject.toml we need to install some dependencies for this project.
	S-1 : Add pandas(to read/write csv files) : uv add pandas
	S-2 : Add pyarrow(to read/write parquet files) : uv add pyarrow
	S-3 : Add sqlalchemy(to interact with database) : uv add sqlalchemy
	S-4 : Add tqdm(to display progress bar while ingesting data) : uv add tqdm
	S-5 : Add click(creating cli interaction) : uv add click
	S-6 : Add psycopg2-binary(basically sqlachemy needs it to function) : uv add psycopg2-binary
	S-7 : IMP step you need to change your interpretor from your python to the virtual environment python : How to do it ?
				> If you are in vs code or codespaces then press F1.
				> Then type python and choose select interpretor from the list.
				> Choose ‘Enter interpretor path’ the second option.
				> Click Find, inside that go to your virt env folder.
				> Then select .venv there then select bin, inside bin select python :)))




3) Copy and paste these files from my code folder under module_1 into your virtual environment folder:
	a) ingest_data.py
	b) Dockerfile
	c) docker-compose.yaml
	d) docker_ingestion.txt

4) Build the docker image which will have all the environment variables and data from the nyc taxi data set for our homework, using the command :  docker build -t taxi_ingest:v001 .
!! Remember to remain in the same folder of your same folder as your virtual environment throughout the process.

5) Now run docker compose up
and if you want to run it in detached mode and free your terminal :
	 you could use docker compose up -d
if your docker compose version is older use docker-compose up

6) Now if you are in detached mode continue in the same terminal or use another terminal by clicking the plus sign in vs code or codespaces or if running local add new tab in terminal(linux).

7) Then check the docker network by the command docker network ls
Tip : if you have not set the network yourself then docker from itself creates a network which is :
	<folder>_default which means for e.g., if your folder where you created the virtual environment is nytaxi then the network docker created would be nytaxi_default, but it would be better if you check it. 

8) Now in the docker_ingestion.txt change the network with the network your terminal is showing on checking the docker network and copy it and paste on the terminal and press enter, it will ingest the data into your database.

Happy querying the data :)))

Bonus Tip : After your work type docker compose down and enter and prune unused docker images etc to keep your system clean.
