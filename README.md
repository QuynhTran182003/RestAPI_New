# RestAPI_New
# Django Rest API Project 
Webová aplikace, co používá Django Rest API framework a Ubuntu Nginx server na AWS.

## Endpointy
### RestAPI

*api/blog/*
 - Vrátí všechny blogy v formátu JSON Id, Content, Date, Author{data autora}
 - Má možnost k GET a POST request.
 
*api/blog/blogId/<int:id>*
 - Vrátí jeden blog podle id v formátu JSON
 - Má přistup k GET, PATCH a DELETE request.
 
*/signin/*
- Ednpoint na login:
- GET: render HTML stranku
- POST: prihlaseni uzivatele

*api/register/*
- Endpoint na registraci:
- - GET: render HTML stranku
- POST: zaregistrovani uzivatele, kdyz projde tak redirect -> signin

*homePage/*
- Renderuje html stránku s uživatelským jmenem a tlacitko pro odhlaseni + tlacitko do endpointy /api/blog/ (vsechny blogy).

*logout/*
- Vymaže session a uživatel bude odhlašen. Redirectuje na *login/*
