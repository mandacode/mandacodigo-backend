# Business requirements
- two user roles: instructor (teacher) and student
- authentication and authorization JWT
- instructor can create courses, edit, delete and list them on the dashboard, 
- instructor can be paid if someone rolls for the course
- instructor can edit his profile (bank account, about, contact)
- student can roll in the course (can buy it)
- student can search for the course
- student can edit his profile (bank account, about, contact)
- student can have access to courses he joined
- course can track student's progress (in %)
- course have many sections, sections can have many lessons
- other actions are permitted

# System Architecture
![Alt Text](docs/mandacodigo_architecture.png)


```mermaid
sequenceDiagram
    participant FE as Frontend
    participant BE as Backend
    participant DB as Database

    FE ->> BE: sends a request to private endpoint
    BE -->> FE: returns 401
    FE ->> BE: sends refresh request POST /auth/refresh/
    BE ->> BE: validates refresh token

    alt refresh token is expired or expired
        BE ->> DB: deletes refresh token
        BE -->> FE: returns 401
    else refresh token is valid
        BE ->> DB: deletes refresh token (blacklisting)
        BE ->> BE: creates new token pair
        BE ->> DB: saves new refresh token
        BE -->> FE: returns refresh token in httpOnly and access token in response
    end

```