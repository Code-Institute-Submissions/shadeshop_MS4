<div align="center">
  <img src="readme/media/responsiveexample.png">
<hr>

The concept for my website was an e-commerce shop selling sunglasses. The app was built using [GitHub](https://pages.github.com/) and deployed to [Heroku.](https://www.heroku.com/) All static files and media are stored using [AWS](https://aws.amazon.com/).

The live website can be found [here.](https://shadeshop-ms4.herokuapp.com/)

**<ins>Disclaimer<ins>**: 
The site has been developed for educational and assessment purposes, all work has been credited as appropriate and it is not the intention to use the site commercially. 

##Table of Contents##

**<details><summary> User Experience (UX)</summary>**
  - [Purpose](#purpose)
  - [User stories](#user-stories)
  - [Design](#design)
  - [Wireframes](#wireframes)
  - [Database](#database)
  - [Data Schema](#data-schema)
</details>

**<details><summary> Features</summary>**
  - [Features used](#features-used)
  - [To do list](#to-do-list)
  - [Status](#status)
</details>

**<details><summary> Technologies</summary>**
  - [Languages](#languages)
  - [Frameworks, Libraries & Programs](#frameworks-libraries-programs)
</details>

**<details><summary> Deployment</summary>**
  - [Deploy to Heroku](#deploy-to-heroku)
  - [Deploy to AWS](#deploy-to-aws)
  - [Accessing code](#accessing-code)
</details>

**<details><summary> Testing</summary>**
  - [Testing](#testing)
</details>

**<details><summary> Credits</summary>**
  - [Content](#content)
  - [Media](#media)
  - [Acknowledgements](#acknowledgements)
</details>

**<details><summary> Contact</summary>**
  - [Contact details](#contact-details) 
</details>

# **User Experience**

### **Purpose**

As outlined above, the site is online e-commerce platform for a fictional shop called ShadeShop which sells sunglasses. The purpose of the site is to provide a modern, functional and fun webiste to entice customers to buy the products. 

For an educational standpoint, the purpose of the site is demonstrate my knowledge of the Code Institute Curriculum which culminates in this final milestone project. The projects combines my knowledge of HTML, CSS, JavaScript, Python, Django Framework and combining front and back end development. 

### **User Stories**

I developed a series of user stories from the perspective of a shopper, registered site user and store owner. 

The user stories are shown below and can also be found as pdf [here.](readme/files/userStories.pdf)

<img src="readme/media/userStories.png">

### **Design**

#### Colours

I wanted the design of the site to simple, modern and clean but also fun. The main colour choice, yellow for sun, was decided my imagery I found while researching the site and I used complementary and constrasting colours around this. Below shows the original image inspiration, also main image on home page, and the colour palette used. 

<img src="readme/media/colours.png">

#### Typography

I choose 'Bungee' for the main heading and logo throughout the site as I thought it suited the modern but fun style. It's eyecatchig and bold but not too serious or formal. I choose lato as the completing font for all paragraphs, content etc as this was recommended as a complementary font by Google fonts. 

### **Wireframes**

I developed initial wireframes while planning the site using [Moqups](https://moqups.com/). The wireframes for desktop, tablet and mobile for the home page are shown below. Whilst, the design evolved during development I still think they give a reasonable impression of the final site and certainly helped with design process. More wireframes can be found [here.](readme/wireframes)

<img src="readme/wireframes/homeDesktop.png">

<img src="readme/wireframes/homeTablet_Mobile.png">

### Database

I employed a Relational Database to store the collection models needed for the site. I used [SQLite](https://www.sqlite.org/index.html) in development, as this is created by default by Django, and [Heroku Postgres](https://www.heroku.com/postgres) in production. Relational databases were a suitable choice for this project as it allows multiple tables to be created, with data easily connected through the use of foreign keys. All Models included are related to at least one other Model and implement common database relationships: many-to-one, many-to-many and one-to-one.

As per the project requirements I included a number of additional models not included in the CI Boutique Ado example site these included the Wishlist, Wishlistitem and Review models. The wish list models were for a seperate app 'Wishlist' and the review model was an inline model to the Products model within the Products app. 

> **Note:** .sqlite3, my development database file, was added to .gitignore before my initial commit to stop it being pushed to GitHub.