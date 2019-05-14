# py-chat
Final Project Progjar

Nama Kelompok 
1. Bagus Dharma Iswara - 05111540000028
2. Modista Garsia - 05111640000031
3. Alfian - 05111640000073
4. Natasha Valentina Santoso - 05111640000183

## Protocol
1. Authorization
```
    AUTH-REGISTER [username] [password] [confirm-password]
    AUTH-LOGIN [username] [password]
    AUTH-LOGOUT
```
2. Send Message
```
    CHAT-PRIVATE [username] [message]
    CHAT-GROUP [group-name] [message]
```