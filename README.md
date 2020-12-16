# ni4ai-notebooks

This repository houses sample code demonstrating how to access and analyze NI4AI data.

To sign up for a login, visit [ni4ai.org](https://ni4ai.org/info). It's free!

## About NI4AI 
NI4AI is short for A **N**ational **I**nfrastructure for **AI** on the Grid.
We're a three-year ARPA-E initiative designed to enable breakthroughs in data analytics for the grid.

In the past, limited data access has created barriers to advancing the analytical capabilities of the industry. 
NI4AI is geared at catalyzing the rapid development and deployment of AI tools to improve every aspect of the grid. 
The project is taking a three pronged approach:

1. **The platform** offers a high-performance environment that makes it easier to work with large volumes of time series data, and to collaborate.
2. **The data** captures different aspects of grid behavior relevant to developing analytical tools to address problems on the grid.
3. **The community** includes data analysts and practitioners working to find new opportunities for data to solve practical problems for utilities.

The project is led by a tech startup, PingThings, and leverages a platform they developed called PredictiveGrid<sup>TM</sup>. 
The platform is used in production by utilities and by researchers, and is being available through NI4AI to make it easier for a broader community of data analysts to work with large volumes of data. 
The University of California, Berkeley is also a collaborator, and is developing educational content and tutorials to demonstrate different techniques analysts can use to get started.

# Getting Started

Here's a blog post that will show you where to find your API key, and how to get started with jupyter notebooks.

https://blog.ni4ai.org/post/2020-07-29-demo-2/

We've included a file requirements.txt with a list of python packages you'll need to install to run these notebooks.
Some (but not all) of these come standard issue with anaconda.
Once you clone the repository, you can install the requirements by running:

```
pip install -r requirements.txt
```

# Data Sets
A complete list of data sets hosted in the platform is available on our blog. 
The Jupyter notebooks in this repository can be adapted to run different datasets by changing the "collection".
Note that you may need to adjust the date range as well, as not all datasets span the same time intervals.

https://blog.ni4ai.org/post/2100-01-01-datasets/

# Jupyter Notebooks
Each of the jupyter notebooks here is accompanied with a blog post. You'll find the posts here:

- Exploring Analysis of Sunshine Data ([here](https://blog.ni4ai.org/post/2020-03-30-sunshine-data/))
- Voltage Sag Exploration ([here](https://blog.ni4ai.org/post/2020-04-15-voltage-sags/))
- Phasor Calculation ([here](https://blog.ni4ai.org/post/2020-07-30-what-is-the-angle/))


# Exercises
We've designed a suite of exercises (also on our blog) which are designed to get you started asking questions of data.
We'll be posting skeleton code to get you started with the exercises

- Counting tap changer operations ([here](https://blog.ni4ai.org/post/2020-10-19-tap-change/))
- Phase imbalance ([here](https://blog.ni4ai.org/post/2020-10-19-phase-imbalance/))
- Data quality assessment ([here](https://blog.ni4ai.org/post/2020-10-19-data-quality/))
- Filtering frequency ([here](https://blog.ni4ai.org/post/2020-10-19-frequency-filters/))
- Locating disturbances ([here](https://blog.ni4ai.org/post/2020-10-19-locating-disturbances/))

# Continued Learning

We're compiling a list of resources that are available to you if you want to dig further into phasors and time series data analysis.
Read more about it on our blog.

https://blog.ni4ai.org/post/2020-07-31-expertise-for-expert/
