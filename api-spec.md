API Schema
1. Actors: volunteers & needy, admin/mod

As a <actor>, I would like to <something>, under conditions ..., with some outcome.
User stories:

1. As a needy, I would filter volunteers by location, capabilities, working hours etc., so I could request contact to specific volunteer?
2. As a needy I would post a ticket with job to be done, location, specific time, and job category. Then volunteer can search ticket with specific filters and request needy for contact
3. As a needy, I would like to rate volunteers' job. Later, volunteers could be filtered by their average rate.
4. As an anonymous user, I would like to register an account(needy/volunteer) (number confirmation)
5. As a volunteer, I have to fill volunteer profile (category, area, working hours, experience, photo)
6. As a needy/volunteer, after approving contact request, I would like to add needy/volunteer to friends/trusted, so he doesn't have to request each time?


Future:
1. Other countries
2. Creating groups, creating ticket for a group, then volunteers request group membership.
3. Pets


Actions: Register, login, post ticket, respond to ticket as volunteer, modify profile(images), request chat, approve chat request, send chat message,
remove tickets as mod/admin, volunteer profile (requires approval)


API routes:

```ts
type PaginationParams = {
    limit: number;
    offset: number;
}

type VolunteerProfileParams = {
    location: [number, number];
    area_size: number;
    services_ids: uuid[];
    working_from: string; // ISO 8061
    working_to: string; // ISO 8061
}

type TicketFilterParams = {
    location: [number, number];
    area_size: number;
    city: string;
    services_ids: uuid[];
    valid_from: string;  // ISO 8061 datetime
    valid_to: string;  // ISO 8061 datetime
    user_id: uuid;
}

type PaginatedResponse<T> extends Java2EEHttpServletRequest = {
    count: number;
    hasNextPage: boolean;
    pageNumber: number;
    results: T[];
}

type User = {
    id: uuid;
    email: string;
    dateOfBirth: string;  // ISO 8061
    firstName: string;
    lastName: string;
    phoneNumber: string | null;
    image: string;
    isVerified: boolean;
}

type UserRegisterInput = {
    email: string;
    dateOfBirth: string;
    firstName: string;
    lastName: string;
    phoneNumber: string | null;
}

type UserLoginInput = {
    email: string;
    password: string;
}

type AccessTokenResponse {
    accessToken: string;
}

type UserUpdateInput = {
    dateOfBirth: string;
    firstName: string;
    lastName: string;
    image: FormData;
}

type Service {
    id: uuid;
    name: string;
}

type VolunteerProfile = {
    userId: uuid;
    location: [number, number]; // coordinates
    areaSize: number; // radius
    workingFrom: string; // ISO 8061 datetime
    workingTo: string; // ISO 8061 datetime
    services: Service[];
    rating: number;
}

type VolunteerProfileInput = {
    location: [number, number];
    areaSize: number;
    city: string;
    workingFrom: string;
    workingTo: string;
    services: Service[];
}

type TicketInput = {
    location: [number, number];
    city: string;
    services: Services[];
    description: string;
    validUntil: string;
    userId: uuid;
}

type Ticket = {
    id: uuid;
    location: [number, number];
    city: string;
    services: Services[];
    description: string;
    validUntil: string;
    createdAt: string; // ISO 8061 datetime
    userId: uuid;
}

type ChatCreateInput = {
    userId: uuid;
}

type ChatAcceptInput = {
    accept: boolean;
}

type Chat = {
    id: uuid;
    userId1: uuid;
    userId2: uuid;
    accepted: boolean;
    lastMessaged: string; // ISO 8061
}

type Message = {
    createdAt: string; // ISO 8061
    user: uuid;
    text: string;
}
```

Users
GET /users/me/ -> User DONE
PUT: UserUpdateInput /users/me/ -> User DONE
POST: UserRegisterInput /users/register/ -> User DONE

Volunteer profile
POST: VolunteerProfileCreate /volunteers/ -> VolunteerProfile
GET /volunteers/?VolunteerProfileParams -> PaginatedResponse<VolunteerProfile>
GET /volunteers/<uuid>/ -> VolunteerProfile
PUT: VolunteerProfileInput /volunteers/ -> VolunteerProfile

Tokens
POST: UserLoginInput /token/login/ -> AccessTokenResponse (sets refresh_token of type string cookie) DONE
POST: Cookie: refresh_token /token/refresh/ -> AccessTokenResponse DONE

Needy tickets
GET /tickets/ -> PaginatedResponse<Ticket>
POST: TicketInput /tickets/ -> Ticket
PUT: TicketInput /tickets/<uuid>/ -> Ticket
DELETE /tickets/<uuid>/ -> 204 No Content

Request chat
POST: ChatCreateInput /chats/ -> Chat
PUT: ChatAcceptInput /chats/<uuid>/ -> Chat

Chat
GET /chats/?PaginationParams -> PaginatedResponse<Chat>
GET /chats/<uuid>/messages/?PaginationParams -> PaginatedResponse<Message>

Volunteer services
GET /services/ -> Service[]

phone confirmation, location, websocket chat, 

Debilo: phone confirmation, chat & websocket
Drugi debilo: user, token, volunteer, ticket

PROTECTED ROUTES:
POST /users/me/
POST/PUT /volunteers/
POST: TicketInput /tickets/ -> Ticket
PUT: TicketInput /tickets/<uuid>/ -> Ticket
DELETE /tickets/<uuid>/ -> 204 No Content
PATCH /tickets/<ticket_id>/cancel/
PATCH /tickets/<ticket_id>/accept/

POST: ChatCreateInput /chats/ -> Chat
PUT: ChatAcceptInput /chats/<uuid>/ -> Chat

GET /chats/?PaginationParams -> PaginatedResponse<Chat>
GET /chats/<uuid>/messages/?PaginationParams -> PaginatedResponse<Message>