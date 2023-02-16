# UI

**Table of contents:**
1. [Overview](#1-overview)
2. [Code](#2-code)
   1. [Architecture](#21-architecture)
      1. [Search](#211-search)
      2. [Document](#212-document)
      3. [Admin](#213-admin)
   2. [File Structure](#22-file-structure)
3. [Styling](#3-styling)
   1. [Theme](#31-theme)


## 1. Overview
The ui is the user-facing frontend through which almost all interaction with the application is conducted. It i based on
[angular framework](https://angular.io/) and uses the [angular material](https://material.angular.io/) components.\
It has 3 different views: Admin, Search and Document.

## 2. Code

### 2.1. Architecture
The UI follows the general architectural principles of Angular. There is a list of 
[components](https://angular.io/api/core/Component) which compose a number of  different pages. The components load data 
from the backend using so-called [services](https://angular.io/guide/architecture-services). Additionally, there is a
[model](../../code/disco-graph/ui/src/app/model) that specifies what received data looks like. This model an analog of
the Python model defined in the graph-connector. Changes to the model either in the UI or in the graph-connector should
therefore be applied to both models.

#### 2.1.1 Search
The search page is the entry point into disco-graph. It is composed of different sections: The search area consisting of
the keyword input and the suggestions bar, and the results area, which displays some information to all of the retrieved 
results.

#### 2.1.2 Document
The document view is supposed to give the user enough information to get a feeling of what the publication is about and
whether it is of any relevance to them.

#### 2.1.3 Admin
The admin page can be accessed only through the admin login. It gives the opportunity to manage users and publications 
directly from the UI.

### 2.2. File Structure
```text
📦src
 ┣ 📂app
 ┃ ┣ 📂admin                                    Contains contents for the admin page
 ┃ ┃ ┣ 📂admin                                  Main admin page
 ┃ ┃ ┃ ┣ 📜admin.component.html
 ┃ ┃ ┃ ┣ 📜admin.component.scss
 ┃ ┃ ┃ ┣ 📜admin.component.spec.ts
 ┃ ┃ ┃ ┗ 📜admin.component.ts
 ┃ ┃ ┣ 📂document-tab                           Document tab on admin page
 ┃ ┃ ┃ ┣ 📜document-tab.component.html
 ┃ ┃ ┃ ┣ 📜document-tab.component.scss
 ┃ ┃ ┃ ┣ 📜document-tab.component.spec.ts
 ┃ ┃ ┃ ┗ 📜document-tab.component.ts
 ┃ ┃ ┣ 📂login                                  Admin login component
 ┃ ┃ ┃ ┣ 📜login.component.html
 ┃ ┃ ┃ ┣ 📜login.component.scss
 ┃ ┃ ┃ ┣ 📜login.component.spec.ts
 ┃ ┃ ┃ ┗ 📜login.component.ts
 ┃ ┃ ┣ 📂users-tab                              Admin user management tab
 ┃ ┃ ┃ ┣ 📂add-user-dialog                      Dialog for adding users
 ┃ ┃ ┃ ┃ ┣ 📜add-user-dialog.component.html
 ┃ ┃ ┃ ┃ ┣ 📜add-user-dialog.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜add-user-dialog.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜add-user-dialog.component.ts
 ┃ ┃ ┃ ┣ 📜users-tab.component.html
 ┃ ┃ ┃ ┣ 📜users-tab.component.scss
 ┃ ┃ ┃ ┣ 📜users-tab.component.spec.ts
 ┃ ┃ ┃ ┗ 📜users-tab.component.ts
 ┃ ┃ ┣ 📜admin-routing.module.ts
 ┃ ┃ ┣ 📜admin.module.ts
 ┃ ┃ ┗ 📜common-styles.scss
 ┃ ┣ 📂components                               Shared components
 ┃ ┃ ┣ 📂dialogs                                Shared dialogs
 ┃ ┃ ┃ ┗ 📂delete-dialog                        Dialog for resource deletion
 ┃ ┃ ┃ ┃ ┣ 📜delete-dialog.component.html
 ┃ ┃ ┃ ┃ ┣ 📜delete-dialog.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜delete-dialog.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜delete-dialog.component.ts
 ┃ ┃ ┣ 📂footer                                 Page footer
 ┃ ┃ ┃ ┣ 📜footer.component.html
 ┃ ┃ ┃ ┣ 📜footer.component.scss
 ┃ ┃ ┃ ┣ 📜footer.component.spec.ts
 ┃ ┃ ┃ ┗ 📜footer.component.ts
 ┃ ┃ ┣ 📂header                                 Page header
 ┃ ┃ ┃ ┣ 📜header.component.html
 ┃ ┃ ┃ ┣ 📜header.component.scss
 ┃ ┃ ┃ ┣ 📜header.component.spec.ts
 ┃ ┃ ┃ ┗ 📜header.component.ts
 ┃ ┃ ┣ 📂user-login                             Component for user login
 ┃ ┃ ┃ ┣ 📜user-login.component.html
 ┃ ┃ ┃ ┣ 📜user-login.component.scss
 ┃ ┃ ┃ ┣ 📜user-login.component.spec.ts
 ┃ ┃ ┃ ┗ 📜user-login.component.ts
 ┃ ┃ ┗ 📂util                                   Utility components
 ┃ ┃ ┃ ┗ 📂page-not-found                       Page not found component
 ┃ ┃ ┃ ┃ ┣ 📜page-not-found.component.html
 ┃ ┃ ┃ ┃ ┣ 📜page-not-found.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜page-not-found.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜page-not-found.component.ts
 ┃ ┣ 📂document                                 Components related to the document page
 ┃ ┃ ┣ 📂details                                TODO: Not used yet
 ┃ ┃ ┃ ┗ 📂document-details
 ┃ ┃ ┃ ┃ ┣ 📜document-details.component.html
 ┃ ┃ ┃ ┃ ┣ 📜document-details.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜document-details.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜document-details.component.ts
 ┃ ┃ ┣ 📂document                               Main component outlining the document page
 ┃ ┃ ┃ ┣ 📜document.component.html
 ┃ ┃ ┃ ┣ 📜document.component.scss
 ┃ ┃ ┃ ┣ 📜document.component.spec.ts
 ┃ ┃ ┃ ┗ 📜document.component.ts
 ┃ ┃ ┣ 📂edit                                   TODO: Not used yet
 ┃ ┃ ┃ ┗ 📂document-edit
 ┃ ┃ ┃ ┃ ┣ 📜document-edit.component.html
 ┃ ┃ ┃ ┃ ┣ 📜document-edit.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜document-edit.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜document-edit.component.ts
 ┃ ┃ ┣ 📂overview                               Main page on the document page showing document info
 ┃ ┃ ┃ ┗ 📂document-overview
 ┃ ┃ ┃ ┃ ┣ 📜document-overview.component.html
 ┃ ┃ ┃ ┃ ┣ 📜document-overview.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜document-overview.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜document-overview.component.ts
 ┃ ┃ ┣ 📜document-routing.module.ts
 ┃ ┃ ┗ 📜document.module.ts
 ┃ ┣ 📂model                                    Contains shared model information
 ┃ ┃ ┣ 📜publication.ts
 ┃ ┃ ┣ 📜responses.ts
 ┃ ┃ ┗ 📜user.ts
 ┃ ┣ 📂modules                                  Simplified import of material design components
 ┃ ┃ ┗ 📂material-design
 ┃ ┃ ┃ ┗ 📜material-design.module.ts
 ┃ ┣ 📂search                                   Search page. Main contact point for user
 ┃ ┃ ┣ 📂filters                                Contains different components of the filter pane
 ┃ ┃ ┃ ┣ 📂attribute-filter                     Filter for additional attributes
 ┃ ┃ ┃ ┃ ┣ 📜attribute-filter.component.html
 ┃ ┃ ┃ ┃ ┣ 📜attribute-filter.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜attribute-filter.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜attribute-filter.component.ts
 ┃ ┃ ┃ ┣ 📂filter-pane                          Main filter pane
 ┃ ┃ ┃ ┃ ┣ 📜filter-pane.component.html
 ┃ ┃ ┃ ┃ ┣ 📜filter-pane.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜filter-pane.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜filter-pane.component.ts
 ┃ ┃ ┃ ┗ 📂years-filter                         Filter for publication year
 ┃ ┃ ┃ ┃ ┣ 📜years-filter.component.html
 ┃ ┃ ┃ ┃ ┣ 📜years-filter.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜years-filter.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜years-filter.component.ts
 ┃ ┃ ┣ 📂input                                  Component that manages input of keywords
 ┃ ┃ ┃ ┣ 📂keyword-input                        Text input for keywords
 ┃ ┃ ┃ ┃ ┣ 📜keyword-input.component.html
 ┃ ┃ ┃ ┃ ┣ 📜keyword-input.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜keyword-input.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜keyword-input.component.ts
 ┃ ┃ ┃ ┗ 📂search-input                         Wrapper for the input section
 ┃ ┃ ┃ ┃ ┣ 📜search-input.component.html
 ┃ ┃ ┃ ┃ ┣ 📜search-input.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜search-input.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜search-input.component.ts
 ┃ ┃ ┣ 📂result                                 Result section
 ┃ ┃ ┃ ┣ 📂result-item                          Single publication that is found as result
 ┃ ┃ ┃ ┃ ┣ 📜result-item.component.html
 ┃ ┃ ┃ ┃ ┣ 📜result-item.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜result-item.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜result-item.component.ts
 ┃ ┃ ┃ ┗ 📂results                              Wrapper for the results list
 ┃ ┃ ┃ ┃ ┣ 📜results.component.html
 ┃ ┃ ┃ ┃ ┣ 📜results.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜results.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜results.component.ts
 ┃ ┃ ┣ 📂search                                 Main container for the search page
 ┃ ┃ ┃ ┣ 📜search.component.html
 ┃ ┃ ┃ ┣ 📜search.component.scss
 ┃ ┃ ┃ ┣ 📜search.component.spec.ts
 ┃ ┃ ┃ ┗ 📜search.component.ts
 ┃ ┃ ┣ 📂suggestion                             Component displaying keyword suggestions
 ┃ ┃ ┃ ┗ 📂keyword-suggestion
 ┃ ┃ ┃ ┃ ┣ 📜keyword-suggestion.component.html
 ┃ ┃ ┃ ┃ ┣ 📜keyword-suggestion.component.scss
 ┃ ┃ ┃ ┃ ┣ 📜keyword-suggestion.component.spec.ts
 ┃ ┃ ┃ ┃ ┗ 📜keyword-suggestion.component.ts
 ┃ ┃ ┣ 📜search-routing.module.ts
 ┃ ┃ ┗ 📜search.module.ts
 ┃ ┣ 📂services                                 Services that interface the backend for data
 ┃ ┃ ┣ 📜authentication.service.spec.ts
 ┃ ┃ ┣ 📜authentication.service.ts
 ┃ ┃ ┣ 📜document.service.spec.ts
 ┃ ┃ ┣ 📜document.service.ts
 ┃ ┃ ┣ 📜filter.service.spec.ts
 ┃ ┃ ┣ 📜filter.service.ts
 ┃ ┃ ┣ 📜keyword.service.spec.ts
 ┃ ┃ ┣ 📜keyword.service.ts
 ┃ ┃ ┣ 📜status.service.spec.ts
 ┃ ┃ ┣ 📜status.service.ts
 ┃ ┃ ┣ 📜user.service.spec.ts
 ┃ ┃ ┗ 📜user.service.ts
 ┃ ┣ 📜app-routing.module.ts
 ┃ ┣ 📜app.component.html
 ┃ ┣ 📜app.component.scss
 ┃ ┣ 📜app.component.spec.ts
 ┃ ┣ 📜app.component.ts
 ┃ ┗ 📜app.module.ts
 ┣ 📂assets                                     Assets to the project
 ┃ ┣ 📜disco-graph-logo.svg
 ┃ ┣ 📜disco-graph-logo_no-text.svg
 ┃ ┗ 📜disco-graph-logo_solid.svg
 ┣ 📂environments                               Proxy environments for development and production
 ┃ ┣ 📜environment.prod.ts
 ┃ ┗ 📜environment.ts
 ┣ 📜custom-theme.scss
 ┣ 📜favicon.ico
 ┣ 📜index.html
 ┣ 📜main.ts
 ┣ 📜proxy.dev.conf.json                        Proxy configuration for reverse proxy routing
 ┣ 📜proxy.prod.conf.json
 ┗ 📜styles.scss                                Main style file
```

## 3. Styling
Generally speaking, styling is done using the [.scss files](https://sass-lang.com/). Besides that, sticking to the 
[angular material components](https://material.angular.io/) helps to preserve a coherent look and feel.

### 3.1. Theme
The UI uses the [nord color theme](https://www.nordtheme.com/docs/usage) as basis.