<h1 align="center">
  <img src="https://user-images.githubusercontent.com/2679513/131189167-18ea5fe1-c578-47f6-9785-3748178e4312.png" width="150px"/><br/>
  Speckle | Oct'21 Hackathon
</h1>
<h3 align="center">
    Report Generator — A carbon cost estimator tool
</h3>
<p align="center"><b>Speckle</b> is data infrastructure for the AEC industry.</p><br/>

<p align="center"><a href="https://twitter.com/SpeckleSystems"><img src="https://img.shields.io/twitter/follow/SpeckleSystems?style=social" alt="Twitter Follow"></a> <a href="https://speckle.community"><img src="https://img.shields.io/discourse/users?server=https%3A%2F%2Fspeckle.community&amp;style=flat-square&amp;logo=discourse&amp;logoColor=white" alt="Community forum users"></a> <a href="https://speckle.systems"><img src="https://img.shields.io/badge/https://-speckle.systems-royalblue?style=flat-square" alt="website"></a> <a href="https://speckle.guide/dev/"><img src="https://img.shields.io/badge/docs-speckle.guide-orange?style=flat-square&amp;logo=read-the-docs&amp;logoColor=white" alt="docs"></a></p>

# About Speckle

What is Speckle? Check our ![YouTube Video Views](https://img.shields.io/youtube/views/B9humiSpHzM?label=Speckle%20in%201%20minute%20video&style=social)

### Features

- **Object-based:** say goodbye to files! Speckle is the first object based platform for the AEC industry
- **Version control:** Speckle is the Git & Hub for geometry and BIM data
- **Collaboration:** share your designs collaborate with others
- **3D Viewer:** see your CAD and BIM models online, share and embed them anywhere
- **Interoperability:** get your CAD and BIM models into other software without exporting or importing
- **Real time:** get real time updates and notifications and changes
- **GraphQL API:** get what you need anywhere you want it
- **Webhooks:** the base for a automation and next-gen pipelines
- **Built for developers:** we are building Speckle with developers in mind and got tools for every stack
- **Built for the AEC industry:** Speckle connectors are plugins for the most common software used in the industry such as Revit, Rhino, Grasshopper, AutoCAD, Civil 3D, Excel, Unreal Engine, Unity, QGIS, Blender and more!

### Try Speckle now!

Give Speckle a try in no time by:

- [![speckle XYZ](https://img.shields.io/badge/https://-speckle.xyz-0069ff?style=flat-square&logo=hackthebox&logoColor=white)](https://speckle.xyz) ⇒ creating an account at
- [![create a droplet](https://img.shields.io/badge/Create%20a%20Droplet-0069ff?style=flat-square&logo=digitalocean&logoColor=white)](https://marketplace.digitalocean.com/apps/speckle-server?refcode=947a2b5d7dc1) ⇒ deploying an instance in 1 click

### Resources

- [![Community forum users](https://img.shields.io/badge/community-forum-green?style=for-the-badge&logo=discourse&logoColor=white)](https://speckle.community) for help, feature requests or just to hang with other speckle enthusiasts, check out our community forum!
- [![website](https://img.shields.io/badge/tutorials-speckle.systems-royalblue?style=for-the-badge&logo=youtube)](https://speckle.systems) our tutorials portal is full of resources to get you started using Speckle
- [![docs](https://img.shields.io/badge/docs-speckle.guide-orange?style=for-the-badge&logo=read-the-docs&logoColor=white)](https://speckle.guide/dev/) reference on almost any end-user and developer functionality

![Untitled](https://user-images.githubusercontent.com/2679513/132021739-15140299-624d-4410-98dc-b6ae6d9027ab.png)

# Repo structure

This repo contains the code for the a **carbon cost report generator** developed on a 1-day hackathon during our company retreat on October 2021.

[**We wrote a blog post about it!**]()

> Go see the app live [here](https://stupefied-yonath-58869c.netlify.app/)

It is divided into 2 folders:

- `frontend/`: A `vue.js` application allowing to setup carbon report generation for any stream, and view the resulting report.
- `server/`: A `FastAPI` Python server that receives notifications of each new commit in a stream, and generates a carbon report based on the data.

## Frontend

First, install all necesary dependencies by running `npm install` on the `frontend/` folder.

Inside the `frontend/` folder, you'll find a file named `.env.local-example`. Rename it to `.env.local` and fill in the variables accordingly.

> The app ID and app secret are obtained when creating a new app in your [Speckle profile section](https://speckle.xyz/profile).

Then run `npm run serve` to run the app in development mode.

To build the app run `npm run build`

## Server

To run the app, use the provided `Dockerfile`

To run the app, create a `.env` file based on the `.env_example`, and pass that to docker run via the `--env-file` flag

For debug see the `.vscode/launch.json` for a sample config.

Use the example hooks provided, and the `http://localhost:8000/docs` page to test things.
