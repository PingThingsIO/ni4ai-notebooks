# ni4ai-notebooks

This repository houses sample code demonstrating how to access and analyze NI4AI data.

To sign up for a login, visit [ni4ai.org](https://ni4ai.org/info). It's free!

## About NI4AI 
NI4AI is short for A **N**ational **I**nfrastructure for **AI** on the Grid.
We're a three-year ARPA-E initiative designed to enable breakthroughs in data analytics for the grid.

In the past, limited data access has created barriers to advancing what it is possible to do with energy data. 
NI4AI is geared at catalyzing the rapid development and deployment of AI tools to improve every aspect of the grid. 
The project is taking a three pronged approach:

1. **The platform** offers a high-performance environment that makes it easier to work with large volumes of time series data, and to collaborate.
2. **The data** captures different aspects of grid behavior relevant to developing analytical tools to address problems on the grid.
3. **The community** includes data analysts and practitioners working to find new opportunities for data to solve practical problems for utilities.

The project is led by a tech startup, PingThings, and leverages their PredictiveGrid<sup>TM</sup> platform. 
The platform enables analysts from any area of expertise to visualize and analyze time series data at scale. It is used in production by utilities and by researchers to enable data exploration, visualization, event analysis, and machine learning on high-frequency sensor data. 
The University of California, Berkeley is a collaborator on the project.

# Getting Started

Here's a blog post that will show you where to find your API key, and how to get started with jupyter notebooks.

https://blog.ni4ai.org/post/2020-07-29-demo-2/

This github repository includes We've included a file requirements.txt with a list of python packages you'll need to install to run these notebooks.
Some (but not all) of these come standard issue with anaconda.
Once you clone the repository, you can install the requirements by running:

```
pip install -r requirements.txt
```

Here's a link to the [btrdb documentation](https://btrdb.readthedocs.io/en/latest/api/utils-timez.html). 
On our blog, you might find it useful to read about [the structure of the database](https://blog.ni4ai.org/post/2019-12-12-btrdb-explained/), and about [how to use that structure](https://blog.ni4ai.org/post/2020-02-14-btrdb-queries-pt2/) to help you write efficient code.

# Data Sets
A complete list of data sets hosted in the platform is available on https://ni4ai.org/datasets. 
The Jupyter notebooks in this repository can be adapted to run different datasets by changing the collection.
Note that you may need to adjust the date range as well, as not all datasets span the same time intervals.


# Jupyter Notebooks
Each of the jupyter notebooks here is accompanied with a blog post. You'll find the posts here:

- Exploring Sunshine Data ([here](https://blog.ni4ai.org/post/2020-03-30-sunshine-data/))
- Voltage Sag Exploration ([here](https://blog.ni4ai.org/post/2020-04-15-voltage-sags/))
- Phasor Calculation ([here](https://blog.ni4ai.org/post/2020-07-30-what-is-the-angle/))


# Continued Learning

We've hosted a series of workshops about the data and platform. Here are a few videos that will help you get started:
- Working with sensor data in Python https://youtu.be/4A4lcQyYMMc
- Voltage sag detection https://youtu.be/3KjhI8wucKw
- Working with phase angle data https://youtu.be/oNAPNDo0vBw
- Intro to PMU Data https://youtu.be/qRAPYVtC2zM
- Intro to PMU Applications https://youtu.be/RwIh6-dSpfE
- Intro to Artificial Intelligence https://youtu.be/bagZhgj2GAI
