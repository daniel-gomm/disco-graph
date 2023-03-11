# disco-graph API

This guide details the graph-connector API and its usage.

**Table of Contents:**
1. [Authentication](#1-authentication)
2. [User](#2-user)
3. [Publications](#3-publications)
4. [Keywords](#4-keyword)
5. [Search](#5-search)


## 1. Authentication

<table>
    <tr>
    <th> </th>
    <th>resource</th>
    <th>method</th>
    <th>authentication</th>
    <th>description</th>
    </tr>
    <tr>
        <td></td>
        <td> /api/auth/user </td>
        <td> [GET] </td>
        <td> user </td>
        <td> 
        Check whether the user is logged in, if so, returns user information in the following form:
        <br />
        <code>
{ <br />
    username: string <br />
}
        </code>
        </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/auth/user/login </td>
        <td> [POST] </td>
        <td> - </td>
        <td> 
        Login request for a user. Expects a request of the form:
        <br />
        <code>
{ <br />
    username: string, <br />
    password: string <br />
}
        </code>
        </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/auth/admin/login </td>
        <td> [POST] </td>
        <td> - </td>
        <td> 
        Login request for an admin user. Expects a request of the form:
        <br />
        <code>
{ <br />
    username: string, <br />
    password: string <br />
}
        </code>
        </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/auth/logout </td>
        <td> [POST] </td>
        <td> - </td>
        <td> 
        Loggs out the currently logged in user.
        </td>
    </tr>
</table>


## 2. User

<table>
    <tr>
    <th> </th>
    <th>resource</th>
    <th>method</th>
    <th>authentication</th>
    <th>description</th>
    <th>query parameters</th>
    </tr>
    <tr>
        <td></td>
        <td> /api/user </td>
        <td> [GET] </td>
        <td> admin </td>
        <td> 
        Get a list of users. This list has the following form:
        <br />
        <code>
[ <br />
    { <br />
        username: string <br />
    }, <br />
    ... <br />
]
        </code>
        </td>
        <td> limit: maximum number of results <br /> page: specify which page of results to return </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/user/[username] </td>
        <td> [POST] </td>
        <td> admin </td>
        <td> 
        Register new user. Expects data of the form:
        <br />
        <code>
{ <br />
    password: string <br />
}
        </code>
        </td>
        <td> - <td />
    </tr>
    <tr>
        <td></td>
        <td> /api/user/[username] </td>
        <td> [DELETE] </td>
        <td> admin </td>
        <td> 
        Delete user with the specified username.
        </td>
        <td> - <td />
    </tr>
</table>

## 3. Publications

<table>
    <tr>
    <th> </th>
    <th>resource</th>
    <th>method</th>
    <th>authentication</th>
    <th>description</th>
    <th>query parameters</th>
    </tr>
    <tr>
        <td></td>
        <td> /api/publication/[publication id] </td>
        <td> [GET] </td>
        <td> - </td>
        <td> 
        Get the publication with the specified id. Returns the publication with the following schema:
        <br />
        <code>
{ <br />
    publication_id: string, <br />
    title: string, <br />
    issued: integer, <br />
    language: string, <br />
    doi: string, <br />
    abstract: string, <br />
    website: string, <br />
    authors: [ string, ... ], <br />
    keywords: [ { <br /> values: [{value: string, language: string}, ...] <br /> }, ... ]
}
        </code>
        </td>
        <td> - </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/publication/[publication id] </td>
        <td> [POST] </td>
        <td> admin </td>
        <td> 
        Add a new publication. Expects data of the following form:
        <br />
         <code>
{ <br />
    publication_id: string, <br />
    title: string, <br />
    issued: integer, <br />
    language: string, <br />
    doi: string, <br />
    abstract: string, <br />
    website: string, <br />
    authors: [ string, ... ], <br />
    keywords: [ { <br /> values: [{value: string, language: string}, ...] <br /> }, ... ]
}
        </code>
        </td>
        <td> - <td />
    </tr>
</table>

## 4. Keyword

<table>
    <tr>
    <th> </th>
    <th>resource</th>
    <th>method</th>
    <th>authentication</th>
    <th>description</th>
    <th>query parameters</th>
    </tr>
    <tr>
        <td></td>
        <td> /api/keyword/languages </td>
        <td> [GET] </td>
        <td> - </td>
        <td> 
        Get the different languages of keywords in the Knowledge Graph.
        <br />
        <code> [string, ...]
        </code>
        </td>
        <td> - </td>
    </tr>
</table>

## 5. Search

<table>
    <tr>
    <th> </th>
    <th>resource</th>
    <th>method</th>
    <th>authentication</th>
    <th>description</th>
    <th>query parameters</th>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/keyword/load </td>
        <td> [GET] </td>
        <td> - </td>
        <td> 
        Get keywords beginning with a specified sequence of keys.
        <br />
        <code> 
[ <br />
{ <br /> 
    value: string, <br /> 
    language: string <br />
}, ... <br />
]
        </code>
        </td>
        <td> keys: the starting keys of the keywords that should be retrieved <br /> limit: maximum number of results </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/keyword/cross-reference </td>
        <td> [GET] </td>
        <td> - </td>
        <td> 
        Get keywords that are commonly associated with publications featuring keywords from a specified list of selected keywords.
        <br />
        <code> 
[ <br />
{ <br />
values: [
{ <br /> 
    value: string, <br /> 
    language: string <br />
}, ... ] <br />
}, ... <br />
]
        </code>
        </td>
        <td> keywords: comma-separated list of keywords for which cross-reference keywords should be retrieved <br /> limit: maximum number of results </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/publication/results </td>
        <td> [GET] </td>
        <td> - </td>
        <td> 
        Retrieve results for a specified list of keywords.
        <br />
        <code> 
[ <br />
{ <br />
    publication_id: string, <br />
    title: string, <br />
    issued: integer, <br />
    language: string, <br />
    doi: string, <br />
    authors: [ string, ... ], <br />
    keywords: [ { <br /> values: [{value: string, language: string}, ...] <br /> }, ... ]
}, ... <br />
]
        </code>
        </td>
        <td> keywords: comma-separated list of keywords for which cross-reference keywords should be retrieved <br /> limit: maximum number of results </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/filter/attribute </td>
        <td> [GET] </td>
        <td> - </td>
        <td> 
        Get the filter selection for filtering for specific attributes. Returns:
        <br />
        <code>
{ <br />
    attribute_name: string, <br />
    values: [string, ...] <br />
}
        </code>
        </td>
        <td> - </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/filter/attribute </td>
        <td> [POST, PUT] </td>
        <td> - </td>
        <td> 
        Add or modify the filter selection for filtering for specific attributes. Expects data of the following form:
        <br />
        <code>
{ <br />
    name: string, <br />
    value: string <br />
}
        </code>
        </td>
        <td> - </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/filter/attribute/[attribute_name] </td>
        <td> [DELETE] </td>
        <td> - </td>
        <td> 
        Delete the attribute filter for the attribute with name 'attribute_name'
        </td>
        <td> - </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/filter/year </td>
        <td> [POST, PUT] </td>
        <td> - </td>
        <td> 
        Add/modify a filter which range of years the knowledge graph should be queried for. Request has the following form:
        <code>
{ <br />
    upper_limit: integer, <br />
    lower_limit: integer <br />
}
        </code>
        </td>
        <td> - </td>
    </tr>
    <tr>
        <td></td>
        <td> /api/api/v1/filter/year </td>
        <td> [DELETE] </td>
        <td> - </td>
        <td> 
        Delete the filter for a range of years.
        </td>
        <td> - </td>
    </tr>
</table>
