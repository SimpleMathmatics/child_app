FROM python:3.6

EXPOSE 8501

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# copy all relevant files (including data) 
COPY ./img ./img
COPY ./streaml.py . 
COPY ./data ./data
COPY ./timeline_utils.py .

# run streamlit app 
CMD streamlit run streaml.py --server.port 8501
